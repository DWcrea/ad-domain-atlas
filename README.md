# 广告域名图谱 · Ad Domain Atlas

> 规则库告诉你「拦什么」，这个项目告诉你「拦了会怎样」。

<!-- STATS:START -->
187 个域名 / 19 家厂商 · 可拦 145 · 建议保留 42
<!-- STATS:END -->

**在线浏览**：https://dwcrea.github.io/ad-domain-atlas/ —— 带导航的网页版，手机也能查。

---

## 这是什么

一份可持续维护的广告 / 追踪 / 归因 / 崩溃上报域名档案。每一条记录都回答四个问题：

1. **这个域名是谁的**，具体在干什么活
2. **该不该拦**
3. **拦了会掉什么功能**
4. **该用什么粒度拦**（整域通配，还是只拦某个主机名）

它不是一个规则库。规则库的产出是一张黑名单，本项目的产出是一本说明书，规则文件只是顺带的副产品。

## 为什么值得做

现成的规则库只给结论，不给理由。于是常见的三种翻车方式：

| 翻车方式 | 例子 | 后果 |
| --- | --- | --- |
| 一刀切拦掉统计域 | `\|\|umeng.com^` | 统计没了，**推送也没了**（友盟统计与 U-Push 同域） |
| 只拦主域 | `\|\|pangolin-sdk-toutiao.com^` | 穿山甲自动切到 `-b` / `-toutiao1~4` / `pangolin-x`，广告照旧 |
| 误伤基础设施 | `\|\|googleapis.com^` | Google 登录、Firebase 推送、地图一起失效，App 白屏 |

这个项目想做的就是把「为什么」写下来，让下一次做决定时有据可依。

## 快速开始

```bash
git clone https://github.com/DWcrea/ad-domain-atlas.git
cd ad-domain-atlas
pip install -r requirements.txt

python tools/validate.py        # 校验数据
python tools/build_docs.py      # 生成 docs/ 下的文档
```

### 查一个域名

```bash
python tools/query.py doubleclick.net
```

```text
  doubleclick.net
  =================
  产品  Google Ad Manager / DoubleClick（DFP）
  归属  Google（谷歌）  [Google]
  分类  广告投放  (ad-serving)
  判定  直接拦截  ·  整域通配（含所有子域）
  置信度 已确认

  用途
  ----------------------------------------
  Google 展示广告的核心投放域。ad.doubleclick.net 承载广告素材与点击跳转，
  stats.g.doubleclick.net 负责曝光与点击计数……

  拦截后果
  ----------------------------------------
  网页与 App 内的 Google 系广告位变为空白，广告链接点不开，属预期行为。

  规则
  ----------------------------------------
  ||doubleclick.net^
```

按条件筛选：

```bash
python tools/query.py --vendor google          # 某厂商全部域名
python tools/query.py --verdict keep           # 只看「不建议拦截」
python tools/query.py --category attribution   # 只看安装归因
python tools/query.py appsflyer --json         # 机器可读输出
```

### 导出规则

```bash
python tools/export_rules.py                       # block + block-cost + partial
python tools/export_rules.py --include block       # 只要「放心拦」的部分
python tools/export_rules.py --min-confidence high # 只要已确认的条目
```

产物在 `lists/` 下：

| 文件 | 用途 |
| --- | --- |
| `adguard.txt` | AdGuard / uBlock / ABP 语法，可作自定义过滤器订阅 |
| `hosts.txt` | hosts 格式，供 AdAway、DNS66 等使用 |
| `dnsmasq.conf` | dnsmasq 的 `address=/domain/0.0.0.0` |
| `allowlist.txt` | **放行清单**，`@@` 白名单语法，建议置于所有拦截规则之前 |

#### 直接订阅

AdGuard 里「添加自定义过滤器」填下面这条即可，仓库更新后会自动同步：

```text
https://raw.githubusercontent.com/DWcrea/ad-domain-atlas/main/lists/adguard.txt
```

放行清单同样可以订阅（建议加在所有拦截规则之前）：

```text
https://raw.githubusercontent.com/DWcrea/ad-domain-atlas/main/lists/allowlist.txt
```

### 和现成规则库比一比

```bash
python tools/check_lists.py --list https://big.oisd.nl/ --name "OISD big"
python tools/build_docs.py     # 生成 docs/coverage.md
```

输出会告诉你：这些域名里，规则库已经拦了多少，还剩哪些可拦的漏网。剩下的那部分才是值得自己补的。

### 补充注册信息

```bash
python tools/rdap.py doubleclick.net
python tools/rdap.py --all --sleep 1.5    # 全量查询，注意别把人家 RDAP 打爆
```

判读技巧：注册时间很新、命名却很像正规产品的域名，多半是短命投放域或马甲域。

### 体检别人的规则文件

看到一份来路不明的规则库，先别急着订阅，跑一遍：

```bash
python tools/review_list.py ./someone-blacklist.txt --oisd ./oisd_big.txt
```

它会告诉你四件事：

- 语法构成与拦截粒度（整域多还是子域多）
- 有没有和你库里「不建议拦截」的判定冲突
- 有多少条打到了推送、上传、升级、验证码、配置下发这类业务接口
- 和成熟规则库的重叠度——哪些是重复劳动，哪些是真增量

## 数据长什么样

数据按厂商拆分在 `data/domains/*.yaml`，一条记录长这样：

