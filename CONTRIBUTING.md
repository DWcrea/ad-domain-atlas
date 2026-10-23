# 贡献指南

这个项目的价值全部在数据质量上。一条错误的判定，可能让人把 App 拦成白屏。所以下面这些要求看着啰嗦，但都是踩过坑总结出来的。

## 最快路径

```bash
git clone https://github.com/your-name/ad-domain-atlas.git
cd ad-domain-atlas
pip install -r requirements.txt

# 1. 改数据
#    data/domains/<厂商>.yaml

# 2. 校验
python tools/validate.py

# 3. 重新生成文档与规则（CI 会检查生成物是否同步）
python tools/build_docs.py
python tools/export_rules.py

# 4. 提 PR
```

## 新增一条域名

1. 先确认不是重复：`python tools/query.py <域名>`
2. 找到对应厂商文件。没有就新建 `data/domains/<vendor-id>.yaml`，并在 `data/vendors.yaml` 里登记同 id 的厂商条目（文件名必须与 id 一致）
3. 按下面的模板填写
4. 跑校验，跑生成

```yaml
- domain: example-ads.com
  product: 产品名 / SDK 名
  category: ad-serving
  purpose: 这个域名收到什么请求、返回什么、由谁调用。写具体，不要写「广告相关」。
  verdict: block
  scope: apex
  impact: 拦掉之后具体会怎样。
  confidence: high
  tags: [标签1, 标签2]
```

## 判定怎么给

判定回答的是「拦了会不会出问题」，不是「它是不是广告」。按这个顺序问自己：

| 问题 | 如果答案是「是」 |
| --- | --- |
| 拦掉之后，App 的核心功能会不会坏？ | `keep` |
| 拦掉之后，会不会丢推送、登录、支付、验证码？ | `keep` 或 `block-cost` |
| 拦掉之后，只是丢统计、丢归因、丢崩溃上报？ | `block-cost` |
| 同一主机名下既有广告又有业务接口？ | `partial` + `scope: host` |
| 就是个纯广告域，拦了一点事没有？ | `block` |

**几个硬规矩：**

- 拿不准就标 `confidence: medium`，完全没验证过标 `low`，并在 `notes` 里写清依据。**宁可标待验证，也不要编。**
- `scope: apex` 只用于「整域都是广告」的情况。同域下有业务接口的，一律 `scope: host`。
- 录了子域，就要把它的主机根域也录一条（哪怕判定是 `keep`）。校验器会提醒你。
- 别录 `www.` 前缀，别录路径，别录通配符。通配交给 `scope: apex` 表达。

## 怎么验证

不要求你有抓包环境，但至少要给出依据。可接受的做法：

- **抓包**：AdGuard 的过滤日志、Charles / mitmproxy、浏览器 DevTools 的 Network 面板。最可靠。
- **SDK 文档**：厂商官方文档里列出的 endpoint，贴链接到 `refs`。
- **规则库交叉印证**：OISD、anti-AD、AdGuard DNS filter 里对该域的收录情况。只能证明「别人也认为它是广告」，不能证明用途。
- **DNS 查询**：`dig` 看 CNAME 指向，能反推托管方。

`refs` 里放能支撑你判定的链接，别放搜索引擎结果页。

## 遇到陌生域名怎么办

这是最常卡住的一步。抓包或规则库里看到一个没见过的域名，先按下面的顺序走一遍，五分钟内能定性。

### 第一步：跑工具

```bash
python tools/explain.py 域名 --list ./anti-ad.txt
```

它会一次性给出四样东西：库里有没有（含父域继承）、同根域下这个规则库还封了哪些、CNAME 链指向谁、HTTP 响应头长什么样。下面几条判断都基于它的输出。

### 第二步：四个快速判据

