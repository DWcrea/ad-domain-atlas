# 与主流规则库的覆盖对比

回答一个问题：这些域名，现成的规则库到底拦了多少？没被拦的部分，才是需要自己补规则的地方。


> 生成于 2026-10-23

## 参与比对的规则库

| 规则库 | 条目数 | 来源 |
| --- | --- | --- |
| OISD big | 234,497 | `oisd_big.txt` |
| SM-Ad-FuckU-hosts | 4,979 | `SMAdHosts.txt` |

## 总体覆盖

- 收录域名：**146** 条
- 被规则库直接命中：**81** 条
- 仅被上级域规则覆盖：**0** 条
- 完全未覆盖：**65** 条
- 覆盖率：**55.5%**

「仅被上级域覆盖」指规则库只封了某个子域（例如 `||ad.doubleclick.net^`），而没有封主机根域。这类条目在 DNS 层仍可能漏掉其他子域。

## 规则库漏掉的可拦域名（44 条）

这些条目判定为可拦，但上面参与比对的规则库里没有对应规则。把它们补进自己的规则集，效果会立竿见影。

| 域名 | 厂商 | 判定 | 用途 |
| --- | --- | --- | --- |
| `alimama.com` | Alibaba | 拦截 | 淘宝联盟与直通车的投放管理、素材与点击跳转接口。 |
| `cnzz.com` | Alibaba | 拦截 | 面向中小站长的访问统计，采集 PV/UV、来源、地域。 |
| `mmstat.com` | Alibaba | 拦截 | 阿里系 App 的埋点上报域（User Track），记录页面浏览、点击、停留时长。 |
| `tanx.com` | Alibaba | 拦截 | 阿里的 RTB 广告交易市场，向媒体方提供广告位竞价与素材。 |
| `pangle.io` | ByteDance | 拦截 | 面向海外开发者的广告变现平台，提供广告请求、报表与素材接口。 |
| `2mdn.net` | Google | 拦截 | 存放 DoubleClick 广告素材（图片、视频、富媒体创意），由广告投放域引用。 |
| `app-measurement.com` | Google | 拦截·代价 | 移动 App 的 Firebase 埋点上报端点，负责事件、用户属性、受众同步。 |
| `crashlytics.com` | Google | 拦截·代价 | 崩溃与 ANR 上报，附带设备型号、系统版本、堆栈与最近操作路径。 |
| `firebaseinstallations.googleapis.com` | Google | 拦截·代价 | 生成并维护 Firebase Installation ID（FID），Analytics、Remote Config、Cloud Messaging 都依赖它做实例标识。 |
| `googletagmanager.com` | Google | 拦截·代价 | 标签管理器容器。 |
| `googletagservices.com` | Google | 拦截 | 网页广告位的调度脚本（gpt.js），负责向 Ad Manager 请求广告并渲染到页面。 |
| `connect.facebook.net` | Meta | 拦截·代价 | 网页端 SDK 宿主。 |
| `amplitude.com` | 产品分析 | 拦截 | 与 Mixpanel 同类的行为分析平台，移动端与网页端都常用。 |
| `heap.io` | 产品分析 | 拦截 | 全量自动采集（capture everything），不需要预先埋点。 |
| `hotjar.com` | 产品分析 | 拦截 | 会话录制、热图与问卷，能回放用户在你站点上的每一次点击与滚动。 |
| `mixpanel.com` | 产品分析 | 拦截 | 事件级产品分析，记录每一次点击、注册、付费，做漏斗与留存。 |
| `segment.com` | 产品分析 | 拦截·代价 | 客户数据平台（CDP）。 |
| `segment.io` | 产品分析 | 拦截·代价 | Segment 的实际数据上报域（api.segment.io），与 segment.com 分工不同。 |
| `metrics.data.hicloud.com` | 国产终端厂商 | 拦截·代价 | 华为分析服务（Analytics Kit）与系统遥测的数据上报端点。 |
| `mistat.xiaomi.com` | 国产终端厂商 | 拦截·代价 | MIUI/HyperOS 与小米系 App 的使用统计、广告归因、设备画像上报。 |
| `sensorsdata.cn` | 国内第三方 SDK | 拦截·代价 | 埋点上报主域（/sa、/sdk），记录事件、页面、用户属性。 |
| `inmobi.com` | 国际广告网络与聚合 | 拦截 | 全球移动广告网络，覆盖印度、东南亚市场较多。 |
| `adform.net` | 国际程序化广告与监测 | 拦截 | 北欧为主的广告服务器、DSP 与 DMP 一体化平台。 |
| `adnxs.com` | 国际程序化广告与监测 | 拦截 | 微软旗下的程序化广告交易平台，ib.adnxs.com 是最常见的竞价端点。 |
| `magnite.com` | 国际程序化广告与监测 | 拦截 | Magnite 现行主域，承担 SSP 竞价与素材分发。 |
| `outbrain.com` | 国际程序化广告与监测 | 拦截 | 与 Taboola 同类的内容推荐广告网络。 |
| `rubiconproject.com` | 国际程序化广告与监测 | 拦截 | 大型 SSP，2020 年与 Telaria 合并后更名 Magnite。 |
| `scorecardresearch.com` | 国际程序化广告与监测 | 拦截 | 受众测量与流量统计，用像素记录站点访问人群特征。 |
| `taboola.com` | 国际程序化广告与监测 | 拦截 | 内容推荐广告网络，网页底部「你可能感兴趣」「推荐阅读」的赞助内容。 |
| `bugsnag.com` | 崩溃与性能监控 | 拦截·代价 | 异常与稳定性监控，按错误聚合与告警。 |
| `instabug.com` | 崩溃与性能监控 | 拦截·代价 | 应用内反馈 SDK，收集崩溃、卡顿、网络日志，并把用户反馈与现场数据一起上报。 |
| `newrelic.com` | 崩溃与性能监控 | 拦截·代价 | 应用性能监控（APM），采集请求耗时、数据库调用、错误率。 |
| `sentry.io` | 崩溃与性能监控 | 拦截·代价 | 崩溃、异常、性能追踪上报。 |
| `adjust.com` | 归因与深度链接 | 拦截 | 与 AppsFlyer 同类的归因平台，欧洲市场占有率较高，同时提供防作弊。 |
| `appsflyer.com` | 归因与深度链接 | 拦截·代价 | 移动归因与营销分析的事实标准。 |
| `branch.io` | 归因与深度链接 | 拦截·代价 | 深度链接与归因一体。 |
| `kochava.com` | 归因与深度链接 | 拦截 | 归因与受众平台，游戏与工具类 App 使用较多。 |
| `singular.net` | 归因与深度链接 | 拦截 | 归因与营销 ETL 平台，把多家渠道数据汇总做 ROI 分析。 |
| `tenjin.com` | 归因与深度链接 | 拦截 | 面向独立游戏开发者的轻量归因与收入分析。 |
| `airship.com` | 营销自动化与推送 | 拦截·代价 | 推送基础设施与消息编排，服务大量欧美媒体与零售 App。 |
| `braze.com` | 营销自动化与推送 | 拦截·代价 | 跨渠道营销自动化，统一管理推送、站内信、邮件与短信的触达节奏。 |
| `clevertap.com` | 营销自动化与推送 | 拦截·代价 | 用户分群与营销自动化，主打推送与应用内消息。 |
| `onesignal.com` | 营销自动化与推送 | 拦截·代价 | 免费的跨平台推送服务，中小开发者常用。 |
| `pushwoosh.com` | 营销自动化与推送 | 拦截·代价 | 推送与营销自动化平台，东欧市场较多。 |

另有 21 条「不建议拦截」的域名本来就不该出现在规则库里，未计入上表。它们见 [误杀黑名单](keep.md)。

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。