# 按用途分类

同一个域名只归一个主分类。分类说明见下表。


| 分类 | 说明 | 数量 |
| --- | --- | --- |
| 广告投放 (`ad-serving`) | 广告请求、素材分发、曝光与点击计数 | 48 |
| 广告交易 (`ad-exchange`) | RTB 竞价、DSP/SSP 交换、程序化交易 | 9 |
| 聚合中介 (`mediation`) | 多家广告网络的聚合调度与瀑布流 | 4 |
| 行为追踪 (`tracking`) | 跨站/跨应用行为采集、用户画像、埋点 | 9 |
| 统计分析 (`analytics`) | 产品分析、留存、漏斗、热图 | 24 |
| 安装归因 (`attribution`) | 渠道归因、深度链接、转化回传 | 6 |
| 广告测量 (`measurement`) | 可见性、品牌提升、第三方监测 | 6 |
| 崩溃监控 (`crash`) | 崩溃、异常、APM 性能上报 | 6 |
| 推送消息 (`push`) | 推送通道、营销自动化触达 | 10 |
| 基础服务 (`infra`) | CDN、静态资源、设备注册等业务必需能力 | 24 |

## 广告投放

广告请求、素材分发、曝光与点击计数

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `2mdn.net` | Google | DoubleClick Studio 素材 CDN | 存放 DoubleClick 广告素材（图片、视频、富媒体创意），由广告投放域引用。 | 拦截 |
| `ad.xiaomi.com` | 国产终端厂商 | 小米广告（MIUI 广告） | MIUI 系统广告位（负一屏、天气、文件夹推荐）的广告请求与素材下发。 | 拦截 |
| `adcolony.com` | 国际广告网络与聚合 | AdColony（Digital Turbine） | 高清视频广告网络，以激励视频为主，2021 年被 Digital Turbine 收购。 | 拦截 |
| `adform.net` | 国际程序化广告与监测 | Adform | 北欧为主的广告服务器、DSP 与 DMP 一体化平台。 | 拦截 |
| `adkwai.com` | Kuaishou | 快手广告（磁力引擎） | 快手磁力引擎的广告投放域，承担广告请求、竞价与素材地址下发，同时也作为联盟广告的落地域。 | 拦截 |
| `adservice.google.com` | Google | AdMob / AdX 移动端广告请求 | 移动 App 内广告 SDK 的请求入口，常见路径 /adsid/integrator.js 与 /pagead/。 | 拦截 |
| `adsfs.oppomobile.com` | 国产终端厂商 | OPPO 广告素材 CDN | ColorOS 系统广告与 OPPO 联盟广告的素材分发。 | 拦截 |
| `adview.cn` | 国内广告联盟 | AdView 移动广告平台 | 移动广告联盟，为中小 App 提供 banner、插屏、开屏广告的请求与素材接口。 | 拦截 |
| `alimama.com` | Alibaba | 阿里妈妈投放平台 | 淘宝联盟与直通车的投放管理、素材与点击跳转接口。 | 拦截 |
| `amazon-adsystem.com` | 国际程序化广告与监测 | Amazon Advertising | 亚马逊广告平台，既投自家站点也做站外程序化投放。 | 拦截 |
| `an.facebook.com` | Meta | Meta Audience Network | 面向第三方 App 的横幅、插屏、激励视频广告请求与素材下发。 | 拦截 |
| `applvn.com` | 国际广告网络与聚合 | AppLovin 短域 | AppLovin 的短域名，承担事件上报与素材地址分流，常被漏拦。 | 拦截 |
| `atanx.alicdn.com` | Alibaba | 阿里妈妈素材 CDN | 存放 Tanx 广告素材，由投放域引用。 | 拦截 |
| `chartboost.com` | 国际广告网络与聚合 | Chartboost | 游戏内广告网络与交叉推广平台。 | 拦截 |
| `cpro.baidu.com` | Baidu | 百度联盟内容推荐广告 | 站内内容推荐位与信息流广告的投放接口，常以「相关推荐」形式出现在正文底部。 | 拦截 |
| `criteo.com` | 国际程序化广告与监测 | Criteo | 重定向广告网络。 | 拦截 |
| `criteo.net` | 国际程序化广告与监测 | Criteo 投放与素材域 | Criteo 的广告投放、竞价与素材分发域，与 .com 分工不同。 | 拦截 |
| `csjplatform.com` | ByteDance | 穿山甲平台域（csj = 穿山甲） | 命名与穿山甲缩写一致，被 OISD 等主流规则库收录，用途指向广告平台服务端； | 拦截 |
| `domob.cn` | 国内广告联盟 | 多盟（Domob） | 移动广告联盟与 DSP，提供广告投放、素材与点击跳转。 | 拦截 |
| `doubleclick.net` | Google | Google Ad Manager / DoubleClick（DFP） | Google 展示广告的核心投放域。 | 拦截 |
| `e.qq.com` | Tencent | 广点通曝光与点击上报 | 广告曝光、点击、转化的事件上报端点，广告请求成功后紧接着打这里。 | 拦截 |
| `gdt.qq.com` | Tencent | 广点通 / 腾讯广告 | 腾讯广告（原广点通）的广告请求与投放接口，微信、QQ、腾讯视频、优量汇的广告位都从这里取量。 | 拦截 |
| `googleadservices.com` | Google | Google Ads 点击与转化跟踪 | 广告点击后的跳转与转化归因（pagead/aclk、pagead/conversion）。 | 拦截 |
| `googlesyndication.com` | Google | AdSense / AdMob | pagead2.googlesyndication.com 下发广告脚本，tpc.googlesyndication.com 存放广告素材，googleads.g.double… | 拦截 |
| `googletagservices.com` | Google | Google Publisher Tag（GPT） | 网页广告位的调度脚本（gpt.js），负责向 Ad Manager 请求广告并渲染到页面。 | 拦截 |
| `inmobi.com` | 国际广告网络与聚合 | InMobi | 全球移动广告网络，覆盖印度、东南亚市场较多。 | 拦截 |
| `liftoff.io` | 国际广告网络与聚合 | Liftoff | 效果广告与再营销平台，服务端接口与素材分发。 | 拦截 |
| `mediav.com` | 国内广告联盟 | MediaV（聚胜万合） | 效果广告投放与精准定向平台，电商与游戏行业使用较多。 | 拦截 |
| `mintegral.com` | 国际广告网络与聚合 | Mintegral（汇量科技） | 全球移动广告平台，以激励视频与试玩广告见长，国内出海 App 使用极多。 | 拦截 |
| `mintegral.net` | 国际广告网络与聚合 | Mintegral 备用域 | 与 mintegral.com 等价的素材与请求域，用于分流与容灾。 | 拦截 |
| `mobads.baidu.com` | Baidu | 百青藤（百度移动广告） | 面向移动 App 的百度广告联盟接口，提供开屏、插屏、激励视频。 | 拦截 |
| `outbrain.com` | 国际程序化广告与监测 | Outbrain | 与 Taboola 同类的内容推荐广告网络。 | 拦截 |
| `pangle.io` | ByteDance | Pangle（穿山甲海外版） | 面向海外开发者的广告变现平台，提供广告请求、报表与素材接口。 | 拦截 |
| `pangolin-sdk-toutiao-b.com` | ByteDance | 穿山甲备用域（B） | 穿山甲主域不可用时的轮换域名，功能与主域完全等价。 | 拦截 |
| `pangolin-sdk-toutiao.com` | ByteDance | 穿山甲（Pangle）广告 SDK | 国内穿山甲 SDK 的服务端入口，承担广告请求、竞价、配置下发与素材地址返回。 | 拦截 |
| `pangolin-sdk-toutiao1.com` | ByteDance | 穿山甲备用域（1~4） | 穿山甲按序号轮换的一组域名，-toutiao1 至 -toutiao4 同时存在，SDK 会在失败时依次重试。 | 拦截 |
| `pangolin-x.com` | ByteDance | 穿山甲关联域 | 穿山甲体系内的辅助域，用于配置拉取与请求分流，被主流规则库普遍收录。 | 拦截 |
| `pangolin.snssdk.com` | ByteDance | 穿山甲（snssdk 下接口） | 挂在 snssdk.com 主域下的穿山甲广告接口，与抖音业务接口共用根域，必须按主机名拦。 | 拦截 |
| `pangolin16.isnssdk.com` | ByteDance | 穿山甲国际版接口 | TikTok / 海外字节系 App 的穿山甲广告接口。 | 拦截 |
| `pgdt.gtimg.com` | Tencent | 广点通素材 CDN | 存放广点通广告的图片与视频素材，由投放域引用。 | 拦截 |
| `pos.baidu.com` | Baidu | 百度联盟主题推广 | 百度联盟的展示广告位接口，站长嵌入的「百度联盟推广」大多指向这里。 | 拦截 |
| `smartadserver.com` | 国际程序化广告与监测 | Equativ（原 Smart AdServer） | 欧洲为主的广告服务器与 SSP。 | 拦截 |
| `supersonicads.com` | 国际广告网络与聚合 | ironSource 旧域 | ironSource 早期域名，老版本 SDK 仍会请求。 | 拦截 |
| `taboola.com` | 国际程序化广告与监测 | Taboola | 内容推荐广告网络，网页底部「你可能感兴趣」「推荐阅读」的赞助内容。 | 拦截 |
| `tapjoy.com` | 国际广告网络与聚合 | Tapjoy | 激励视频与积分墙，用户完成任务换取游戏内奖励。 | 拦截 |
| `teads.tv` | 国际程序化广告与监测 | Teads | 外播视频广告（outstream video），把视频广告插进图文正文中间。 | 拦截 |
| `unityads.unity3d.com` | 国际广告网络与聚合 | Unity Ads | Unity Ads 的广告请求与展示接口，大量休闲游戏的主要变现方式。 | 拦截 |
| `vungle.com` | 国际广告网络与聚合 | Vungle（Liftoff） | 视频广告网络，主打激励视频与插屏，2021 年被 Liftoff 收购。 | 拦截 |

