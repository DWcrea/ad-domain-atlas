#!/usr/bin/env python3
"""体检一份第三方 AdGuard / ABP 规则文件。

回答四个问题：
  1. 这份规则长什么样（规模、语法、结构）
  2. 它和本库的判定有没有冲突（拦了本库认为不该拦的）
  3. 有没有打到业务接口（推送、登录、升级、验证码、配置下发）
  4. 和成熟规则库的重叠度（哪些是重复劳动，哪些是真增量）

用法：
    python tools/review_list.py ./someone-blacklist.txt
    python tools/review_list.py https://example.com/black.txt
    python tools/review_list.py ./list.txt --oisd ./oisd_big.txt --json /tmp/review.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import CATEGORIES, ROOT, TWO_LEVEL_TLDS, load_all, setup_stdio  # noqa: E402

# 主机名里出现这些词，通常意味着「这是业务接口，不是广告」
# 第二个元素：True 表示出现在任意层级都算命中（如 access1.tpns.tencent.com），
#             False 表示只在第一段命中（避免 api 这种泛词到处误报）
RISK_WORDS: dict[str, tuple[str, str, bool]] = {
    "push": ("推送", "拦掉收不到通知", True),
    "tpns": ("推送", "腾讯移动推送通道", True),
    "jpush": ("推送", "极光推送通道", True),
    "getui": ("推送", "个推通道", True),
    "passport": ("登录", "账号登录入口", True),
    "login": ("登录", "账号登录入口", True),
    "oauth": ("登录", "第三方登录回调", True),
    "sso": ("登录", "单点登录", True),
    "pay": ("支付", "支付与订单", True),
    "cashier": ("支付", "收银台", True),
    "sms": ("短信", "验证码短信", True),
    "vcode": ("验证码", "图形/短信验证码", True),
    "captcha": ("验证码", "人机验证", True),
    "upgrade": ("升级", "系统/应用更新", True),
    "update": ("升级", "系统/应用更新", True),
    "ota": ("升级", "固件 OTA", True),
    "upload": ("上传", "用户内容上传", True),
    "verify": ("验证", "身份或设备校验", False),
    "config": ("配置下发", "功能开关与远端配置", False),
    "abtest": ("AB 实验", "灰度与实验分组", False),
    "settings": ("设置同步", "用户设置同步", False),
    "gateway": ("网关", "业务统一入口", False),
    "api": ("业务接口", "通用业务 API", False),
}

SYNTAX_ORDER = [
    "域名 ||x^",
    "通配 ||*x^",
    "路径/修饰符",
    "白名单 @@",
    "元素隐藏 ##",
    "正则 /…/",
    "其它",
]


def registrable(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_LEVEL_TLDS:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def read_source(src: str) -> str:
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(
            src, headers={"User-Agent": "ad-domain-atlas/1.0 (+list review)"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8", errors="replace")
    return Path(src).read_text(encoding="utf-8", errors="replace")


def strip_host(rule: str) -> str:
    body = rule[2:] if rule.startswith("||") else rule
    cut = len(body)
    for sep in ("^", "$", "/", "|"):
        i = body.find(sep)
        if i != -1:
            cut = min(cut, i)
    return body[:cut].lower()


def parse(text: str) -> dict:
    comments: list[str] = []
    syntax: Counter = Counter()
    hosts: list[str] = []
    wildcards: list[str] = []
    specials: list[str] = []
    exceptions: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("!", "#")):
            comments.append(line)
            continue
        if line.startswith("@@"):
            syntax["白名单 @@"] += 1
            exceptions.append(line)
        elif "##" in line or "#@#" in line or "#?#" in line:
            syntax["元素隐藏 ##"] += 1
        elif line.startswith("/") and line.endswith("/"):
            syntax["正则 /…/"] += 1
        elif line.startswith("||"):
            host = strip_host(line)
            if "*" in host:
                syntax["通配 ||*x^"] += 1
                wildcards.append(line)
            else:
                syntax["域名 ||x^"] += 1
                hosts.append(host)
            if any(ch in line for ch in ("$", "/")):
                specials.append(line)
        else:
            syntax["其它"] += 1
            specials.append(line)

    return {
        "comments": comments,
        "syntax": syntax,
        "hosts": hosts,
        "wildcards": wildcards,
        "specials": specials,
        "exceptions": exceptions,
    }


def load_oisd(path: Path) -> set[str]:
    blocked: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("||"):
            host = strip_host(line)
            if host and "*" not in host:
                blocked.add(host)
    return blocked


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="体检第三方规则文件")
    parser.add_argument("source", help="规则文件路径或 URL")
    parser.add_argument("--oisd", help="对照用的成熟规则库（ABP 格式）")
    parser.add_argument("--json", help="把结果写成 JSON")
    parser.add_argument("--top", type=int, default=15, help="根域排行榜长度")
    args = parser.parse_args()

    text = read_source(args.source)
    data = parse(text)
    hosts = data["hosts"]
    syntax: Counter = data["syntax"]

    vendors, entries = load_all()
    by_domain = {e.domain: e for e in entries}

    total_rules = sum(syntax.values())
    bases = Counter(registrable(h) for h in hosts)
    apex_count = sum(1 for h in hosts if registrable(h) == h)

    print("=" * 74)
    print(f"规则文件体检：{args.source}")
    print("=" * 74)

    print("\n【1】基本信息")
    for c in data["comments"][:8]:
        print("   " + c)
    print(f"   有效规则 {total_rules} 条 · 去重根域 {len(bases)} 个")

    print("\n【2】语法构成")
    for key in SYNTAX_ORDER:
        n = syntax.get(key, 0)
        if n:
            print(f"   {key:<14}{n:>6} 条  ({n / total_rules * 100:5.1f}%)")

    print("\n【3】拦截粒度")
    print(f"   整域（如 example.com）      {apex_count:>5} 条")
    print(f"   具体子域（如 api.example.com）{len(hosts) - apex_count:>5} 条")
    print(f"   通配规则                    {len(data['wildcards']):>5} 条")
    if apex_count > len(hosts) * 0.2:
        print("   提示：整域规则占比偏高，误伤面通常也更大。")

    print(f"\n【4】根域排行（前 {args.top}）")
    for base, n in bases.most_common(args.top):
        print(f"   {base:<36}{n:>4} 条")

    # ---- 与本库冲突 ----
    hits = [h for h in hosts if h in by_domain]
    print("\n【5】与本库判定的冲突")
    print(f"   命中本库已收录域名 {len(hits)} 条")
    conflicts = [by_domain[h] for h in hits if by_domain[h].verdict == "keep"]
    partials = [by_domain[h] for h in hits if by_domain[h].verdict == "partial"]
    if conflicts:
        print(f"\n   ⚠ 本库判定「不建议拦截」，却被这份规则整域封了（{len(conflicts)} 条）：")
        for e in sorted(conflicts, key=lambda x: x.domain):
            print(f"     {e.domain:<32}{e.impact[:40]}")
    if partials:
        print(f"\n   ⚠ 本库判定「只能部分拦截」（{len(partials)} 条）：")
        for e in partials:
            print(f"     {e.domain:<32}{e.impact[:40]}")
    if not conflicts and not partials:
        print("   未发现冲突。")

    # ---- 业务接口命中 ----
    print("\n【6】业务接口命中扫描")
    buckets: dict[str, list[str]] = defaultdict(list)
    for h in hosts:
        labels = h.split(".")
        base = registrable(h)
        matched = None
        for idx, label in enumerate(labels):
            # 跳过根域后缀本身（com / cn / com.cn）
            if ".".join(labels[idx:]) == base and idx > 0:
                break
            for kw, (label_cn, _why, any_label) in RISK_WORDS.items():
                if not (idx == 0 or any_label):
                    continue
                if label == kw or label.startswith(kw + "-") or label.endswith("-" + kw) or label.startswith(kw):
                    matched = label_cn
                    break
            if matched:
                break
        if matched:
            buckets[matched].append(h)
    if buckets:
        for label, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
            print(f"   {label:<8}{len(items):>4} 条   例：{', '.join(items[:3])}")
        print("\n   说明：命中关键词不等于一定误伤，但每一条都值得单独确认。")
    else:
        print("   未命中。")

    # ---- 与成熟规则库重叠 ----
    overlap = None
    if args.oisd:
        oisd = load_oisd(Path(args.oisd))
        dup = [h for h in hosts if h in oisd]
        only = [h for h in hosts if h not in oisd]
        overlap = {
            "compared_with": args.oisd,
            "duplicate": len(dup),
            "unique": len(only),
            "duplicate_examples": dup[:20],
            "unique_examples": only[:20],
        }
        print("\n【7】与成熟规则库的重叠")
        print(f"   对照库已收录 {len(dup)} 条（{len(dup) / len(hosts) * 100:.1f}%）")
        print(f"   仅本文件收录 {len(only)} 条")
        print("   增量示例：" + "、".join(only[:10]))

    if args.json:
        payload = {
            "source": args.source,
            "rules": total_rules,
            "syntax": dict(syntax),
            "hosts": len(hosts),
            "apex": apex_count,
            "registrable_domains": len(bases),
            "top_bases": bases.most_common(args.top),
            "conflicts_keep": [e.domain for e in conflicts],
            "conflicts_partial": [e.domain for e in partials],
            "risk_buckets": {k: v for k, v in buckets.items()},
            "overlap": overlap,
        }
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
        )
        print(f"\n结果已写入 {args.json}")

    print("\n" + "=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