```yaml
- domain: umeng.com
  product: 友盟+（U-App / U-Push）
  category: analytics
  purpose: 国内使用最广的第三方统计 SDK。同一套域名同时承担统计上报与 U-Push 推送通道。
  verdict: block-cost
  scope: apex
  impact: 统计全丢是必然；如果 App 的推送走友盟，通知会一起收不到。
  confidence: high
  tags: [统计, 推送, 混用]
  notes: 不确定 App 是否用友盟推送时，先只拦统计上报路径，观察一天再决定是否整域。
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `domain` | 是 | 主机根域或具体主机名，小写，不带 `www.`、不带路径 |
| `product` | 是 | 产品 / SDK 名称 |
| `category` | 是 | 十类之一，见下表 |
| `purpose` | 是 | 这个域名到底在干什么，写具体，别写「广告相关」 |
| `verdict` | 是 | 四档判定之一，见下表 |
| `scope` | 是 | `apex` 整域通配 / `host` 仅该主机名 |
| `impact` | 是 | 拦截后的具体后果 |
| `confidence` | 是 | `high` 已确认 / `medium` 较可信 / `low` 待验证 |
| `owner` | 否 | 聚合厂商文件里标注真实归属公司 |
| `status` | 否 | `active`（默认）/ `deprecated` 已停用 |
| `tags` | 否 | 自由标签，便于检索 |
| `notes` | 否 | 判读技巧、注意事项 |
| `refs` | 否 | 参考链接 |

## 判定标准

判定回答的是「**拦了会不会出问题**」，不是「它是不是广告」。很多统计、归因域名属于灰色地带——拦掉不报错，但会丢数据。

| 判定 | 含义 | 典型例子 |
| --- | --- | --- |
| `block` | 直接拦截，无业务副作用 | `doubleclick.net`、`applovin.com` |
| `block-cost` | 可拦，代价是丢数据或丢某个功能 | `app-measurement.com`（丢埋点）、`umeng.com`（丢推送） |
| `partial` | 同域混业务，只能按主机名或路径精确拦 | `graph.facebook.com`（登录与广告归因同域） |
| `keep` | 不建议拦截，属业务基础能力 | `googleapis.com`、`alicdn.com`、`snssdk.com` |

`keep` 这一档最容易被忽略，也最容易出事故。全部 `keep` 条目汇总在 [docs/keep.md](docs/keep.md)，可以直接转成放行规则用。

## 分类

| 分类 | 说明 |
| --- | --- |
| `ad-serving` | 广告投放：请求、素材分发、曝光与点击计数 |
| `ad-exchange` | 广告交易：RTB 竞价、DSP/SSP、程序化交易 |
| `mediation` | 聚合中介：多家广告网络的聚合调度与瀑布流 |
| `tracking` | 行为追踪：跨站/跨应用采集、用户画像、埋点 |
| `analytics` | 统计分析：产品分析、留存、漏斗、热图 |
| `attribution` | 安装归因：渠道归因、深度链接、转化回传 |
| `measurement` | 广告测量：可见性、品牌提升、第三方监测 |
| `crash` | 崩溃监控：崩溃、异常、APM |
| `push` | 推送消息：推送通道、营销自动化触达 |
| `infra` | 基础服务：CDN、静态资源、设备注册等业务必需能力 |

## 文档

| 页面 | 内容 |
| --- | --- |
| [docs/index.md](docs/index.md) | 全量总表，按厂商分组 |
| [docs/categories.md](docs/categories.md) | 按用途分类 |
| [docs/verdicts.md](docs/verdicts.md) | 按拦截判定，含每条的具体后果 |
| [docs/keep.md](docs/keep.md) | 误杀黑名单：这些域名不要拦 |
| [docs/vendors.md](docs/vendors.md) | 厂商索引 |
| [docs/coverage.md](docs/coverage.md) | 与主流规则库的覆盖对比（需先跑 `check_lists.py`） |

## 目录结构

```text
ad-domain-atlas/
├── data/
│   ├── vendors.yaml          # 厂商档案
│   ├── domains/*.yaml        # 域名数据，按厂商拆分
│   └── coverage.json         # 覆盖率报告（生成物）
├── docs/                     # 文档（生成物，勿手改）
├── lists/                    # 规则文件（生成物，勿手改）
├── tools/
│   ├── atlas/                # 核心模型、校验、渲染
│   ├── validate.py           # 数据校验
│   ├── query.py              # 域名查询
│   ├── build_docs.py         # 文档生成
│   ├── export_rules.py       # 规则导出
│   ├── check_lists.py        # 规则库覆盖比对
│   ├── review_list.py        # 第三方规则文件体检
│   └── rdap.py               # RDAP 注册信息
└── .github/workflows/ci.yml  # 校验 + 生成一致性检查
```

## 与现成规则库的关系

不替代，只补充。推荐用法：

1. 订阅一个低误杀的基础规则库（OISD、AdGuard DNS filter 等）
2. 用 `lists/allowlist.txt` 抵消它们的误杀
3. 用 `lists/adguard.txt` 补上它们漏掉的部分

如果发现本项目某条判定与你的实测不符，请开 issue 说明现象——这正是这个项目最需要的输入。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。最短路径：改 `data/domains/*.yaml` → 跑 `python tools/build_docs.py` → 提 PR。

CI 会检查三件事：数据校验通过、`docs/` 与 `lists/` 已重新生成、没有手改生成物。

## 免责声明

本项目记录的是「域名在技术上的用途与拦截影响」，不构成对任何厂商的指控。判定结论基于公开资料、抓包观察与规则库实践，可能存在偏差；所有 `confidence: low` 的条目都明确标注为待验证。

拦截规则请自行评估风险，尤其是 `keep` 档之外的边界条目。因误拦导致的任何问题，本项目不承担责任。

## License

MIT。代码与数据均可自由使用、修改、再分发，保留版权声明即可。见 [LICENSE](LICENSE)。