## 广告交易

RTB 竞价、DSP/SSP 交换、程序化交易

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `33across.com` | 国际程序化广告与监测 | 33Across | 以身份识别与受众扩展为主的广告技术公司。 | 拦截 |
| `adnxs.com` | 国际程序化广告与监测 | Xandr（原 AppNexus） | 微软旗下的程序化广告交易平台，ib.adnxs.com 是最常见的竞价端点。 | 拦截 |
| `adsrvr.org` | 国际程序化广告与监测 | The Trade Desk | 需求方平台（DSP）的竞价与用户匹配端点，常出现在网页的同步像素里。 | 拦截 |
| `casalemedia.com` | 国际程序化广告与监测 | Index Exchange | 老牌 SSP，以 header bidding 接入为主。 | 拦截 |
| `magnite.com` | 国际程序化广告与监测 | Magnite | Magnite 现行主域，承担 SSP 竞价与素材分发。 | 拦截 |
| `openx.net` | 国际程序化广告与监测 | OpenX | 独立广告交易平台，同时提供 SSP 与 Ad Exchange 能力。 | 拦截 |
| `pubmatic.com` | 国际程序化广告与监测 | PubMatic | 卖方平台（SSP），帮媒体把广告位拿到交易所竞价。 | 拦截 |
| `rubiconproject.com` | 国际程序化广告与监测 | Magnite（原 Rubicon Project） | 大型 SSP，2020 年与 Telaria 合并后更名 Magnite。 | 拦截 |
| `tanx.com` | Alibaba | 阿里妈妈 Tanx 广告交易平台 | 阿里的 RTB 广告交易市场，向媒体方提供广告位竞价与素材。 | 拦截 |

