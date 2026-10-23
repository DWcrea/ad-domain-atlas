#!/usr/bin/env python3
"""把数据库导出成可直接订阅/导入的规则文件。

用法：
    python tools/export_rules.py                       # 默认导出 block + block-cost + partial
    python tools/export_rules.py --include block       # 只导出「放心拦」的部分
    python tools/export_rules.py --min-confidence high # 只要已确认的条目
    python tools/export_rules.py --split-vendor        # 按厂商拆成多个文件
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import REPO_URL, ROOT, VERDICTS, load_all, setup_stdio  # noqa: E402

CONF_ORDER = {"high": 3, "medium": 2, "low": 1}
SOURCE_URL = REPO_URL


def _banner(title: str, count: int, extra: str = "") -> list[str]:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"! Title: ad-domain-atlas · {title}",
        f"! Entries: {count}",
        f"! Generated: {stamp}",
        f"! Source: {SOURCE_URL}",
        "! 说明：由 data/ 下的 YAML 自动生成，请勿手工修改。",
    ]
    if extra:
        lines.append(f"! {extra}")
    return lines


def write_adguard(path: Path, groups: dict[str, list], title: str, extra: str) -> int:
    total = sum(len(v) for v in groups.values())
    out = _banner(title, total, extra)
    for vendor_name, items in groups.items():
        out += ["", f"! ===== {vendor_name} ====="]
        for e in items:
            out.append(e.rule)
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return total


def write_hosts(path: Path, groups: dict[str, list], title: str, extra: str) -> int:
    total = sum(len(v) for v in groups.values())
    out = [f"# {title}", f"# Entries: {total}", f"# {extra}", ""]
    for vendor_name, items in groups.items():
        out.append(f"# ===== {vendor_name} =====")
        for e in items:
            out.append(f"0.0.0.0 {e.domain}")
        out.append("")
    path.write_text("\n".join(out), encoding="utf-8", newline="\n")
    return total


def write_dnsmasq(path: Path, groups: dict[str, list], title: str, extra: str) -> int:
    total = sum(len(v) for v in groups.values())
    out = [f"# {title}", f"# Entries: {total}", f"# {extra}", ""]
    for vendor_name, items in groups.items():
        out.append(f"# ===== {vendor_name} =====")
        for e in items:
            out.append(f"address=/{e.domain}/0.0.0.0")
            out.append(f"address=/{e.domain}/::")
        out.append("")
    path.write_text("\n".join(out), encoding="utf-8", newline="\n")
    return total


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="导出拦截规则")
    parser.add_argument(
        "--out", default=str(ROOT / "lists"), help="输出目录，默认 lists/"
    )
    parser.add_argument(
        "--include",
        default="block,block-cost",
        help="包含哪些判定，逗号分隔，默认 block,block-cost。"
        "partial 不建议自动导出（它需要按路径手写规则）",
    )
    parser.add_argument(
        "--min-confidence",
        default="low",
        choices=["high", "medium", "low"],
        help="最低置信度，默认 low（不过滤）",
    )
    parser.add_argument(
        "--split-vendor", action="store_true", help="按厂商拆分为多个文件"
    )
    parser.add_argument(
        "--repo",
        default=REPO_URL,
        help="写入规则文件头的仓库地址",
    )
    args = parser.parse_args()

    global SOURCE_URL
    SOURCE_URL = args.repo

    include = {x.strip() for x in args.include.split(",") if x.strip()}
    unknown = include - set(VERDICTS)
    if unknown:
        print(f"未知判定：{', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    floor = CONF_ORDER[args.min_confidence]
    vendors, entries = load_all()

    if "partial" in include:
        print(
            "注意：partial 条目会按主机名整域导出，可能破坏同域业务功能。"
            "这类条目建议手写路径规则。",
            file=sys.stderr,
        )

    selected = [
        e
        for e in entries
        if e.verdict in include
        and CONF_ORDER.get(e.confidence, 0) >= floor
        and e.status == "active"
    ]
    allowed = [e for e in entries if e.verdict == "keep" and e.status == "active"]

    groups: dict[str, list] = defaultdict(list)
    for e in selected:
        groups[vendors[e.vendor].name].append(e)
    for items in groups.values():
        items.sort(key=lambda x: x.domain)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    extra = f"包含判定：{', '.join(sorted(include))} · 最低置信度：{args.min_confidence}"

    if args.split_vendor:
        slug = lambda s: "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")
        for name, items in groups.items():
            sub = {name: items}
            write_adguard(out_dir / f"adguard-{slug(name)}.txt", sub, name, extra)
        print(f"已按厂商拆分导出 {len(groups)} 个文件到 {out_dir}")
    else:
        n1 = write_adguard(out_dir / "adguard.txt", groups, "AdGuard / ABP 拦截规则", extra)
        n2 = write_hosts(out_dir / "hosts.txt", groups, "hosts 拦截规则", extra)
        n3 = write_dnsmasq(
            out_dir / "dnsmasq.conf", groups, "dnsmasq 拦截规则", extra
        )
        print(f"已导出 {n1} 条 AdGuard 规则 / {n2} 条 hosts / {n3} 条 dnsmasq 到 {out_dir}")

    # 放行清单单独一份，永远导出，不受 --include 影响
    allow_groups: dict[str, list] = defaultdict(list)
    for e in allowed:
        allow_groups[vendors[e.vendor].name].append(e)
    for items in allow_groups.values():
        items.sort(key=lambda x: x.domain)

    allow_path = out_dir / "allowlist.txt"
    total = sum(len(v) for v in allow_groups.values())
    out = _banner("放行清单（误杀保护）", total, "建议置于所有拦截规则之前")
    out += ["", "! 语法说明：@@ 开头为白名单规则，AdGuard / uBlock 均支持。"]
    for vendor_name, items in allow_groups.items():
        out += ["", f"! ===== {vendor_name} ====="]
        for e in items:
            out.append(f"@@{e.rule}")
    allow_path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")

    print(f"已导出 {total} 条放行规则到 {allow_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
