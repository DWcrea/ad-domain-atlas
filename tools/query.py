#!/usr/bin/env python3
"""查询某个广告域名是做什么的、能不能拦。

用法：
    python tools/query.py doubleclick.net
    python tools/query.py --vendor google
    python tools/query.py --verdict keep
    python tools/query.py --category ad-serving --blockable
    python tools/query.py appsflyer --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import (  # noqa: E402
    CATEGORIES,
    CONFIDENCE,
    SCOPES,
    STATUSES,
    VERDICTS,
    Entry,
    load_all,
    search,
    setup_stdio,
)

LABEL_W = 6


def _kv(label: str, value: str) -> str:
    pad = " " * max(1, LABEL_W - len(label) * 2)
    return f"  {label}{pad}{value}"


def render_entry(entry: Entry, vendors: dict) -> str:
    vendor = vendors[entry.vendor]
    cat = CATEGORIES.get(entry.category, (entry.category, ""))[0]
    verdict = VERDICTS.get(entry.verdict, (entry.verdict, ""))[0]
    conf = CONFIDENCE.get(entry.confidence, entry.confidence)

    lines = [
        "",
        f"  {entry.domain}",
        f"  {'=' * (len(entry.domain) + 2)}",
        _kv("产品", entry.product),
        _kv("归属", f"{vendor.display}  [{entry.owner or vendor.name}]"),
        _kv("分类", f"{cat}  ({entry.category})"),
        _kv("判定", f"{verdict}  ·  {SCOPES.get(entry.scope, entry.scope)}"),
        _kv("置信度", conf),
    ]
    if entry.status != "active":
        lines.append(_kv("状态", STATUSES.get(entry.status, entry.status)))
    if entry.tags:
        lines.append(_kv("标签", "、".join(entry.tags)))

    lines += ["", "  用途", "  " + "-" * 40]
    lines += [f"  {s}" for s in _wrap(entry.purpose)]
    lines += ["", "  拦截后果", "  " + "-" * 40]
    lines += [f"  {s}" for s in _wrap(entry.impact or "—")]
    lines += ["", "  规则", "  " + "-" * 40, f"  {entry.effective_rule}"]

    if entry.notes:
        lines += ["", "  备注", "  " + "-" * 40]
        lines += [f"  {s}" for s in _wrap(entry.notes)]
    if entry.refs:
        lines += ["", "  参考", "  " + "-" * 40]
        lines += [f"  {r}" for r in entry.refs]
    lines.append("")
    return "\n".join(lines)


def _wrap(text: str, width: int = 74) -> list[str]:
    """按显示宽度折行：中文按 2 列计，英文单词整体不拆。"""
    if not text:
        return ["—"]
    tokens = re.findall(
        r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]"
        r"|[^\s\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+"
        r"|\s+",
        text,
    )
    lines: list[str] = []
    cur = ""
    cur_w = 0
    for tok in tokens:
        w = sum(2 if ord(c) > 0x2E80 else 1 for c in tok)
        if cur_w + w > width and cur.strip():
            lines.append(cur.rstrip())
            cur, cur_w = "", 0
            if tok.isspace():
                continue
        cur += tok
        cur_w += w
    if cur.strip():
        lines.append(cur.rstrip())
    return lines or ["—"]


def entry_to_dict(entry: Entry, vendors: dict) -> dict:
    vendor = vendors[entry.vendor]
    return {
        "domain": entry.domain,
        "product": entry.product,
        "vendor": vendor.name,
        "vendor_cn": vendor.name_cn,
        "owner": entry.owner or vendor.name,
        "category": entry.category,
        "purpose": entry.purpose,
        "verdict": entry.verdict,
        "scope": entry.scope,
        "rule": entry.effective_rule,
        "impact": entry.impact,
        "confidence": entry.confidence,
        "status": entry.status,
        "tags": entry.tags,
        "notes": entry.notes,
        "refs": entry.refs,
    }


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="查询广告域名档案")
    parser.add_argument("domain", nargs="?", help="域名或关键词，支持模糊匹配")
    parser.add_argument("--vendor", help="按厂商 id 过滤")
    parser.add_argument("--category", help="按分类过滤")
    parser.add_argument("--verdict", help="按判定过滤")
    parser.add_argument("--blockable", action="store_true", help="只看可拦截的条目")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    parser.add_argument("--limit", type=int, default=0, help="最多显示条数")
    args = parser.parse_args()

    vendors, entries = load_all()

    if not any([args.domain, args.vendor, args.category, args.verdict, args.blockable]):
        parser.print_help()
        return 0

    pool = entries
    if args.vendor:
        pool = [e for e in pool if e.vendor == args.vendor]
    if args.category:
        pool = [e for e in pool if e.category == args.category]
    if args.verdict:
        pool = [e for e in pool if e.verdict == args.verdict]
    if args.blockable:
        pool = [e for e in pool if e.is_blockable]

    if args.domain:
        hits = search(pool, args.domain)
        if not hits and not any([args.vendor, args.category, args.verdict]):
            print(f"未收录：{args.domain}")
            print("可以提交 issue 补充，或先用 `--verdict keep` 看看误杀名单。")
            return 1
        pool = hits

    if args.limit:
        pool = pool[: args.limit]

    if args.json:
        print(json.dumps([entry_to_dict(e, vendors) for e in pool],
                         ensure_ascii=False, indent=2))
        return 0

    if not pool:
        print("没有匹配的条目")
        return 1

    # 单条命中 → 详情视图
    if len(pool) == 1:
        print(render_entry(pool[0], vendors))
        return 0

    # 多条命中 → 列表视图
    print(f"\n匹配 {len(pool)} 条：\n")
    print(f"  {'域名':<40}{'判定':<12}{'用途'}")
    print(f"  {'-' * 40}{'-' * 12}{'-' * 30}")
    for e in pool:
        v = VERDICTS.get(e.verdict, (e.verdict, ""))[0]
        print(f"  {e.domain:<40}{v:<12}{e.summary}")
    print("\n  用完整域名再查一次可看详情。\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