## 聚合中介

多家广告网络的聚合调度与瀑布流

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `applovin.com` | 国际广告网络与聚合 | AppLovin MAX / AXON | 广告聚合平台 MAX 与自有广告网络 AXON 的服务端，负责广告请求、竞价、瀑布流调度。 | 拦截 |
| `fyber.com` | 国际广告网络与聚合 | Fyber（Digital Turbine） | 广告聚合与交易平台，提供 Offer Wall 与中介服务。 | 拦截 |
| `ironsrc.com` | 国际广告网络与聚合 | ironSource（Unity LevelPlay） | ironSource 广告聚合与自有网络的统一入口，2022 年被 Unity 收购后与 LevelPlay 合并。 | 拦截 |
| `mopub.com` | 国际广告网络与聚合 | MoPub（已关停） | Twitter 旗下的广告聚合平台，2022 年 12 月停止服务，流量迁移至 AppLovin MAX。 | 拦截 |

## 行为追踪

跨站/跨应用行为采集、用户画像、埋点

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `connect.facebook.net` | Meta | Facebook JS SDK / Pixel | 网页端 SDK 宿主。 | 拦截·代价 |
| `dm.bytedance.com` | ByteDance | 字节数据管理平台（DMP） | 人群包与用户标签的同步接口，服务于广告定向。 | 拦截·代价 |
| `firebaseinstallations.googleapis.com` | Google | Firebase Installations | 生成并维护 Firebase Installation ID（FID），Analytics、Remote Config、Cloud Messaging 都依赖它做实例标识。 | 拦截·代价 |
| `googletagmanager.com` | Google | Google Tag Manager（GTM） | 标签管理器容器。 | 拦截·代价 |
| `graph.facebook.com` | Meta | Facebook Graph API | Graph API 统一入口。 | 部分 |
| `log.snssdk.com` | ByteDance | 字节日志上报 | App 运行日志与行为埋点的批量上报通道。 | 拦截·代价 |
| `mssdk.bytedance.com` | ByteDance | 字节通用 SDK 服务 | 提供设备标识、SDK 配置、灰度开关等通用能力，被抖音、头条、番茄等多款 App 共用。 | 拦截·代价 |
| `segment.com` | 产品分析 | Segment（Twilio） | 客户数据平台（CDP）。 | 拦截·代价 |
| `segment.io` | 产品分析 | Segment 采集端点 | Segment 的实际数据上报域（api.segment.io），与 segment.com 分工不同。 | 拦截·代价 |

