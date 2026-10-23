#!/usr/bin/env python3
"""把本库的域名和现成规则库做覆盖比对。

目的：搞清楚「这些域名，主流规则库已经拦了多少」，剩下的才是需要自己补的。

用法：
    python tools/check_lists.py --list ./oisd_big.txt --list ./anti-ad.txt
    python tools/check_lists.py --list https://big.oisd.nl/ --out data/coverage.json
    python tools/check_lists.py --list ./hosts.txt --name SM-Ad-FuckU-hosts
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import ROOT, load_all, setup_stdio  # noqa: E402

DOMAIN_RE = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$"
)
IP_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$|^::1?$|^0\.0\.0\.0$")


def read_source(src: str) -> str:
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(
            src, headers={"User-Agent": "ad-domain-atlas/1.0 (+coverage check)"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8", errors="replace")
    return Path(src).read_text(encoding="utf-8", errors="replace")


def parse_domains(text: str) -> set[str]:
    """兼容 ABP、hosts、纯域名三种格式。"""
    domains: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line[0] in "!#[":
            continue
        if line.startswith(("@@", "/")):
            continue
        if line.startswith("||"):
            body = line[2:]
            for sep in ("^", "$", "/", "|"):
                idx = body.find(sep)
                if idx != -1:
                    body = body[:idx]
            body = body.strip().lower().lstrip("*.")
            if body and "*" not in body and DOMAIN_RE.match(body):
                domains.add(body)
            continue
        if line.startswith("|"):
            continue
        parts = line.split()
        if not parts:
            continue
        if IP_RE.match(parts[0]):
            candidates = parts[1:]
        else:
            candidates = parts[-1:]
        for cand in candidates:
            cand = cand.lower().strip(".")
            if cand.startswith("*."):
                cand = cand[2:]
            if DOMAIN_RE.match(cand):
                domains.add(cand)
    return domains


def list_name(src: str, override: str | None) -> str:
    if override:
        return override
    if src.startswith(("http://", "https://")):
        tail = src.rstrip("/").split("/")[-1]
        return tail or src
    return Path(src).name


def display_source(src: str) -> str:
    """仓库内的文件用相对路径，避免把本地绝对路径写进提交物。"""
    if src.startswith(("http://", "https://")):
        return src
    try:
        return Path(src).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(src).name


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="规则库覆盖比对")
    parser.add_argument(
        "--list",
        action="append",
        required=True,
        metavar="PATH_OR_URL",
        help="规则文件路径或 URL，可重复",
    )
    parser.add_argument("--name", action="append", help="与 --list 顺序对应的显示名")
    parser.add_argument(
        "--out", default=str(ROOT / "data" / "coverage.json"), help="输出 JSON 路径"
    )
    args = parser.parse_args()

    names = args.name or []

    vendors, entries = load_all()

    blocked: set[str] = set()
    list_info = []
    for i, src in enumerate(args.list):
        try:
            text = read_source(src)
        except Exception as exc:  # noqa: BLE001
            print(f"读取失败 {src}：{exc}", file=sys.stderr)
            return 2
        found = parse_domains(text)
        blocked |= found
        info = {
            "name": list_name(src, names[i] if i < len(names) else None),
            "source": display_source(src),
            "entries": len(found),
        }
        list_info.append(info)
        print(f"载入 {info['name']}：{len(found):,} 个域名")

    if not blocked:
        print("没有解析出任何域名，检查一下输入格式", file=sys.stderr)
        return 2

    exact = children = none = 0
    uncovered = []
    for e in entries:
        if e.domain in blocked:
            exact += 1
        elif e.scope == "apex" and any(
            d.endswith(e.domain + ".") for d in blocked
        ):
            children += 1
        else:
            none += 1
            uncovered.append(
                {
                    "domain": e.domain,
                    "vendor": vendors[e.vendor].name,
                    "verdict": e.verdict,
                    "category": e.category,
                    "summary": e.summary,
                }
            )

    total = len(entries)
    covered = exact + children
    coverage = {
        "generated": date.today().isoformat(),
        "lists": list_info,
        "summary": {
            "total": total,
            "exact": exact,
            "children": children,
            "none": none,
            "rate": round(covered / total * 100, 1) if total else 0.0,
        },
        "uncovered": sorted(uncovered, key=lambda x: (x["vendor"], x["domain"])),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )

    print()
    print(f"收录域名 {total} 条")
    print(f"  直接命中 {exact} 条")
    print(f"  仅被上级域覆盖 {children} 条")
    print(f"  完全未覆盖 {none} 条")
    print(f"  覆盖率 {coverage['summary']['rate']}%")
    print(f"\n已写入 {out_path}，运行 build_docs.py 可生成 docs/coverage.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
