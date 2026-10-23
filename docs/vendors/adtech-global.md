# 国际程序化广告与监测

覆盖 Criteo、Taboola、PubMatic、Magnite、OpenX、Xandr、Comscore 等。以 Web 端为主，属于纯广告与监测基础设施，误杀风险最低。


- 官网：—
- 隐私政策：—
- 登记域名：20 条

## `33across.com`

- **产品 / SDK**：33Across
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：较可信
- **标签**：身份识别、受众

**用途**

以身份识别与受众扩展为主的广告技术公司。

**拦截后果**

定向失效，广告量下降。

**规则**

```text
||33across.com^
```

## `adform.net`

- **产品 / SDK**：Adform
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：广告服务器、欧洲

**用途**

北欧为主的广告服务器、DSP 与 DMP 一体化平台。

**拦截后果**

广告位空白。

**规则**

```text
||adform.net^
```

## `adnxs.com`

- **产品 / SDK**：Xandr（原 AppNexus）
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：AdExchange、RTB

**用途**

微软旗下的程序化广告交易平台，ib.adnxs.com 是最常见的竞价端点。

**拦截后果**

广告位竞价失败。

**规则**

```text
||adnxs.com^
```

## `adsrvr.org`

- **产品 / SDK**：The Trade Desk
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：DSP、用户同步

**用途**

需求方平台（DSP）的竞价与用户匹配端点，常出现在网页的同步像素里。

**拦截后果**

跨站定向失效，广告量下降。

**规则**

```text
||adsrvr.org^
```

## `amazon-adsystem.com`

- **产品 / SDK**：Amazon Advertising
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：电商广告、程序化

**用途**

亚马逊广告平台，既投自家站点也做站外程序化投放。

**拦截后果**

亚马逊系广告位空白；亚马逊购物不受影响。

**规则**

```text
||amazon-adsystem.com^
```

## `casalemedia.com`

- **产品 / SDK**：Index Exchange
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：较可信
- **标签**：SSP、HeaderBidding

**用途**

老牌 SSP，以 header bidding 接入为主。

**拦截后果**

广告位竞价失败。

**规则**

```text
||casalemedia.com^
```

## `comscore.com`

- **产品 / SDK**：Comscore 主域
- **分类**：广告测量（`measurement`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：较可信
- **标签**：受众测量

**用途**

Comscore 的配置与报表域，部分采集脚本也从这里下发。

**拦截后果**

测量数据缺失。

**规则**

```text
||comscore.com^
```

## `criteo.com`

- **产品 / SDK**：Criteo
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：重定向、电商

**用途**

重定向广告网络。靠 Cookie 追踪用户浏览过的商品，在别的网站再推一次。电商站几乎必装。

**拦截后果**

「刚看过的东西到处跟着你」现象消失；商品页与下单不受影响。

**规则**

```text
||criteo.com^
```

## `criteo.net`

- **产品 / SDK**：Criteo 投放与素材域
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：重定向、备用域名

**用途**

Criteo 的广告投放、竞价与素材分发域，与 .com 分工不同。

**拦截后果**

只拦 .com 会漏掉大部分广告请求。

**规则**

```text
||criteo.net^
```

## `magnite.com`

- **产品 / SDK**：Magnite
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：SSP

**用途**

Magnite 现行主域，承担 SSP 竞价与素材分发。

**拦截后果**

广告位竞价失败。

**规则**

```text
||magnite.com^
```

## `moatads.com`

- **产品 / SDK**：Oracle Moat
- **分类**：广告测量（`measurement`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：可见性、测量

**用途**

广告可见性与无效流量测量，验证广告是否真的被人看到。

**拦截后果**

监测数据缺失，广告主侧统计不准，用户无感。

**规则**

```text
||moatads.com^
```

## `openx.net`

- **产品 / SDK**：OpenX
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：AdExchange

**用途**

独立广告交易平台，同时提供 SSP 与 Ad Exchange 能力。

**拦截后果**

广告位竞价失败。

**规则**

```text
||openx.net^
```

## `outbrain.com`

- **产品 / SDK**：Outbrain
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：原生广告、内容推荐

**用途**

与 Taboola 同类的内容推荐广告网络。

**拦截后果**

推荐位空白。

**规则**

```text
||outbrain.com^
```

## `pubmatic.com`

- **产品 / SDK**：PubMatic
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：SSP、RTB

**用途**

卖方平台（SSP），帮媒体把广告位拿到交易所竞价。

**拦截后果**

广告位竞价失败，广告空白。

**规则**

```text
||pubmatic.com^
```

## `quantserve.com`

- **产品 / SDK**：Quantcast
- **分类**：广告测量（`measurement`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：受众测量、DSP

**用途**

受众测量与程序化投放，pixel.quantserve.com 是最常见的采集端点。

**拦截后果**

测量与定向失效。

**规则**

```text
||quantserve.com^
```

## `rubiconproject.com`

- **产品 / SDK**：Magnite（原 Rubicon Project）
- **分类**：广告交易（`ad-exchange`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：SSP、RTB

**用途**

大型 SSP，2020 年与 Telaria 合并后更名 Magnite。

**拦截后果**

广告位竞价失败。

**规则**

```text
||rubiconproject.com^
```

## `scorecardresearch.com`

- **产品 / SDK**：Comscore
- **分类**：广告测量（`measurement`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：受众测量

**用途**

受众测量与流量统计，用像素记录站点访问人群特征。

**拦截后果**

测量数据缺失，用户无感。

**规则**

```text
||scorecardresearch.com^
```

## `smartadserver.com`

- **产品 / SDK**：Equativ（原 Smart AdServer）
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：较可信
- **标签**：广告服务器、欧洲

**用途**

欧洲为主的广告服务器与 SSP。

**拦截后果**

广告位空白。

**规则**

```text
||smartadserver.com^
```

## `taboola.com`

- **产品 / SDK**：Taboola
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：原生广告、内容推荐

**用途**

内容推荐广告网络，网页底部「你可能感兴趣」「推荐阅读」的赞助内容。

**拦截后果**

推荐位空白，正文不受影响。

**规则**

```text
||taboola.com^
```

## `teads.tv`

- **产品 / SDK**：Teads
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：视频广告、原生广告

**用途**

外播视频广告（outstream video），把视频广告插进图文正文中间。

**拦截后果**

正文中的自动播放视频广告消失，页面更省流量。

**规则**

```text
||teads.tv^
```

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。