## 统计分析

产品分析、留存、漏斗、热图

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `amplitude.com` | 产品分析 | Amplitude | 与 Mixpanel 同类的行为分析平台，移动端与网页端都常用。 | 拦截 |
| `app-measurement.com` | Google | Firebase Analytics（GA4 for Firebase） | 移动 App 的 Firebase 埋点上报端点，负责事件、用户属性、受众同步。 | 拦截·代价 |
| `beacon.qq.com` | Tencent | 腾讯灯塔（Beacon） | 客户端质量与行为数据上报，覆盖卡顿、崩溃、页面耗时。 | 拦截·代价 |
| `cnzz.com` | Alibaba | CNZZ 站长统计（友盟旗下） | 面向中小站长的访问统计，采集 PV/UV、来源、地域。 | 拦截 |
| `flurry.com` | 营销自动化与推送 | Flurry（Yahoo） | 移动应用分析与广告归因，Yahoo 旗下的老牌移动统计 SDK。 | 拦截 |
| `fullstory.com` | 产品分析 | FullStory | 全量会话回放，把用户在页面上的所有操作录成可检索的「录像」。 | 拦截 |
| `google-analytics.com` | Google | Google Analytics（UA / GA4） | GA 的数据采集端点，analytics.js、gtag/js 与 /g/collect 上报都指向这里。 | 拦截 |
| `growingio.com` | 国内第三方 SDK | GrowingIO | 无埋点采集与热图分析，自动抓取页面元素与点击行为。 | 拦截 |
| `heap.io` | 产品分析 | Heap | 全量自动采集（capture everything），不需要预先埋点。 | 拦截 |
| `hm.baidu.com` | Baidu | 百度统计 | 网站访问统计的采集端点（hm.js 与 /hm.gif），记录 PV/UV、来源、事件。 | 拦截 |
| `hotjar.com` | 产品分析 | Hotjar | 会话录制、热图与问卷，能回放用户在你站点上的每一次点击与滚动。 | 拦截 |
| `metrics.data.hicloud.com` | 国产终端厂商 | 华为分析 / HMS 遥测 | 华为分析服务（Analytics Kit）与系统遥测的数据上报端点。 | 拦截·代价 |
| `mistat.xiaomi.com` | 国产终端厂商 | 小米统计（MIUI 遥测） | MIUI/HyperOS 与小米系 App 的使用统计、广告归因、设备画像上报。 | 拦截·代价 |
| `mixpanel.com` | 产品分析 | Mixpanel | 事件级产品分析，记录每一次点击、注册、付费，做漏斗与留存。 | 拦截 |
| `mmstat.com` | Alibaba | 阿里 UT 统计 | 阿里系 App 的埋点上报域（User Track），记录页面浏览、点击、停留时长。 | 拦截 |
| `mon.snssdk.com` | ByteDance | 字节监控上报 | 性能、卡顿、网络质量等监控数据的上报端点。 | 拦截·代价 |
| `pingjs.qq.com` | Tencent | 腾讯前端性能监控 | 页面性能指标（加载耗时、JS 错误）的采集脚本与上报端点。 | 拦截 |
| `sensorsdata.cn` | 国内第三方 SDK | 神策数据（Sensors Analytics） | 埋点上报主域（/sa、/sdk），记录事件、页面、用户属性。 | 拦截·代价 |
| `ta.qq.com` | Tencent | 腾讯分析（TA） | 网页与 H5 的访问统计、来源分析、转化漏斗采集端点。 | 拦截 |
| `talkingdata.com` | 国内第三方 SDK | TalkingData | 移动统计与广告归因，同时提供数据交易服务（TalkingData AdTracking）。 | 拦截 |
| `tongji.baidu.com` | Baidu | 百度统计后台 | 统计报表与配置后台，同时承担部分数据上报。 | 拦截 |
| `umeng.co` | Alibaba | 友盟短域 | 友盟的短域名，用于素材与上报的分流。 | 拦截·代价 |
| `umeng.com` | Alibaba | 友盟+（U-App / U-Push） | 国内使用最广的第三方统计 SDK。 | 拦截·代价 |
| `umengcloud.com` | Alibaba | 友盟数据上报端点 | U-App 的实际数据上报与配置下发域名，与 umeng.com 互为补充。 | 拦截·代价 |

