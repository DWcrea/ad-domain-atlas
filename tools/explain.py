#!/usr/bin/env python3
"""给一个陌生域名做体检：它是什么、谁在托管、拦了会怎样。

用在两种场景：
  1. 规则库里看到一条不认识的域名，想知道该不该留
  2. 抓包看到一个陌生请求，想知道是谁发的

用法：
    python tools/explain.py mars.jd.com --list ../anti-ad.txt
    python tools/explain.py tnc3-bjlgy.snssdk.com --list a.txt --list b.txt
    python tools/explain.py example.com --no-net          # 只查库，不联网

判断依据全部打印出来，不替你下结论——结论写在最后一段「提示」里，仅供参考。
"""

from __future__ import annotations

import argparse
import random
import socket
import ssl
import struct
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas import TWO_LEVEL_TLDS, load_all, setup_stdio  # noqa: E402

DEFAULT_DNS = "223.5.5.5"
CDN_HINTS = {
    "cdngslb.com": "腾讯云 CDN 调度",
    "alicdn.com": "阿里云 CDN",
    "kunlun.com": "阿里云 CDN",
    "cloudfront.net": "AWS CloudFront",
    "akamai.net": "Akamai",
    "akamaiedge.net": "Akamai",
    "edgekey.net": "Akamai",
    "fastly.net": "Fastly",
    "cdn77.org": "CDN77",
    "wscloudcdn.com": "网宿",
    "chinacache.com": "蓝汛",
    "lxdns.com": "帝联",
    "cdntip.com": "腾讯云 CDN",
    "tbcache.com": "阿里 CDN",
    "sched.qq.com": "腾讯调度",
}
API_SERVERS = {"jfe", "openresty", "nginx", "tengine", "envoy", "istio-envoy"}


# ---------------------------------------------------------------------------
# 极简 DNS 客户端（避免依赖 dig / nslookup，跨平台可用）
# ---------------------------------------------------------------------------


def _read_name(buf: bytes, off: int) -> tuple[str, int]:
    parts: list[str] = []
    next_off: int | None = None
    guard = 0
    while off < len(buf) and guard < 128:
        guard += 1
        ln = buf[off]
        if ln == 0:
            off += 1
            if next_off is None:
                next_off = off
            break
        if ln & 0xC0 == 0xC0:
            ptr = ((ln & 0x3F) << 8) | buf[off + 1]
            if next_off is None:
                next_off = off + 2
            off = ptr
            continue
        off += 1
        parts.append(buf[off : off + ln].decode("ascii", "ignore"))
        off += ln
    return ".".join(parts), (next_off if next_off is not None else off)


