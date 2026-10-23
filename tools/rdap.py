#!/usr/bin/env python3
"""查询域名的注册信息（RDAP），用于补充「这域名是谁注册的、什么时候注册的」。

用法：
    python tools/rdap.py doubleclick.net
    python tools/rdap.py --all --cache data/rdap.json
    python tools/rdap.py umeng.com --json

判读技巧：
    - 注册时间很晚（近两三年）而产品名听起来很正规，多半是马甲域或短命投放域。
    - 注册商是隐私保护代理，且没有企业信息，属于正常现象，不代表恶意。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import ROOT, load_all, setup_stdio  # noqa: E402

BOOTSTRAP = "https://rdap.org/domain/{}"
CACHE_PATH = ROOT / "data" / "rdap.json"

EVENT_LABELS = {
    "registration": "注册",
    "expiration": "到期",
    "last changed": "变更",
    "last update of RDAP database": "库更新",
}


def fetch(domain: str, timeout: int = 20) -> dict | None:
    req = urllib.request.Request(
        BOOTSTRAP.format(domain),
        headers={
            "User-Agent": "ad-domain-atlas/1.0 (+rdap)",
            "Accept": "application/rdap+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError):
        return None


def summarize(domain: str, data: dict) -> dict:
    events = {}
    for ev in data.get("events", []) or []:
        action = str(ev.get("eventAction", "")).lower()
        if action in EVENT_LABELS:
            events[EVENT_LABELS[action]] = str(ev.get("eventDate", ""))[:10]

    registrar = ""
    for ent in data.get("entities", []) or []:
        roles = [r.lower() for r in ent.get("roles", []) or []]
        if "registrar" not in roles:
            continue
        vcard = ent.get("vcardArray") or []
        if len(vcard) > 1:
            for item in vcard[1]:
                if item and item[0] == "fn":
                    registrar = str(item[3])
                    break
        if not registrar:
            registrar = ent.get("handle", "")
        break

    return {
        "domain": domain,
        "registrar": registrar,
        "created": events.get("注册", ""),
        "expires": events.get("到期", ""),
        "updated": events.get("变更", ""),
        "status": ", ".join(data.get("status", []) or [])[:120],
        "nameservers": [
            str(ns.get("ldhName", "")).lower() for ns in data.get("nameservers", []) or []
        ][:4],
    }


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="RDAP 域名注册信息查询")
    parser.add_argument("domain", nargs="*", help="要查询的域名，可多个")
    parser.add_argument("--all", action="store_true", help="查询库中全部域名")
    parser.add_argument("--cache", default=str(CACHE_PATH), help="缓存文件路径")
    parser.add_argument("--refresh", action="store_true", help="忽略缓存重新查询")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    parser.add_argument("--sleep", type=float, default=1.0, help="请求间隔秒数")
    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        return 0

    cache_path = Path(args.cache)
    cache: dict = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except ValueError:
            cache = {}

    if args.all:
        _, entries = load_all()
        targets = sorted({e.domain for e in entries})
    else:
        targets = [d.strip().lower() for d in args.domain]

    results = []
    for i, domain in enumerate(targets):
        cached = cache.get(domain)
        if cached and not args.refresh:
            results.append(cached)
            continue
        data = fetch(domain)
        if data is None:
            info = {"domain": domain, "error": "查询失败或该后缀不支持 RDAP"}
        else:
            info = summarize(domain, data)
            info["fetched"] = date.today().isoformat()
        cache[domain] = info
        results.append(info)
        if args.all and i < len(targets) - 1:
            time.sleep(args.sleep)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    print()
    print(f"  {'域名':<36}{'注册':<13}{'到期':<13}{'注册商'}")
    print(f"  {'-' * 36}{'-' * 13}{'-' * 13}{'-' * 24}")
    for r in results:
        if r.get("error"):
            print(f"  {r['domain']:<36}{'—':<13}{'—':<13}{r['error']}")
            continue
        print(
            f"  {r['domain']:<36}{r.get('created') or '—':<13}"
            f"{r.get('expires') or '—':<13}{r.get('registrar') or '—'}"
        )
    print(f"\n缓存已写入 {cache_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