## 安装归因

渠道归因、深度链接、转化回传

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `adjust.com` | 归因与深度链接 | Adjust | 与 AppsFlyer 同类的归因平台，欧洲市场占有率较高，同时提供防作弊。 | 拦截 |
| `appsflyer.com` | 归因与深度链接 | AppsFlyer | 移动归因与营销分析的事实标准。 | 拦截·代价 |
| `branch.io` | 归因与深度链接 | Branch | 深度链接与归因一体。 | 拦截·代价 |
| `kochava.com` | 归因与深度链接 | Kochava | 归因与受众平台，游戏与工具类 App 使用较多。 | 拦截 |
| `singular.net` | 归因与深度链接 | Singular | 归因与营销 ETL 平台，把多家渠道数据汇总做 ROI 分析。 | 拦截 |
| `tenjin.com` | 归因与深度链接 | Tenjin | 面向独立游戏开发者的轻量归因与收入分析。 | 拦截 |

## 广告测量

可见性、品牌提升、第三方监测

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `comscore.com` | 国际程序化广告与监测 | Comscore 主域 | Comscore 的配置与报表域，部分采集脚本也从这里下发。 | 拦截 |
| `gridsum.com` | 国内广告联盟 | 国双（Gridsum） | 网站与广告的第三方数据分析、监测与归因，常见于大型企业站点。 | 拦截 |
| `miaozhen.com` | Alibaba | 秒针系统（Miaozhen） | 第三方广告监测，做曝光验证、可见性测量与到达率统计，广告主用它给媒体结账。 | 拦截 |
| `moatads.com` | 国际程序化广告与监测 | Oracle Moat | 广告可见性与无效流量测量，验证广告是否真的被人看到。 | 拦截 |
| `quantserve.com` | 国际程序化广告与监测 | Quantcast | 受众测量与程序化投放，pixel.quantserve.com 是最常见的采集端点。 | 拦截 |
| `scorecardresearch.com` | 国际程序化广告与监测 | Comscore | 受众测量与流量统计，用像素记录站点访问人群特征。 | 拦截 |