def dns_query(
    name: str, qtype: int, server: str, timeout: float = 3.0
) -> list[tuple[int, str]]:
    """返回 [(记录类型, 值)]，类型 1=A、5=CNAME。"""
    tid = random.randint(0, 0xFFFF)
    header = struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0)
    qname = b"".join(
        bytes([len(p)]) + p.encode("ascii", "ignore")
        for p in name.rstrip(".").split(".")
        if p
    ) + b"\x00"
    packet = header + qname + struct.pack("!HH", qtype, 1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(packet, (server, 53))
        data, _ = sock.recvfrom(4096)
    except OSError:
        return []
    finally:
        sock.close()

    if len(data) < 12:
        return []
    ancount = struct.unpack("!H", data[6:8])[0]
    off = 12
    _, off = _read_name(data, off)
    off += 4  # qtype + qclass

    out: list[tuple[int, str]] = []
    for _ in range(ancount):
        _, off = _read_name(data, off)
        if off + 10 > len(data):
            break
        rtype, _rclass, _ttl, rdlen = struct.unpack("!HHIH", data[off : off + 10])
        off += 10
        rdata = data[off : off + rdlen]
        off += rdlen
        if rtype == 5:
            out.append((5, _read_name(data, off - rdlen)[0]))
        elif rtype == 1 and rdlen == 4:
            out.append((1, ".".join(str(b) for b in rdata)))
    return out


def cname_chain(name: str, server: str, depth: int = 6) -> list[str]:
    chain: list[str] = []
    cur = name
    for _ in range(depth):
        targets = [v for t, v in dns_query(cur, 5, server) if t == 5]
        if not targets:
            break
        cur = targets[0]
        chain.append(cur)
    return chain


def a_records(name: str, server: str) -> list[str]:
    return [v for t, v in dns_query(name, 1, server) if t == 1]


# ---------------------------------------------------------------------------
# HTTP 指纹
# ---------------------------------------------------------------------------


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """不跟随跳转，把 3xx 与 Location 原样暴露出来。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def http_probe(domain: str, timeout: float = 8.0) -> dict:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    opener = urllib.request.build_opener(
        _NoRedirect, urllib.request.HTTPSHandler(context=ctx)
    )
    last = ""
    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}/"
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "User-Agent": "Mozilla/5.0 (ad-domain-atlas explain)",
                "Accept": "*/*",
            },
        )
        try:
            with opener.open(req, timeout=timeout) as resp:
                return {
                    "url": url,
                    "status": resp.status,
                    "headers": dict(resp.headers.items()),
                    "body": resp.read(600).decode("utf-8", "replace"),
                }
        except urllib.error.HTTPError as exc:
            return {
                "url": url,
                "status": exc.code,
                "headers": dict(exc.headers.items()) if exc.headers else {},
                "body": exc.read(600).decode("utf-8", "replace"),
            }
        except Exception as exc:  # noqa: BLE001
            last = f"{type(exc).__name__}: {exc}"
    return {"url": domain, "status": None, "headers": {}, "body": "", "error": last}


# ---------------------------------------------------------------------------
# 规则库
# ---------------------------------------------------------------------------


def load_list(path: str) -> set[str]:
    out: set[str] = set()
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s.startswith("||"):
            continue
        body = s[2:]
        for sep in ("^", "$", "/"):
            i = body.find(sep)
            if i != -1:
                body = body[:i]
        if body and "*" not in body:
            out.add(body.lower())
    return out


def registrable(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_LEVEL_TLDS:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


# ---------------------------------------------------------------------------


def main() -> int:
    setup_stdio()
    parser = argparse.ArgumentParser(description="域名体检")
    parser.add_argument("domain", help="要查的域名")
    parser.add_argument("--list", action="append", default=[], help="规则库路径，可重复")
    parser.add_argument("--dns", default=DEFAULT_DNS, help=f"DNS 服务器，默认 {DEFAULT_DNS}")
    parser.add_argument("--no-net", action="store_true", help="跳过 DNS 与 HTTP 探测")
    args = parser.parse_args()

    domain = args.domain.strip().lower().rstrip(".")
    root = registrable(domain)

    print("=" * 74)
    print(f"域名体检：{domain}")
    print("=" * 74)

    # ---- 1. 本库 ----
    vendors, entries = load_all()
    by_domain = {e.domain: e for e in entries}
    print("\n【1】ad-domain-atlas")
    if domain in by_domain:
        e = by_domain[domain]
        print(f"   已收录：{e.product}（{vendors[e.vendor].name}）")
        print(f"   判定：{e.verdict} · {e.impact}")
    else:
        parents = [d for d in by_domain if domain.endswith("." + d)]
        parents.sort(key=len, reverse=True)
        if parents:
            e = by_domain[parents[0]]
            print(f"   未直接收录，但父域 {parents[0]} 已收录：{e.product}")
            print(f"   父域判定：{e.verdict}（{e.impact[:40]}…）")
            print("   注意：父域判定不能直接套到子域上——同一根域下常常广告与业务并存。")
        else:
            print(f"   未收录（根域 {root} 也不在库里）")

    # ---- 2. 规则库 ----
    print("\n【2】规则库收录情况")
    if not args.list:
        print("   未指定 --list，跳过")
    else:
        for path in args.list:
            try:
                rules = load_list(path)
            except OSError as exc:
                print(f"   {path}：读取失败（{exc}）")
                continue
            hit = "命中" if domain in rules else "未命中"
            siblings = sorted(r for r in rules if registrable(r) == root and r != domain)
            print(f"   {Path(path).name}：{hit}（该库共 {len(rules):,} 条）")
            if siblings:
                print(f"      同根域下另有 {len(siblings)} 条被收录：")
                for s in siblings[:12]:
                    print(f"        {s}")
                if len(siblings) > 12:
                    print(f"        … 另有 {len(siblings) - 12} 条")

    # ---- 3. DNS ----
    print("\n【3】DNS")
    ips: list[str] = []
    chain: list[str] = []
    if args.no_net:
        print("   --no-net，跳过")
    else:
        chain = cname_chain(domain, args.dns)
        ips = a_records(domain, args.dns)
        if chain:
            print("   CNAME 链：" + " → ".join(chain))
            for target in chain:
                for suffix, label in CDN_HINTS.items():
                    if target.endswith(suffix):
                        print(f"   → 指向 {label}")
                        break
        if ips:
            print("   A 记录：" + "、".join(ips[:6]))
        if not chain and not ips:
            print("   解析失败（可能已停用，或根域本身没有 A 记录）")

    # ---- 4. HTTP ----
    print("\n【4】HTTP 指纹")
    probe: dict = {}
    if args.no_net:
        print("   --no-net，跳过")
    else:
        probe = http_probe(domain)
        if probe.get("status") is None:
            print(f"   请求失败：{probe.get('error', '未知')}")
        else:
            print(f"   {probe['url']} → HTTP {probe['status']}")
            h = {k.lower(): v for k, v in probe.get("headers", {}).items()}
            for key in ("server", "location", "content-type", "via", "x-cache"):
                if key in h:
                    print(f"   {key}: {h[key]}")
            for key in h:
                if key.startswith(("x-tt-", "x-alicdn", "cf-ray", "x-served-by", "x-amz")):
                    print(f"   {key}: {h[key][:70]}")
            if "access-control-allow-origin" in h:
                print(f"   access-control-allow-origin: {h['access-control-allow-origin']}")
            body = probe.get("body", "").strip().replace("\n", " ")[:120]
            if body:
                print(f"   响应片段：{body}")

    # ---- 5. 提示 ----
    print("\n【5】提示（仅供参考，最终靠自己验证）")
    hints: list[str] = []
    if probe.get("status"):
        h = {k.lower(): v for k, v in probe.get("headers", {}).items()}
        server = h.get("server", "").lower()
        if any(t in chain for t in []) or any(
            any(t.endswith(sfx) for sfx in CDN_HINTS) for t in chain
        ):
            hints.append("CNAME 指向 CDN：多半是静态资源或加速回源节点，拦了可能白图/接口变慢")
        if "cdn-cache" in str(h.get("x-tt-trace-tag", "")) or "via" in h:
            hints.append("响应头带 CDN 缓存标记：这是分发节点，不是业务域名本身")
        if server in API_SERVERS and h.get("access-control-allow-origin"):
            hints.append("返回 CORS 开放头：这是给浏览器 JS 调用的接口域，不是页面")
        if h.get("location"):
            hints.append(f"根路径跳转到 {h['location']}：说明它本身不提供页面内容")
    if not hints:
        hints.append("证据不足以判断用途，建议抓包看它返回什么内容再决定")
    for h in hints:
        print("   - " + h)

    print("\n" + "=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
