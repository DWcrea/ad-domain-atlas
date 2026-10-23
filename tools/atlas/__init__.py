"""ad-domain-atlas 核心模型：加载、校验、派生字段。

数据全部位于 data/ 目录，本模块不依赖任何第三方库以外的运行时（仅 PyYAML）。
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
VENDOR_FILE = DATA_DIR / "vendors.yaml"
DOMAIN_DIR = DATA_DIR / "domains"

#: 生成规则文件时写进注释的来源地址，改仓库名后记得同步这一行
REPO_URL = "https://github.com/DWcrea/ad-domain-atlas"

# ---------------------------------------------------------------------------
# 枚举
# ---------------------------------------------------------------------------

#: 分类 → (中文名, 说明)
CATEGORIES: dict[str, tuple[str, str]] = {
    "ad-serving": ("广告投放", "广告请求、素材分发、曝光与点击计数"),
    "ad-exchange": ("广告交易", "RTB 竞价、DSP/SSP 交换、程序化交易"),
    "mediation": ("聚合中介", "多家广告网络的聚合调度与瀑布流"),
    "tracking": ("行为追踪", "跨站/跨应用行为采集、用户画像、埋点"),
    "analytics": ("统计分析", "产品分析、留存、漏斗、热图"),
    "attribution": ("安装归因", "渠道归因、深度链接、转化回传"),
    "measurement": ("广告测量", "可见性、品牌提升、第三方监测"),
    "crash": ("崩溃监控", "崩溃、异常、APM 性能上报"),
    "push": ("推送消息", "推送通道、营销自动化触达"),
    "infra": ("基础服务", "CDN、静态资源、设备注册等业务必需能力"),
}

#: 拦截判定 → (中文名, 说明)
VERDICTS: dict[str, tuple[str, str]] = {
    "block": ("直接拦截", "无业务副作用，可整域封禁"),
    "block-cost": ("可拦，有代价", "拦掉后丢失某项数据或功能，但不影响核心使用"),
    "partial": ("部分拦截", "同域混用业务流量，只能按主机名或路径精确拦截"),
    "keep": ("不建议拦截", "属业务基础能力，整域封禁会造成故障"),
}

#: 拦截粒度
SCOPES: dict[str, str] = {
    "apex": "根域及其所有子域（整域通配）",
    "host": "仅该子域（含其下级）",
}

CONFIDENCE: dict[str, str] = {
    "high": "已确认",
    "medium": "较可信",
    "low": "待验证",
}

STATUSES: dict[str, str] = {
    "active": "在用",
    "deprecated": "已停用",
}

#: 常见的二级后缀，用于正确切分主机根域（PSL 精简版）
TWO_LEVEL_TLDS: frozenset[str] = frozenset(
    {
        "com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "ac.cn",
        "co.uk", "org.uk", "ac.uk", "co.jp", "co.kr", "or.kr",
        "com.tw", "com.hk", "com.sg", "com.au", "com.br", "com.mx",
        "com.tr", "com.my", "co.id", "com.vn", "com.ar", "co.za",
    }
)

DOMAIN_RE = re.compile(
    r"^(?=.{4,253}$)"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$"
)

REQUIRED_FIELDS = (
    "domain",
    "product",
    "category",
    "purpose",
    "verdict",
    "scope",
    "impact",
    "confidence",
)


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class Entry:
    domain: str
    product: str
    category: str
    purpose: str
    verdict: str
    scope: str
    impact: str
    confidence: str
    vendor: str = ""
    owner: str = ""
    tags: list[str] = field(default_factory=list)
    status: str = "active"
    notes: str = ""
    refs: list[str] = field(default_factory=list)
    source_file: str = ""
    lineno: int = 0

    # -- 派生字段 ---------------------------------------------------------

    @property
    def rule(self) -> str:
        """AdGuard / ABP 语法规则。"""
        return f"||{self.domain}^"

    @property
    def allow_rule(self) -> str:
        """放行（白名单）规则，用于 keep 档。"""
        return f"@@||{self.domain}^"

    @property
    def effective_rule(self) -> str:
        """按判定给出实际该用的规则。"""
        return self.allow_rule if self.verdict == "keep" else self.rule

    @property
    def summary(self) -> str:
        """purpose 的第一句，用于表格。"""
        text = self.purpose.strip().replace("\n", " ")
        parts = re.split(r"(?<=[。；;])", text, maxsplit=1)
        first = parts[0].strip()
        if len(first) > 90:
            first = first[:88].rstrip("，、 ") + "…"
        return first

    @property
    def is_blockable(self) -> bool:
        return self.verdict in ("block", "block-cost", "partial")

    @property
    def parent_domain(self) -> str:
        if not self.is_subdomain:
            return self.domain
        labels = self.domain.split(".")
        if ".".join(labels[-2:]) in TWO_LEVEL_TLDS:
            return ".".join(labels[-3:])
        return ".".join(labels[-2:])

    @property
    def is_subdomain(self) -> bool:
        labels = self.domain.split(".")
        if len(labels) <= 2:
            return False
        if len(labels) == 3 and ".".join(labels[-2:]) in TWO_LEVEL_TLDS:
            return False
        return True


@dataclass
class Vendor:
    id: str
    name: str
    name_cn: str = ""
    country: str = ""
    website: str = ""
    privacy: str = ""
    note: str = ""
    entries: list[Entry] = field(default_factory=list)

    @property
    def display(self) -> str:
        if self.name_cn and self.name_cn != self.name:
            return f"{self.name}（{self.name_cn}）"
        return self.name

    @property
    def slug(self) -> str:
        return self.id


# ---------------------------------------------------------------------------
# 加载
# ---------------------------------------------------------------------------


class AtlasError(RuntimeError):
    pass


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_vendors(path: Path | None = None) -> dict[str, Vendor]:
    path = path or VENDOR_FILE
    if not path.exists():
        raise AtlasError(f"缺少厂商档案文件：{path}")
    raw = _read_yaml(path) or []
    vendors: dict[str, Vendor] = {}
    for item in raw:
        vid = str(item.get("id", "")).strip()
        if not vid:
            raise AtlasError(f"{path} 中存在缺少 id 的厂商条目")
        if vid in vendors:
            raise AtlasError(f"{path} 中厂商 id 重复：{vid}")
        vendors[vid] = Vendor(
            id=vid,
            name=str(item.get("name", vid)),
            name_cn=str(item.get("name_cn", "") or ""),
            country=str(item.get("country", "") or ""),
            website=str(item.get("website", "") or ""),
            privacy=str(item.get("privacy", "") or ""),
            note=str(item.get("note", "") or ""),
        )
    return vendors


def load_entries(
    domain_dir: Path | None = None,
    vendors: dict[str, Vendor] | None = None,
) -> list[Entry]:
    domain_dir = domain_dir or DOMAIN_DIR
    vendors = vendors if vendors is not None else load_vendors()
    entries: list[Entry] = []

    files = sorted(domain_dir.glob("*.yaml")) + sorted(domain_dir.glob("*.yml"))
    if not files:
        raise AtlasError(f"{domain_dir} 下没有找到任何 yaml 数据文件")

    for path in files:
        raw = _read_yaml(path)
        if raw is None:
            continue
        if not isinstance(raw, dict):
            raise AtlasError(f"{path.name} 顶层必须是映射（vendor / domains）")
        vendor_id = str(raw.get("vendor", "")).strip()
        if not vendor_id:
            raise AtlasError(f"{path.name} 缺少 vendor 字段")
        if vendor_id not in vendors:
            raise AtlasError(f"{path.name} 引用了未登记的厂商 id：{vendor_id}")
        if path.stem != vendor_id:
            raise AtlasError(
                f"{path.name} 文件名应与 vendor id 一致（期望 {vendor_id}.yaml）"
            )

        items = raw.get("domains") or []
        if not isinstance(items, list):
            raise AtlasError(f"{path.name} 的 domains 必须是列表")

        for item in items:
            if not isinstance(item, dict):
                raise AtlasError(f"{path.name} 中存在非映射的域名条目")
            entry = Entry(
                domain=str(item.get("domain", "")).strip().lower(),
                product=str(item.get("product", "")).strip(),
                category=str(item.get("category", "")).strip(),
                purpose=_clean(item.get("purpose", "")),
                verdict=str(item.get("verdict", "")).strip(),
                scope=str(item.get("scope", "")).strip(),
                impact=_clean(item.get("impact", "")),
                confidence=str(item.get("confidence", "")).strip(),
                vendor=vendor_id,
                owner=str(item.get("owner", "") or "").strip(),
                tags=[str(t).strip() for t in (item.get("tags") or []) if str(t).strip()],
                status=str(item.get("status", "active") or "active").strip(),
                notes=_clean(item.get("notes", "")),
                refs=[str(r).strip() for r in (item.get("refs") or []) if str(r).strip()],
                source_file=path.name,
            )
            entries.append(entry)

    # 回填 vendor.entries
    for entry in entries:
        vendors[entry.vendor].entries.append(entry)

    entries.sort(key=lambda e: (e.vendor, e.domain))
    return entries


def _clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    # 折叠 YAML 多行文本中的硬换行
    text = re.sub(r"\s*\n\s*", "", text) if "\n" in text else text
    return unicodedata.normalize("NFC", text)


# ---------------------------------------------------------------------------
# 校验
# ---------------------------------------------------------------------------


def validate(entries: list[Entry], vendors: dict[str, Vendor]) -> list[str]:
    problems: list[str] = []
    seen: dict[str, Entry] = {}

    for e in entries:
        where = f"{e.source_file} :: {e.domain or '<空域名>'}"

        for name in REQUIRED_FIELDS:
            if not getattr(e, name):
                problems.append(f"{where} 缺少必填字段 `{name}`")

        if e.domain:
            if not DOMAIN_RE.match(e.domain):
                problems.append(f"{where} 域名格式非法")
            if "*" in e.domain or "/" in e.domain:
                problems.append(f"{where} 域名中不应包含通配符或路径")
            if e.domain.startswith("www."):
                problems.append(f"{where} 不要录入 www 前缀，请使用主机根域")
            if e.domain in seen:
                other = seen[e.domain]
                problems.append(
                    f"{where} 与 {other.source_file} 重复录入同一域名"
                )
            else:
                seen[e.domain] = e

        if e.category and e.category not in CATEGORIES:
            problems.append(
                f"{where} category 非法：{e.category}（可选 {', '.join(CATEGORIES)}）"
            )
        if e.verdict and e.verdict not in VERDICTS:
            problems.append(
                f"{where} verdict 非法：{e.verdict}（可选 {', '.join(VERDICTS)}）"
            )
        if e.scope and e.scope not in SCOPES:
            problems.append(f"{where} scope 非法：{e.scope}（可选 apex / host）")
        if e.confidence and e.confidence not in CONFIDENCE:
            problems.append(
                f"{where} confidence 非法：{e.confidence}（可选 high / medium / low）"
            )
        if e.status not in STATUSES:
            problems.append(f"{where} status 非法：{e.status}（可选 active / deprecated）")

        # 语义一致性
        if e.scope == "apex" and e.is_subdomain:
            problems.append(
                f"{where} scope=apex 但录入的是子域，请改用 scope=host 或改录主机根域"
            )
        if e.verdict == "keep" and e.category in ("ad-serving", "ad-exchange"):
            problems.append(
                f"{where} verdict=keep 与分类 {e.category} 冲突，若确为业务基础能力请改分类为 infra"
            )
        if e.verdict == "partial" and e.scope != "host":
            problems.append(f"{where} verdict=partial 必须配合 scope=host")
        if e.verdict in ("block-cost", "partial", "keep") and len(e.impact) < 8:
            problems.append(f"{where} verdict={e.verdict} 必须写清 impact（副作用）")
        for ref in e.refs:
            if not ref.startswith(("http://", "https://")):
                problems.append(f"{where} refs 必须是 http(s) 链接：{ref}")

    # 覆盖率提示：登记了子域却没登记其父域，不算错误，但值得提醒
    for e in entries:
        if e.is_subdomain and e.parent_domain not in seen:
            problems.append(
                f"{e.source_file} :: {e.domain} 的子域所属根域 "
                f"{e.parent_domain} 未登记（建议补一条 keep 或 block 说明）"
            )

    for v in vendors.values():
        if not v.entries:
            problems.append(f"厂商 {v.id} 在 vendors.yaml 中登记但没有域名数据")

    return problems


# ---------------------------------------------------------------------------
# 便捷函数
# ---------------------------------------------------------------------------


def load_all() -> tuple[dict[str, Vendor], list[Entry]]:
    vendors = load_vendors()
    entries = load_entries(vendors=vendors)
    return vendors, entries


def search(entries: Iterable[Entry], needle: str) -> list[Entry]:
    """按域名后缀 / 产品名 / 厂商名 / 标签模糊匹配。"""
    needle = needle.strip().lower()
    if not needle:
        return []
    pool = list(entries)

    # 精确域名命中时直接返回，避免正文里提到该域名的其他条目混进来
    exact = [e for e in pool if e.domain == needle]
    if exact:
        return exact

    hits: list[Entry] = []
    for e in pool:
        haystack = " ".join(
            [e.domain, e.product, e.purpose, e.notes, " ".join(e.tags)]
        ).lower()
        if needle in e.domain or needle in haystack:
            hits.append(e)
    # 域名包含匹配优先，其次按层级深度
    hits.sort(key=lambda e: (needle not in e.domain, e.domain.count("."), e.domain))
    return hits


def coverage_of(entry: Entry, blocked: set[str]) -> str:
    """给定规则库域名集合，判断该条目的覆盖状态。"""
    if entry.domain in blocked:
        return "exact"
    if entry.scope == "apex":
        prefix = entry.domain + "."
        if any(d.endswith(prefix) for d in blocked):
            return "children"
    return "none"


def setup_stdio() -> None:
    """在 Windows 控制台强制 UTF-8，避免中文输出炸掉。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except (AttributeError, OSError):
            pass
