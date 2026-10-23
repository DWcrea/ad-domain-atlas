#!/usr/bin/env python3
"""校验 data/ 目录下的全部域名数据。

用法：
    python tools/validate.py
    python tools/validate.py --quiet     # 只输出结论
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import AtlasError, load_all, setup_stdio, validate  # noqa: E402


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="校验广告域名数据库")
    parser.add_argument("--quiet", action="store_true", help="仅输出结论")
    args = parser.parse_args()

    try:
        vendors, entries = load_all()
    except AtlasError as exc:
        print(f"加载失败：{exc}", file=sys.stderr)
        return 2

    problems = validate(entries, vendors)

    if not args.quiet:
        print(f"厂商 {len(vendors)} 家 / 域名 {len(entries)} 条")

    if problems:
        print(f"\n发现 {len(problems)} 个问题：\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    if not args.quiet:
        by_verdict: dict[str, int] = {}
        for e in entries:
            by_verdict[e.verdict] = by_verdict.get(e.verdict, 0) + 1
        detail = " · ".join(f"{k}={v}" for k, v in sorted(by_verdict.items()))
        print(f"判定分布：{detail}")
    print("校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