## 崩溃监控

崩溃、异常、APM 性能上报

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `bugly.qq.com` | Tencent | 腾讯 Bugly | 崩溃、ANR、卡顿上报与热更新下发，国内 App 使用极广。 | 拦截·代价 |
| `bugsnag.com` | 崩溃与性能监控 | Bugsnag（SmartBear） | 异常与稳定性监控，按错误聚合与告警。 | 拦截·代价 |
| `crashlytics.com` | Google | Firebase Crashlytics | 崩溃与 ANR 上报，附带设备型号、系统版本、堆栈与最近操作路径。 | 拦截·代价 |
| `instabug.com` | 崩溃与性能监控 | Instabug | 应用内反馈 SDK，收集崩溃、卡顿、网络日志，并把用户反馈与现场数据一起上报。 | 拦截·代价 |
| `newrelic.com` | 崩溃与性能监控 | New Relic | 应用性能监控（APM），采集请求耗时、数据库调用、错误率。 | 拦截·代价 |
| `sentry.io` | 崩溃与性能监控 | Sentry | 崩溃、异常、性能追踪上报。 | 拦截·代价 |

## 推送消息

推送通道、营销自动化触达

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `airship.com` | 营销自动化与推送 | Airship（原 Urban Airship） | 推送基础设施与消息编排，服务大量欧美媒体与零售 App。 | 拦截·代价 |
| `appboy.com` | 营销自动化与推送 | Braze 旧域（Appboy） | Braze 改名前的域名，老版本 SDK 仍在引用。 | 拦截·代价 |
| `braze.com` | 营销自动化与推送 | Braze | 跨渠道营销自动化，统一管理推送、站内信、邮件与短信的触达节奏。 | 拦截·代价 |
| `clevertap.com` | 营销自动化与推送 | CleverTap | 用户分群与营销自动化，主打推送与应用内消息。 | 拦截·代价 |
| `getui.com` | 国内第三方 SDK | 个推（Getui） | 个推消息推送服务，同时提供用户画像与数据服务（个推大数据）。 | 保留 |
| `igexin.com` | 国内第三方 SDK | 个推旧域 | 个推早期域名，老版本 SDK 仍在引用。 | 保留 |
| `jiguang.cn` | 国内第三方 SDK | 极光 JPush / JVerification | 极光推送的长连接与 API 入口，同时承载一键登录（JVerification）与统计（JAnalytics）。 | 保留 |
| `jpush.cn` | 国内第三方 SDK | 极光推送短域 | JPush 的短域名，用于推送通道与消息回执。 | 保留 |
| `onesignal.com` | 营销自动化与推送 | OneSignal | 免费的跨平台推送服务，中小开发者常用。 | 拦截·代价 |
| `pushwoosh.com` | 营销自动化与推送 | Pushwoosh | 推送与营销自动化平台，东欧市场较多。 | 拦截·代价 |

## 基础服务

CDN、静态资源、设备注册等业务必需能力

