"""Markdown 渲染：把结构化数据变成 GitHub 上可读的文档。"""

from __future__ import annotations

from collections import defaultdict

from . import (
    CATEGORIES,
    CONFIDENCE,
    SCOPES,
    STATUSES,
    VERDICTS,
    Entry,
    Vendor,
)

SHORT_VERDICT = {
    "block": "拦截",
    "block-cost": "拦截·代价",
    "partial": "部分",
    "keep": "保留",
}

SHORT_CATEGORY = {k: v[0] for k, v in CATEGORIES.items()}


def cell(text: str) -> str:
    """表格单元格转义。"""
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def vendor_link(vendor: Vendor) -> str:
    return f"[{cell(vendor.name)}](vendors/{vendor.slug}.md)"


def domain_link(entry: Entry, vendor: Vendor) -> str:
    return f"[`{entry.domain}`](vendors/{vendor.slug}.md#{anchor(entry.domain)})"


def anchor(text: str) -> str:
    return text.replace(".", "").replace("_", "-").lower()


def header(title: str, subtitle: str = "") -> str:
    lines = [f"# {title}", ""]
    if subtitle:
        lines += [subtitle, ""]
    return "\n".join(lines)


def legend() -> str:
    rows = ["| 判定 | 含义 |", "| --- | --- |"]
    for key, (label, desc) in VERDICTS.items():
        rows.append(f"| `{SHORT_VERDICT[key]}` | {label}：{desc} |")
    return "\n".join(rows)


