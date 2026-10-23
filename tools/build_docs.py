#!/usr/bin/env python3
"""从 data/ 生成 docs/ 下的全部 Markdown 文档，并回填 README 的统计行。

用法：
    python tools/build_docs.py
    python tools/build_docs.py --check    # 只检查是否有文件过期，不写盘
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import ROOT, load_all, setup_stdio, validate  # noqa: E402
from atlas import render  # noqa: E402

DOCS = ROOT / "docs"
README = ROOT / "README.md"
COVERAGE = ROOT / "data" / "coverage.json"

STATS_START = "<!-- STATS:START -->"
STATS_END = "<!-- STATS:END -->"


def build() -> dict[Path, str]:
    vendors, entries = load_all()

    problems = validate(entries, vendors)
    if problems:
        print("数据校验未通过，先修数据再生成文档：", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    files: dict[Path, str] = {
        DOCS / "index.md": render.render_index(vendors, entries),
        DOCS / "categories.md": render.render_categories(vendors, entries),
        DOCS / "verdicts.md": render.render_verdicts(vendors, entries),
        DOCS / "keep.md": render.render_keep(vendors, entries),
    }

    for rel, text in render.render_vendors_dir(vendors, entries).items():
        files[DOCS / rel] = text

    if COVERAGE.exists():
        coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        files[DOCS / "coverage.md"] = render.render_coverage(vendors, entries, coverage)

    if README.exists():
        text = README.read_text(encoding="utf-8")
        stats = render.readme_stats(vendors, entries)
        new_text = _inject(text, stats)
        if new_text != text:
            files[README] = new_text

    return files


def _inject(text: str, stats: str) -> str:
    if STATS_START not in text or STATS_END not in text:
        return text
    head, rest = text.split(STATS_START, 1)
    _, tail = rest.split(STATS_END, 1)
    return f"{head}{STATS_START}\n{stats}\n{STATS_END}{tail}"


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="生成文档")
    parser.add_argument("--check", action="store_true", help="只检查是否过期")
    args = parser.parse_args()

    files = build()

    stale: list[Path] = []
    for path, content in files.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != content:
            stale.append(path)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")

    # 清理已经没有对应数据的厂商页
    expected = {p for p in files if p.parent.name == "vendors"}
    for old in (DOCS / "vendors").glob("*.md"):
        if old not in expected:
            stale.append(old)
            if not args.check:
                old.unlink()

    if args.check:
        if stale:
            print("以下文件已过期，请运行 `python tools/build_docs.py`：", file=sys.stderr)
            for p in sorted(stale):
                print(f"  - {p.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("文档均为最新")
        return 0

    print(f"已更新 {len(stale)} 个文件，共 {len(files)} 个文档")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