| 域名 | 厂商 | 产品 | 用途 | 判定 |
| --- | --- | --- | --- | --- |
| `alicdn.com` | Alibaba | 阿里巴巴 CDN | 淘宝、天猫、支付宝、闲鱼等业务的图片与静态资源 CDN，体量极大。 | 保留 |
| `baidu.com` | Baidu | 百度主域 | 搜索、账号、网盘、地图、百家号等业务的宿主域。 | 保留 |
| `baidustatic.com` | Baidu | 百度静态资源 CDN | 百度各业务的前端静态资源（JS/CSS/图片）分发。 | 保留 |
| `bytedance.com` | ByteDance | 字节跳动主域 | 企业官网与部分 SDK 的配置、鉴权入口。 | 保留 |
| `facebook.com` | Meta | Facebook 主域 | 账号登录、OAuth 授权、分享、Messenger 跳转的宿主域。 | 保留 |
| `facebook.net` | Meta | Facebook 静态资源域 | 承载 connect.facebook.net 等前端 SDK 资源。 | 保留 |
| `fbcdn.net` | Meta | Facebook 内容 CDN | 头像、图片、视频、静态资源分发。 | 保留 |
| `gifshow.com` | Kuaishou | 快手内容 CDN / 旧版接口 | 快手（原快手 GIF 秀）的视频与封面 CDN，仍被大量客户端引用。 | 保留 |
| `google.com` | Google | Google 主域 | 搜索、账号、登录、验证码、地图等核心服务的宿主域。 | 保留 |
| `googleapis.com` | Google | Google APIs 公共入口 | 承载 Firebase、地图、登录、云服务的统一 API 网关，大量 App 的基础能力都在这个域下。 | 保留 |
| `gstatic.com` | Google | Google 静态资源 CDN | 提供字体、JS 库、公共静态资源。 | 保留 |
| `gtimg.com` | Tencent | 腾讯图片 CDN | 腾讯全系产品的图片与静态资源 CDN，头像、表情、封面、新闻配图都在这里。 | 保留 |
| `hicloud.com` | 国产终端厂商 | 华为云 / HMS 基础设施 | 华为云服务、HMS Core 能力、云空间与推送的基础设施域。 | 保留 |
| `is.snssdk.com` | ByteDance | 字节设备注册与服务发现 | 设备注册、服务端地址下发，App 启动阶段的第一跳。 | 保留 |
| `isnssdk.com` | ByteDance | TikTok / 海外字节核心 API | snssdk.com 的海外对应域，承载 TikTok 的业务接口。 | 保留 |
| `kuaishou.com` | Kuaishou | 快手主域 | 快手 App 与网页版的账号、内容、直播接口宿主域。 | 保留 |
| `mob.com` | 国内第三方 SDK | MobTech ShareSDK / 秒验 | 社交分享与第三方登录（ShareSDK）、本机号码一键登录（秒验）。 | 保留 |
| `oppomobile.com` | 国产终端厂商 | OPPO 系统服务 / 推送 | ColorOS 系统服务、OPPO 推送（PUSH）与账号体系的宿主域。 | 保留 |
| `pstatp.com` | ByteDance | 字节内容 CDN | 图片、视频、头像、封面等静态资源的 CDN。 | 保留 |
| `qq.com` | Tencent | 腾讯主域 | QQ 登录、微信开放平台回调、腾讯文档、邮箱等业务的宿主域。 | 保留 |
| `snssdk.com` | ByteDance | 抖音 / 今日头条核心 API | 内容流、账号、支付、直播等业务接口的宿主域，抖音与头条 App 的主干。 | 保留 |
| `unity3d.com` | 国际广告网络与聚合 | Unity 引擎 / 服务 | Unity 引擎的资源、License 校验、云服务入口。 | 保留 |
| `vivo.com.cn` | 国产终端厂商 | vivo 系统服务 / 推送 | Funtouch OS / OriginOS 系统服务、vivo 推送与账号体系。 | 保留 |
| `xiaomi.com` | 国产终端厂商 | 小米账号 / 云服务 | 小米账号登录、云服务、应用商店、系统更新的宿主域。 | 保留 |

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。