def stats_block(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    total = len(entries)
    blockable = sum(1 for e in entries if e.is_blockable)
    keep = sum(1 for e in entries if e.verdict == "keep")
    low = sum(1 for e in entries if e.confidence == "low")
    deprecated = sum(1 for e in entries if e.status == "deprecated")
    return (
        f"> 共 **{total}** 个域名 · **{len(vendors)}** 家厂商 · "
        f"可拦 **{blockable}** · 建议保留 **{keep}** · "
        f"待验证 **{low}** · 已停用 **{deprecated}**"
    )


# ---------------------------------------------------------------------------
# 全量总表
# ---------------------------------------------------------------------------


def render_index(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    out = [
        header(
            "广告域名总表",
            "按厂商分组。点域名可跳到该厂商详情页，查看拦截副作用与证据来源。",
        ),
        stats_block(vendors, entries),
        "",
        legend(),
        "",
        "## 索引",
        "",
        "- [按用途分类](categories.md) · [按拦截判定](verdicts.md) · "
        "[误杀黑名单](keep.md) · [厂商索引](vendors.md)",
        "",
    ]

    by_vendor: dict[str, list[Entry]] = defaultdict(list)
    for e in entries:
        by_vendor[e.vendor].append(e)

    for vid, v in sorted(vendors.items(), key=lambda kv: kv[1].name.lower()):
        items = by_vendor.get(vid, [])
        if not items:
            continue
        out += [f"## {v.display}", "", f"{len(items)} 条 · [厂商详情](vendors/{v.slug}.md)", ""]
        out += [
            "| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for e in sorted(items, key=lambda x: x.domain):
            name = f"`{e.domain}`"
            if e.status == "deprecated":
                name += " (停用)"
            out.append(
                f"| {name} | {cell(e.product)} | {cell(e.summary)} | "
                f"{SHORT_CATEGORY.get(e.category, e.category)} | "
                f"{SHORT_VERDICT.get(e.verdict, e.verdict)} |"
            )
        out.append("")

    out += ["---", "", _footer()]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 按分类
# ---------------------------------------------------------------------------


def render_categories(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    out = [
        header("按用途分类", "同一个域名只归一个主分类。分类说明见下表。"),
        "",
        "| 分类 | 说明 | 数量 |",
        "| --- | --- | --- |",
    ]
    counts = defaultdict(int)
    for e in entries:
        counts[e.category] += 1
    for key, (label, desc) in CATEGORIES.items():
        out.append(f"| {label} (`{key}`) | {desc} | {counts.get(key, 0)} |")
    out.append("")

    for key, (label, desc) in CATEGORIES.items():
        items = [e for e in entries if e.category == key]
        if not items:
            continue
        out += [f"## {label}", "", desc, ""]
        out += [
            "| 域名 | 厂商 | 产品 | 用途 | 判定 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for e in sorted(items, key=lambda x: x.domain):
            v = vendors[e.vendor]
            out.append(
                f"| `{e.domain}` | {cell(v.name)} | {cell(e.product)} | "
                f"{cell(e.summary)} | {SHORT_VERDICT.get(e.verdict, e.verdict)} |"
            )
        out.append("")

    out += ["---", "", _footer()]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 按判定
# ---------------------------------------------------------------------------


def render_verdicts(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    out = [
        header(
            "按拦截判定",
            "判定回答的是「这个域名拦了会不会出问题」，不是「它是不是广告」。"
            "大量统计、归因域名属于灰色地带，拦掉不报错但会丢数据。",
        ),
        "",
        legend(),
        "",
    ]

    order = ["block", "block-cost", "partial", "keep"]
    for key in order:
        label, desc = VERDICTS[key]
        items = [e for e in entries if e.verdict == key]
        if not items:
            continue
        out += [f"## {label}（{len(items)} 条）", "", desc, ""]
        out += [
            "| 域名 | 厂商 | 用途 | 拦截后果 |",
            "| --- | --- | --- | --- |",
        ]
        for e in sorted(items, key=lambda x: (x.vendor, x.domain)):
            out.append(
                f"| `{e.domain}` | {cell(vendors[e.vendor].name)} | "
                f"{cell(e.summary)} | {cell(e.impact)} |"
            )
        out.append("")

    out += ["---", "", _footer()]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 误杀黑名单
# ---------------------------------------------------------------------------


def render_keep(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    items = [e for e in entries if e.verdict == "keep"]
    out = [
        header(
            "误杀黑名单：这些域名不要拦",
            "规则库里混进这些域名，会造成 App 白屏、登录失败、推送收不到、图片加载不出来。"
            "很多「广告拦截后 App 坏了」的报障都出在这里。",
        ),
        "",
        f"共 {len(items)} 条。",
        "",
        "| 域名 | 厂商 | 为什么不能拦 | 拦了会怎样 |",
        "| --- | --- | --- | --- |",
    ]
    for e in sorted(items, key=lambda x: (x.vendor, x.domain)):
        out.append(
            f"| `{e.domain}` | {cell(vendors[e.vendor].name)} | "
            f"{cell(e.summary)} | {cell(e.impact)} |"
        )
    out += [
        "",
        "## 使用建议",
        "",
        "把上表的域名转成放行规则，加在过滤器的**最前面**（AdGuard 的自定义规则里"
        "`@@||domain^` 即白名单），可以抵消上游规则库的误杀：",
        "",
        "```text",
    ]
    for e in sorted(items, key=lambda x: x.domain):
        out.append(f"@@||{e.domain}^")
    out += ["```", "", "---", "", _footer()]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 厂商
# ---------------------------------------------------------------------------


def render_vendor_index(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    out = [
        header("厂商索引", "按厂商归档，便于顺着一条线索把同一家的域名一次摸清。"),
        "",
        "| 厂商 | 国家/地区 | 域名数 | 可拦 | 官网 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for v in sorted(vendors.values(), key=lambda x: x.name.lower()):
        if not v.entries:
            continue
        blockable = sum(1 for e in v.entries if e.is_blockable)
        site = f"[{v.website.split('//')[-1]}]({v.website})" if v.website else "—"
        out.append(
            f"| [{cell(v.display)}](vendors/{v.slug}.md) | {cell(v.country or '—')} | "
            f"{len(v.entries)} | {blockable} | {site} |"
        )
    out += ["", "---", "", _footer()]
    return "\n".join(out)


def render_vendor(vendor: Vendor) -> str:
    out = [
        header(vendor.display, vendor.note),
        "",
        f"- 官网：{vendor.website or '—'}",
        f"- 隐私政策：{vendor.privacy or '—'}",
        f"- 登记域名：{len(vendor.entries)} 条",
        "",
    ]
    for e in sorted(vendor.entries, key=lambda x: x.domain):
        label, _ = VERDICTS.get(e.verdict, (e.verdict, ""))
        out += [
            f"## `{e.domain}`",
            "",
            f"- **产品 / SDK**：{e.product}",
            f"- **分类**：{SHORT_CATEGORY.get(e.category, e.category)}"
            f"（`{e.category}`）",
            f"- **判定**：{label}（`{e.verdict}`）· 粒度：{SCOPES.get(e.scope, e.scope)}",
            f"- **置信度**：{CONFIDENCE.get(e.confidence, e.confidence)}",
        ]
        if e.status != "active":
            out.append(f"- **状态**：{STATUSES.get(e.status, e.status)}")
        if e.tags:
            out.append(f"- **标签**：{'、'.join(e.tags)}")
        out += [
            "",
            "**用途**",
            "",
            e.purpose or "—",
            "",
            "**拦截后果**",
            "",
            e.impact or "—",
            "",
            "**规则**",
            "",
            "```text",
            e.effective_rule,
            "```",
        ]
        if e.notes:
            out += ["", f"> {e.notes}"]
        if e.refs:
            out += ["", "**参考**", ""]
            out += [f"- {r}" for r in e.refs]
        out.append("")

    out += ["---", "", _footer()]
    return "\n".join(out)


def render_vendors_dir(
    vendors: dict[str, Vendor], entries: list[Entry]
) -> dict[str, str]:
    """返回 {相对路径: 内容}，路径相对 docs/。"""
    files: dict[str, str] = {}
    for v in vendors.values():
        if v.entries:
            files[f"vendors/{v.slug}.md"] = render_vendor(v)
    files["vendors.md"] = render_vendor_index(vendors, entries)
    return files


# ---------------------------------------------------------------------------
# 覆盖率报告
# ---------------------------------------------------------------------------


def render_coverage(
    vendors: dict[str, Vendor], entries: list[Entry], coverage: dict
) -> str:
    summary = coverage.get("summary", {})
    lists = coverage.get("lists", [])
    uncovered = coverage.get("uncovered", [])

    out = [
        header(
            "与主流规则库的覆盖对比",
            "回答一个问题：这些域名，现成的规则库到底拦了多少？"
            "没被拦的部分，才是需要自己补规则的地方。",
        ),
        "",
        f"> 生成于 {coverage.get('generated', '—')}",
        "",
        "## 参与比对的规则库",
        "",
        "| 规则库 | 条目数 | 来源 |",
        "| --- | --- | --- |",
    ]
    for item in lists:
        out.append(
            f"| {cell(item.get('name', ''))} | {item.get('entries', 0):,} | "
            f"`{cell(item.get('source', ''))}` |"
        )

    total = summary.get("total", 0)
    exact = summary.get("exact", 0)
    children = summary.get("children", 0)
    none = summary.get("none", 0)
    covered = exact + children
    rate = (covered / total * 100) if total else 0

    out += [
        "",
        "## 总体覆盖",
        "",
        f"- 收录域名：**{total}** 条",
        f"- 被规则库直接命中：**{exact}** 条",
        f"- 仅被上级域规则覆盖：**{children}** 条",
        f"- 完全未覆盖：**{none}** 条",
        f"- 覆盖率：**{rate:.1f}%**",
        "",
        "「仅被上级域覆盖」指规则库只封了某个子域（例如 `||ad.doubleclick.net^`），"
        "而没有封主机根域。这类条目在 DNS 层仍可能漏掉其他子域。",
        "",
    ]

    if uncovered:
        actionable = [
            u for u in uncovered if u.get("verdict") in ("block", "block-cost")
        ]
        intentional = len(uncovered) - len(actionable)
        out += [
            f"## 规则库漏掉的可拦域名（{len(actionable)} 条）",
            "",
            "这些条目判定为可拦，但上面参与比对的规则库里没有对应规则。"
            "把它们补进自己的规则集，效果会立竿见影。",
            "",
            "| 域名 | 厂商 | 判定 | 用途 |",
            "| --- | --- | --- | --- |",
        ]
        for item in actionable:
            out.append(
                f"| `{item['domain']}` | {cell(item.get('vendor', ''))} | "
                f"{SHORT_VERDICT.get(item.get('verdict', ''), item.get('verdict', ''))} | "
                f"{cell(item.get('summary', ''))} |"
            )
        out.append("")
        if intentional:
            out += [
                f"另有 {intentional} 条「不建议拦截」的域名本来就不该出现在规则库里，"
                "未计入上表。它们见 [误杀黑名单](keep.md)。",
                "",
            ]

    out += ["---", "", _footer()]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 统计注入 README
# ---------------------------------------------------------------------------


def _footer() -> str:
    return (
        "> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。\n"
        "> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。"
    )


def readme_stats(vendors: dict[str, Vendor], entries: list[Entry]) -> str:
    total = len(entries)
    blockable = sum(1 for e in entries if e.is_blockable)
    keep = sum(1 for e in entries if e.verdict == "keep")
    return (
        f"{total} 个域名 / {len(vendors)} 家厂商 · "
        f"可拦 {blockable} · 建议保留 {keep}"
    )