| 看到什么 | 大概率是 | 怎么办 |
| --- | --- | --- |
| 主机名含 `ad` / `ads` / `track` / `stat` / `log` / `pixel` / `beacon` | 广告或追踪 | 可拦，但仍要看父域 |
| CNAME 指向 `cdngslb.com`、`alicdn.com`、`cloudfront.net`、`akamai*`、`fastly.net` | CDN 边缘节点 | **别拦**，见下文 |
| 父域是某家大厂主域（`jd.com`、`snssdk.com`、`qq.com`、`taobao.com`） | 业务接口 | 默认放行，只拦命名明确的广告子域 |
| 根路径 301/302 跳到别的站，且 `Access-Control-Allow-Origin` 全开 | 给前端 JS 调用的 API 域 | 用途不明就放行 |

### 第三步：看同族，别单看一个

单看 `mars.jd.com` 什么也看不出来，但把 `jd.com` 下被收录的 37 条拉出来，规律立刻清楚：

```text
jrad / jzt / ads-union / dsp-x / x / u-x / img-x / ccc-x   ← 广告与追踪
mllog / xlog / blackhole                                   ← 埋点
mars / uranus / mercury / hermes / cactus                  ← 内部服务代号
```

同族里明显是广告的那批，说明这个根域确实有广告体系；`mars` 属于另一组命名，就该单独判断，不能跟着一起封。

### 第四步：为什么「CDN 节点别拦」

`tnc3-bjlgy.snssdk.com` 这种最典型，三个理由：

1. **拦不住**——封了 `tnc3-bjlgy`，还有 `tnc0`~`tnc4` 和几十个机房代号，客户端立刻切走
2. **会误伤**——它和业务流量共用，拦了可能白图、接口变慢
3. **会过期**——CDN 调度是动态的，今天封的节点明天可能不用了

收益不明确、成本不确定、还会过期，这类规则不值得维护。

### 第五步：先拦后验，别在拦之前纠结

信息不足时**不用**在拦之前搞明白。更省事的顺序是反过来：

1. 先加进规则，拦住
2. 正常用 1~2 天，留意相关 App 有没有异常
3. 出问题 → AdGuard 过滤日志 → 找最近被拦的域名 → 加 `@@` 放行
4. 没问题 → 留着，但标 `confidence: low` 或 `medium`，等以后有证据再升级

绝大多数误拦在几分钟内就能暴露（白屏、图片不显示、登录转圈）。真正难查的是「半坏不坏」——比如某个低频功能偶尔失败，那种要靠日志慢慢对。

### 一个容易忽略的原则：默认放行

| | 代价 |
| --- | --- |
| 漏拦一个广告域 | 看到一个广告 |
| 误拦一个功能域 | App 某个功能坏了，且很难定位原因 |

两边代价不对称，所以**信息不足时应该放行**。规则数量多不等于更干净，每条没验证过的规则都是一个潜在故障点。

## 修改已有条目

- 只改事实，别改风格。
- 如果推翻了原判定，请在 PR 描述里写清「原来怎么判、为什么错、新的依据是什么」。
- 涉及 `keep` ↔ `block` 的翻转，请附实测记录（哪个 App、什么版本、拦了之后什么现象）。

## 新增一个厂商

1. `data/vendors.yaml` 追加条目（`id` / `name` / `name_cn` / `country` / `website` / `privacy` / `note`）
2. 新建 `data/domains/<id>.yaml`，首行写 `vendor: <id>`
3. 同一家公司的域名尽量放同一个文件，方便顺着线索摸清全貌

如果是「同类服务商聚合」型的文件（例如 `adnet-global.yaml` 收了十几家广告网络），每条必须写 `owner` 标注真实归属。

## PR 检查清单

- [ ] `python tools/validate.py` 通过
- [ ] `python tools/build_docs.py` 已运行，`docs/` 有对应变更
- [ ] `python tools/export_rules.py` 已运行（如果新增了可拦条目）
- [ ] 新增条目都有 `purpose` 和 `impact`，不是空话
- [ ] 拿不准的条目已标 `confidence: medium` / `low` 并在 `notes` 说明
- [ ] 没有手工修改 `docs/` 或 `lists/` 下的文件

## 不要做的事

- 不要往数据里塞整份规则库。这个项目要的是「理解」，不是「数量」。
- 不要为了凑数录入没验证过的域名。
- 不要在 `purpose` 里写价值判断（「流氓」「恶意」）。只写事实：它做什么、谁在用、拦了会怎样。
