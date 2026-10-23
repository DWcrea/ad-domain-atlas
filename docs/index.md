# 广告域名总表

按厂商分组。点域名可跳到该厂商详情页，查看拦截副作用与证据来源。

> 共 **189** 条记录 · **19** 家厂商
>
> 拦截判定：可拦 **145** · 建议保留 **44**（145 + 44 = 189）
>
> 置信度：已确认 **137** · 较可信 **50** · 待验证 **2**；其中 **1** 条为已停用服务
>
> 后两行是同一批记录的另一种切法，不是新的条目。

| 判定 | 含义 |
| --- | --- |
| `拦截` | 直接拦截：无业务副作用，可整域封禁 |
| `拦截·代价` | 可拦，有代价：拦掉后丢失某项数据或功能，但不影响核心使用 |
| `部分` | 部分拦截：同域混用业务流量，只能按主机名或路径精确拦截 |
| `保留` | 不建议拦截：属业务基础能力，整域封禁会造成故障 |

## 索引

- [按用途分类](categories.md) · [按拦截判定](verdicts.md) · [误杀黑名单](keep.md) · [厂商索引](vendors.md)

## Alibaba（阿里巴巴）

13 条 · [厂商详情](vendors/alibaba.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `adash.ut.taobao.com` | 阿里 UT 埋点（adash） | 阿里系 UT 埋点的实际上报端点。 | 统计分析 | 拦截·代价 |
| `alicdn.com` | 阿里巴巴 CDN | 淘宝、天猫、支付宝、闲鱼等业务的图片与静态资源 CDN，体量极大。 | 基础服务 | 保留 |
| `alimama.com` | 阿里妈妈投放平台 | 淘宝联盟与直通车的投放管理、素材与点击跳转接口。 | 广告投放 | 拦截 |
| `atanx.alicdn.com` | 阿里妈妈素材 CDN | 存放 Tanx 广告素材，由投放域引用。 | 广告投放 | 拦截 |
| `baichuan-sdk.taobao.com` | 百川电商 SDK | 阿里百川，让第三方 App 直接接入淘宝的商品、交易、购物车能力。 | 基础服务 | 保留 |
| `cnzz.com` | CNZZ 站长统计（友盟旗下） | 面向中小站长的访问统计，采集 PV/UV、来源、地域。 | 统计分析 | 拦截 |
| `miaozhen.com` | 秒针系统（Miaozhen） | 第三方广告监测，做曝光验证、可见性测量与到达率统计，广告主用它给媒体结账。 | 广告测量 | 拦截 |
| `mmstat.com` | 阿里 UT 统计 | 阿里系 App 的埋点上报域（User Track），记录页面浏览、点击、停留时长。 | 统计分析 | 拦截 |
| `tanx.com` | 阿里妈妈 Tanx 广告交易平台 | 阿里的 RTB 广告交易市场，向媒体方提供广告位竞价与素材。 | 广告交易 | 拦截 |
| `taobao.com` | 淘宝主域 | 商品、订单、支付、账号登录的宿主域。 | 基础服务 | 保留 |
| `umeng.co` | 友盟短域 | 友盟的短域名，用于素材与上报的分流。 | 统计分析 | 拦截·代价 |
| `umeng.com` | 友盟+（U-App / U-Push） | 国内使用最广的第三方统计 SDK。 | 统计分析 | 拦截·代价 |
| `umengcloud.com` | 友盟数据上报端点 | U-App 的实际数据上报与配置下发域名，与 umeng.com 互为补充。 | 统计分析 | 拦截·代价 |

## Baidu（百度）

7 条 · [厂商详情](vendors/baidu.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `baidu.com` | 百度主域 | 搜索、账号、网盘、地图、百家号等业务的宿主域。 | 基础服务 | 保留 |
| `baidustatic.com` | 百度静态资源 CDN | 百度各业务的前端静态资源（JS/CSS/图片）分发。 | 基础服务 | 保留 |
| `cpro.baidu.com` | 百度联盟内容推荐广告 | 站内内容推荐位与信息流广告的投放接口，常以「相关推荐」形式出现在正文底部。 | 广告投放 | 拦截 |
| `hm.baidu.com` | 百度统计 | 网站访问统计的采集端点（hm.js 与 /hm.gif），记录 PV/UV、来源、事件。 | 统计分析 | 拦截 |
| `mobads.baidu.com` | 百青藤（百度移动广告） | 面向移动 App 的百度广告联盟接口，提供开屏、插屏、激励视频。 | 广告投放 | 拦截 |
| `pos.baidu.com` | 百度联盟主题推广 | 百度联盟的展示广告位接口，站长嵌入的「百度联盟推广」大多指向这里。 | 广告投放 | 拦截 |
| `tongji.baidu.com` | 百度统计后台 | 统计报表与配置后台，同时承担部分数据上报。 | 统计分析 | 拦截 |

## ByteDance（字节跳动）

18 条 · [厂商详情](vendors/bytedance.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `bytedance.com` | 字节跳动主域 | 企业官网与部分 SDK 的配置、鉴权入口。 | 基础服务 | 保留 |
| `csjplatform.com` | 穿山甲平台域（csj = 穿山甲） | 命名与穿山甲缩写一致，被 OISD 等主流规则库收录，用途指向广告平台服务端； | 广告投放 | 拦截 |
| `dm.bytedance.com` | 字节数据管理平台（DMP） | 人群包与用户标签的同步接口，服务于广告定向。 | 行为追踪 | 拦截·代价 |
| `is.snssdk.com` | 字节设备注册与服务发现 | 设备注册、服务端地址下发，App 启动阶段的第一跳。 | 基础服务 | 保留 |
| `isnssdk.com` | TikTok / 海外字节核心 API | snssdk.com 的海外对应域，承载 TikTok 的业务接口。 | 基础服务 | 保留 |
| `log.snssdk.com` | 字节日志上报 | App 运行日志与行为埋点的批量上报通道。 | 行为追踪 | 拦截·代价 |
| `mon.snssdk.com` | 字节监控上报 | 性能、卡顿、网络质量等监控数据的上报端点。 | 统计分析 | 拦截·代价 |
| `mssdk.bytedance.com` | 字节通用 SDK 服务 | 提供设备标识、SDK 配置、灰度开关等通用能力，被抖音、头条、番茄等多款 App 共用。 | 行为追踪 | 拦截·代价 |
| `pangle.io` | Pangle（穿山甲海外版） | 面向海外开发者的广告变现平台，提供广告请求、报表与素材接口。 | 广告投放 | 拦截 |
| `pangolin-sdk-toutiao-b.com` | 穿山甲备用域（B） | 穿山甲主域不可用时的轮换域名，功能与主域完全等价。 | 广告投放 | 拦截 |
| `pangolin-sdk-toutiao.com` | 穿山甲（Pangle）广告 SDK | 国内穿山甲 SDK 的服务端入口，承担广告请求、竞价、配置下发与素材地址返回。 | 广告投放 | 拦截 |
| `pangolin-sdk-toutiao1.com` | 穿山甲备用域（1~4） | 穿山甲按序号轮换的一组域名，-toutiao1 至 -toutiao4 同时存在，SDK 会在失败时依次重试。 | 广告投放 | 拦截 |
| `pangolin-x.com` | 穿山甲关联域 | 穿山甲体系内的辅助域，用于配置拉取与请求分流，被主流规则库普遍收录。 | 广告投放 | 拦截 |
| `pangolin.snssdk.com` | 穿山甲（snssdk 下接口） | 挂在 snssdk.com 主域下的穿山甲广告接口，与抖音业务接口共用根域，必须按主机名拦。 | 广告投放 | 拦截 |
| `pangolin16.isnssdk.com` | 穿山甲国际版接口 | TikTok / 海外字节系 App 的穿山甲广告接口。 | 广告投放 | 拦截 |
| `pstatp.com` | 字节内容 CDN | 图片、视频、头像、封面等静态资源的 CDN。 | 基础服务 | 保留 |
| `snssdk.com` | 抖音 / 今日头条核心 API | 内容流、账号、支付、直播等业务接口的宿主域，抖音与头条 App 的主干。 | 基础服务 | 保留 |
| `tnc3-bjlgy.snssdk.com` | 字节 CDN 边缘节点（tnc 集群） | 字节的 CDN 边缘节点。 | 基础服务 | 保留 |

## Google（谷歌）

14 条 · [厂商详情](vendors/google.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `2mdn.net` | DoubleClick Studio 素材 CDN | 存放 DoubleClick 广告素材（图片、视频、富媒体创意），由广告投放域引用。 | 广告投放 | 拦截 |
| `adservice.google.com` | AdMob / AdX 移动端广告请求 | 移动 App 内广告 SDK 的请求入口，常见路径 /adsid/integrator.js 与 /pagead/。 | 广告投放 | 拦截 |
| `app-measurement.com` | Firebase Analytics（GA4 for Firebase） | 移动 App 的 Firebase 埋点上报端点，负责事件、用户属性、受众同步。 | 统计分析 | 拦截·代价 |
| `crashlytics.com` | Firebase Crashlytics | 崩溃与 ANR 上报，附带设备型号、系统版本、堆栈与最近操作路径。 | 崩溃监控 | 拦截·代价 |
| `doubleclick.net` | Google Ad Manager / DoubleClick（DFP） | Google 展示广告的核心投放域。 | 广告投放 | 拦截 |
| `firebaseinstallations.googleapis.com` | Firebase Installations | 生成并维护 Firebase Installation ID（FID），Analytics、Remote Config、Cloud Messaging 都依赖它做实例标识。 | 行为追踪 | 拦截·代价 |
| `google-analytics.com` | Google Analytics（UA / GA4） | GA 的数据采集端点，analytics.js、gtag/js 与 /g/collect 上报都指向这里。 | 统计分析 | 拦截 |
| `google.com` | Google 主域 | 搜索、账号、登录、验证码、地图等核心服务的宿主域。 | 基础服务 | 保留 |
| `googleadservices.com` | Google Ads 点击与转化跟踪 | 广告点击后的跳转与转化归因（pagead/aclk、pagead/conversion）。 | 广告投放 | 拦截 |
| `googleapis.com` | Google APIs 公共入口 | 承载 Firebase、地图、登录、云服务的统一 API 网关，大量 App 的基础能力都在这个域下。 | 基础服务 | 保留 |
| `googlesyndication.com` | AdSense / AdMob | pagead2.googlesyndication.com 下发广告脚本，tpc.googlesyndication.com 存放广告素材，googleads.g.double… | 广告投放 | 拦截 |
| `googletagmanager.com` | Google Tag Manager（GTM） | 标签管理器容器。 | 行为追踪 | 拦截·代价 |
| `googletagservices.com` | Google Publisher Tag（GPT） | 网页广告位的调度脚本（gpt.js），负责向 Ad Manager 请求广告并渲染到页面。 | 广告投放 | 拦截 |
| `gstatic.com` | Google 静态资源 CDN | 提供字体、JS 库、公共静态资源。 | 基础服务 | 保留 |

## Kuaishou（快手）

3 条 · [厂商详情](vendors/kuaishou.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `adkwai.com` | 快手广告（磁力引擎） | 快手磁力引擎的广告投放域，承担广告请求、竞价与素材地址下发，同时也作为联盟广告的落地域。 | 广告投放 | 拦截 |
| `gifshow.com` | 快手内容 CDN / 旧版接口 | 快手（原快手 GIF 秀）的视频与封面 CDN，仍被大量客户端引用。 | 基础服务 | 保留 |
| `kuaishou.com` | 快手主域 | 快手 App 与网页版的账号、内容、直播接口宿主域。 | 基础服务 | 保留 |

## Meta（前 Facebook）

6 条 · [厂商详情](vendors/meta.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `an.facebook.com` | Meta Audience Network | 面向第三方 App 的横幅、插屏、激励视频广告请求与素材下发。 | 广告投放 | 拦截 |
| `connect.facebook.net` | Facebook JS SDK / Pixel | 网页端 SDK 宿主。 | 行为追踪 | 拦截·代价 |
| `facebook.com` | Facebook 主域 | 账号登录、OAuth 授权、分享、Messenger 跳转的宿主域。 | 基础服务 | 保留 |
| `facebook.net` | Facebook 静态资源域 | 承载 connect.facebook.net 等前端 SDK 资源。 | 基础服务 | 保留 |
| `fbcdn.net` | Facebook 内容 CDN | 头像、图片、视频、静态资源分发。 | 基础服务 | 保留 |
| `graph.facebook.com` | Facebook Graph API | Graph API 统一入口。 | 行为追踪 | 部分 |

## Tencent（腾讯）

9 条 · [厂商详情](vendors/tencent.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `beacon.qq.com` | 腾讯灯塔（Beacon） | 客户端质量与行为数据上报，覆盖卡顿、崩溃、页面耗时。 | 统计分析 | 拦截·代价 |
| `bugly.qq.com` | 腾讯 Bugly | 崩溃、ANR、卡顿上报与热更新下发，国内 App 使用极广。 | 崩溃监控 | 拦截·代价 |
| `e.qq.com` | 广点通曝光与点击上报 | 广告曝光、点击、转化的事件上报端点，广告请求成功后紧接着打这里。 | 广告投放 | 拦截 |
| `gdt.qq.com` | 广点通 / 腾讯广告 | 腾讯广告（原广点通）的广告请求与投放接口，微信、QQ、腾讯视频、优量汇的广告位都从这里取量。 | 广告投放 | 拦截 |
| `gtimg.com` | 腾讯图片 CDN | 腾讯全系产品的图片与静态资源 CDN，头像、表情、封面、新闻配图都在这里。 | 基础服务 | 保留 |
| `pgdt.gtimg.com` | 广点通素材 CDN | 存放广点通广告的图片与视频素材，由投放域引用。 | 广告投放 | 拦截 |
| `pingjs.qq.com` | 腾讯前端性能监控 | 页面性能指标（加载耗时、JS 错误）的采集脚本与上报端点。 | 统计分析 | 拦截 |
| `qq.com` | 腾讯主域 | QQ 登录、微信开放平台回调、腾讯文档、邮箱等业务的宿主域。 | 基础服务 | 保留 |
| `ta.qq.com` | 腾讯分析（TA） | 网页与 H5 的访问统计、来源分析、转化漏斗采集端点。 | 统计分析 | 拦截 |

## 产品分析

7 条 · [厂商详情](vendors/product-analytics.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `amplitude.com` | Amplitude | 与 Mixpanel 同类的行为分析平台，移动端与网页端都常用。 | 统计分析 | 拦截 |
| `fullstory.com` | FullStory | 全量会话回放，把用户在页面上的所有操作录成可检索的「录像」。 | 统计分析 | 拦截 |
| `heap.io` | Heap | 全量自动采集（capture everything），不需要预先埋点。 | 统计分析 | 拦截 |
| `hotjar.com` | Hotjar | 会话录制、热图与问卷，能回放用户在你站点上的每一次点击与滚动。 | 统计分析 | 拦截 |
| `mixpanel.com` | Mixpanel | 事件级产品分析，记录每一次点击、注册、付费，做漏斗与留存。 | 统计分析 | 拦截 |
| `segment.com` | Segment（Twilio） | 客户数据平台（CDP）。 | 行为追踪 | 拦截·代价 |
| `segment.io` | Segment 采集端点 | Segment 的实际数据上报域（api.segment.io），与 segment.com 分工不同。 | 行为追踪 | 拦截·代价 |

## 京东（JD）

5 条 · [厂商详情](vendors/jd.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `ads-union.jd.com` | 京东联盟广告 | 京东京准通联盟的广告投放与素材下发，站外媒体挂的京东商品推广位走这里。 | 广告投放 | 拦截 |
| `blackhole.m.jd.com` | 京东客户端埋点 | 京东 App 的行为日志收集端点（内部叫「黑洞」），记录页面路径、点击、曝光。 | 统计分析 | 拦截·代价 |
| `dsp-x.jd.com` | 京东 DSP | 京东的程序化广告投放平台（需求方平台），负责站外精准投放与竞价。 | 广告交易 | 拦截 |
| `jd.com` | 京东主域 | 商品、订单、支付、账号登录的宿主域。 | 基础服务 | 保留 |
| `mars.jd.com` | 京东内部服务（代号 Mars） | 京东内部以行星/神话命名的服务之一（同族还有 uranus、mercury、hermes、cactus）。 | 基础服务 | 保留 |

## 国产终端厂商

8 条 · [厂商详情](vendors/cn-oem.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `ad.xiaomi.com` | 小米广告（MIUI 广告） | MIUI 系统广告位（负一屏、天气、文件夹推荐）的广告请求与素材下发。 | 广告投放 | 拦截 |
| `adsfs.oppomobile.com` | OPPO 广告素材 CDN | ColorOS 系统广告与 OPPO 联盟广告的素材分发。 | 广告投放 | 拦截 |
| `hicloud.com` | 华为云 / HMS 基础设施 | 华为云服务、HMS Core 能力、云空间与推送的基础设施域。 | 基础服务 | 保留 |
| `metrics.data.hicloud.com` | 华为分析 / HMS 遥测 | 华为分析服务（Analytics Kit）与系统遥测的数据上报端点。 | 统计分析 | 拦截·代价 |
| `mistat.xiaomi.com` | 小米统计（MIUI 遥测） | MIUI/HyperOS 与小米系 App 的使用统计、广告归因、设备画像上报。 | 统计分析 | 拦截·代价 |
| `oppomobile.com` | OPPO 系统服务 / 推送 | ColorOS 系统服务、OPPO 推送（PUSH）与账号体系的宿主域。 | 基础服务 | 保留 |
| `vivo.com.cn` | vivo 系统服务 / 推送 | Funtouch OS / OriginOS 系统服务、vivo 推送与账号体系。 | 基础服务 | 保留 |
| `xiaomi.com` | 小米账号 / 云服务 | 小米账号登录、云服务、应用商店、系统更新的宿主域。 | 基础服务 | 保留 |

## 国内广告联盟

4 条 · [厂商详情](vendors/cn-adnet.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `adview.cn` | AdView 移动广告平台 | 移动广告联盟，为中小 App 提供 banner、插屏、开屏广告的请求与素材接口。 | 广告投放 | 拦截 |
| `domob.cn` | 多盟（Domob） | 移动广告联盟与 DSP，提供广告投放、素材与点击跳转。 | 广告投放 | 拦截 |
| `gridsum.com` | 国双（Gridsum） | 网站与广告的第三方数据分析、监测与归因，常见于大型企业站点。 | 广告测量 | 拦截 |
| `mediav.com` | MediaV（聚胜万合） | 效果广告投放与精准定向平台，电商与游戏行业使用较多。 | 广告投放 | 拦截 |

## 国内第三方 SDK

8 条 · [厂商详情](vendors/cn-sdk.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `getui.com` | 个推（Getui） | 个推消息推送服务，同时提供用户画像与数据服务（个推大数据）。 | 推送消息 | 保留 |
| `growingio.com` | GrowingIO | 无埋点采集与热图分析，自动抓取页面元素与点击行为。 | 统计分析 | 拦截 |
| `igexin.com` | 个推旧域 | 个推早期域名，老版本 SDK 仍在引用。 | 推送消息 | 保留 |
| `jiguang.cn` | 极光 JPush / JVerification | 极光推送的长连接与 API 入口，同时承载一键登录（JVerification）与统计（JAnalytics）。 | 推送消息 | 保留 |
| `jpush.cn` | 极光推送短域 | JPush 的短域名，用于推送通道与消息回执。 | 推送消息 | 保留 |
| `mob.com` | MobTech ShareSDK / 秒验 | 社交分享与第三方登录（ShareSDK）、本机号码一键登录（秒验）。 | 基础服务 | 保留 |
| `sensorsdata.cn` | 神策数据（Sensors Analytics） | 埋点上报主域（/sa、/sdk），记录事件、页面、用户属性。 | 统计分析 | 拦截·代价 |
| `talkingdata.com` | TalkingData | 移动统计与广告归因，同时提供数据交易服务（TalkingData AdTracking）。 | 统计分析 | 拦截 |

## 国内视频与音乐平台

14 条 · [厂商详情](vendors/cn-video.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `ad.api.3g.youku.com` | 优酷移动端广告接口 | 优酷 App 的移动端广告请求接口，负责开屏、信息流与播放器贴片广告。 | 广告投放 | 拦截 |
| `ad.m.iqiyi.com` | 爱奇艺移动端广告 | 爱奇艺 App 的移动广告请求入口，覆盖开屏、贴片与信息流。 | 广告投放 | 拦截 |
| `ads.service.kugou.com` | 酷狗广告服务 | 酷狗音乐的广告请求服务，负责开屏、播放页 banner 与音频贴片。 | 广告投放 | 拦截 |
| `adsfile.bssdlbig.kugou.com` | 酷狗广告素材 CDN | 存放广告素材的 CDN 节点（bssdlbig 为酷狗自建分发网络）。 | 广告投放 | 拦截 |
| `atm.youku.com` | 优酷广告投放系统（ATM） | 优酷的广告投放与计数中枢。 | 广告投放 | 拦截 |
| `cloudpush.iqiyi.com` | 爱奇艺推送通道 | 爱奇艺的消息推送服务，负责更新提醒、会员到期、互动通知。 | 推送消息 | 保留 |
| `da.mgtv.com` | 芒果TV 数据统计 | 芒果TV 的数据采集中枢。 | 统计分析 | 拦截·代价 |
| `iqiyi.com` | 爱奇艺主域 | 爱奇艺的内容、播放、会员与账号接口宿主域。 | 基础服务 | 保留 |
| `kugou.com` | 酷狗音乐主域 | 酷狗音乐的曲库、播放、账号接口宿主域。 | 基础服务 | 保留 |
| `log.stat.kugou.com` | 酷狗统计日志 | 酷狗的行为与播放统计上报，配合 log.web、logtj 等子域使用。 | 统计分析 | 拦截·代价 |
| `mbdlog.iqiyi.com` | 爱奇艺埋点日志 | 爱奇艺的客户端行为日志上报（MBD 埋点体系），记录播放行为与页面路径。 | 统计分析 | 拦截·代价 |
| `mgtv.com` | 芒果TV 主域 | 芒果TV 的内容、播放、会员接口宿主域。 | 基础服务 | 保留 |
| `ut.youku.com` | 优酷用户行为统计（UT） | 阿里系统一的 UT 埋点上报域，adashx.ut 与 h-adashx.ut 记录播放、点击、停留时长。 | 统计分析 | 拦截·代价 |
| `youku.com` | 优酷主域 | 优酷的内容分发、播放、会员与登录接口宿主域。 | 基础服务 | 保留 |

## 国内门户与搜索引擎

20 条 · [厂商详情](vendors/cn-portal.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `163.com` | 网易主域 | 网易新闻、邮箱、云音乐、游戏的账号与内容接口宿主域。 | 基础服务 | 保留 |
| `360.cn` | 360 主域 | 360 安全卫士、浏览器、手机助手的账号与更新接口宿主域。 | 基础服务 | 保留 |
| `ad.360.cn` | 360 广告投放 | 360 广告平台的服务端，同族还有 ad.jia / ad.life / ad.iot 等按行业拆分的子域。 | 广告投放 | 拦截 |
| `ad.sina.com.cn` | 新浪广告投放 | 新浪门户的广告位投放。 | 广告投放 | 拦截 |
| `ad.sohu.com` | 搜狐广告投放 | 搜狐门户的广告投放入口，同族还有 ads / adnet 两个子域。 | 广告投放 | 拦截 |
| `adgeo.163.com` | 网易广告地域定向 | 按 IP 与地域做广告定向投放的服务。 | 广告投放 | 拦截 |
| `adsence.sogou.com` | 搜狗联盟 | 搜狗联盟（站外广告位）的投放与素材下发。 | 广告投放 | 拦截 |
| `analytics.163.com` | 网易分析 | 网易系产品的行为统计上报。 | 统计分析 | 拦截 |
| `aty.sohu.com` | 搜狐广告点击统计 | 广告点击与到达率的统计端点，hd.sohu.com 下有对应的 aty.hd 子域。 | 广告测量 | 拦截 |
| `beacon.sina.com.cn` | 新浪埋点 | 页面行为与曝光埋点的上报端点。 | 行为追踪 | 拦截 |
| `click.stat.hao.360.cn` | 360 导航点击统计 | 360 导航站（hao.360.cn）的点击与来源统计。 | 广告测量 | 拦截 |
| `counter.sina.com.cn` | 新浪计数 | 广告与页面的曝光计数服务，广告主用它核对投放量。 | 广告测量 | 拦截 |
| `cpc.sogou.com` | 搜狗竞价广告 | 搜狗的竞价推广（CPC）投放接口，搜索结果里的推广位由它下发。 | 广告投放 | 拦截 |
| `crash.163.com` | 网易崩溃上报 | 网易系 App 的崩溃与异常上报（同族还有 crashlytics.163.com）。 | 崩溃监控 | 拦截·代价 |
| `e.sogou.com` | 搜狗点击统计 | 广告点击跳转与计费统计端点。 | 广告测量 | 拦截 |
| `fenxi.360.cn` | 360 分析 | 360 的行为分析上报（fenxi 即「分析」的拼音）。 | 统计分析 | 拦截·代价 |
| `fp-upload.dun.163.com` | 网易易盾风控 | 易盾的设备指纹与风控数据上传。 | 行为追踪 | 保留 |
| `sina.com.cn` | 新浪主域 | 新浪新闻、微博登录、邮箱等业务的宿主域。 | 基础服务 | 保留 |
| `sogou.com` | 搜狗主域 | 搜狗搜索、输入法、浏览器的宿主域。 | 基础服务 | 保留 |
| `sohu.com` | 搜狐主域 | 搜狐新闻、视频、邮箱的宿主域。 | 基础服务 | 保留 |

## 国际广告网络与聚合

16 条 · [厂商详情](vendors/adnet-global.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `adcolony.com` | AdColony（Digital Turbine） | 高清视频广告网络，以激励视频为主，2021 年被 Digital Turbine 收购。 | 广告投放 | 拦截 |
| `applovin.com` | AppLovin MAX / AXON | 广告聚合平台 MAX 与自有广告网络 AXON 的服务端，负责广告请求、竞价、瀑布流调度。 | 聚合中介 | 拦截 |
| `applvn.com` | AppLovin 短域 | AppLovin 的短域名，承担事件上报与素材地址分流，常被漏拦。 | 广告投放 | 拦截 |
| `chartboost.com` | Chartboost | 游戏内广告网络与交叉推广平台。 | 广告投放 | 拦截 |
| `fyber.com` | Fyber（Digital Turbine） | 广告聚合与交易平台，提供 Offer Wall 与中介服务。 | 聚合中介 | 拦截 |
| `inmobi.com` | InMobi | 全球移动广告网络，覆盖印度、东南亚市场较多。 | 广告投放 | 拦截 |
| `ironsrc.com` | ironSource（Unity LevelPlay） | ironSource 广告聚合与自有网络的统一入口，2022 年被 Unity 收购后与 LevelPlay 合并。 | 聚合中介 | 拦截 |
| `liftoff.io` | Liftoff | 效果广告与再营销平台，服务端接口与素材分发。 | 广告投放 | 拦截 |
| `mintegral.com` | Mintegral（汇量科技） | 全球移动广告平台，以激励视频与试玩广告见长，国内出海 App 使用极多。 | 广告投放 | 拦截 |
| `mintegral.net` | Mintegral 备用域 | 与 mintegral.com 等价的素材与请求域，用于分流与容灾。 | 广告投放 | 拦截 |
| `mopub.com` (停用) | MoPub（已关停） | Twitter 旗下的广告聚合平台，2022 年 12 月停止服务，流量迁移至 AppLovin MAX。 | 聚合中介 | 拦截 |
| `supersonicads.com` | ironSource 旧域 | ironSource 早期域名，老版本 SDK 仍会请求。 | 广告投放 | 拦截 |
| `tapjoy.com` | Tapjoy | 激励视频与积分墙，用户完成任务换取游戏内奖励。 | 广告投放 | 拦截 |
| `unity3d.com` | Unity 引擎 / 服务 | Unity 引擎的资源、License 校验、云服务入口。 | 基础服务 | 保留 |
| `unityads.unity3d.com` | Unity Ads | Unity Ads 的广告请求与展示接口，大量休闲游戏的主要变现方式。 | 广告投放 | 拦截 |
| `vungle.com` | Vungle（Liftoff） | 视频广告网络，主打激励视频与插屏，2021 年被 Liftoff 收购。 | 广告投放 | 拦截 |

## 国际程序化广告与监测

20 条 · [厂商详情](vendors/adtech-global.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `33across.com` | 33Across | 以身份识别与受众扩展为主的广告技术公司。 | 广告交易 | 拦截 |
| `adform.net` | Adform | 北欧为主的广告服务器、DSP 与 DMP 一体化平台。 | 广告投放 | 拦截 |
| `adnxs.com` | Xandr（原 AppNexus） | 微软旗下的程序化广告交易平台，ib.adnxs.com 是最常见的竞价端点。 | 广告交易 | 拦截 |
| `adsrvr.org` | The Trade Desk | 需求方平台（DSP）的竞价与用户匹配端点，常出现在网页的同步像素里。 | 广告交易 | 拦截 |
| `amazon-adsystem.com` | Amazon Advertising | 亚马逊广告平台，既投自家站点也做站外程序化投放。 | 广告投放 | 拦截 |
| `casalemedia.com` | Index Exchange | 老牌 SSP，以 header bidding 接入为主。 | 广告交易 | 拦截 |
| `comscore.com` | Comscore 主域 | Comscore 的配置与报表域，部分采集脚本也从这里下发。 | 广告测量 | 拦截 |
| `criteo.com` | Criteo | 重定向广告网络。 | 广告投放 | 拦截 |
| `criteo.net` | Criteo 投放与素材域 | Criteo 的广告投放、竞价与素材分发域，与 .com 分工不同。 | 广告投放 | 拦截 |
| `magnite.com` | Magnite | Magnite 现行主域，承担 SSP 竞价与素材分发。 | 广告交易 | 拦截 |
| `moatads.com` | Oracle Moat | 广告可见性与无效流量测量，验证广告是否真的被人看到。 | 广告测量 | 拦截 |
| `openx.net` | OpenX | 独立广告交易平台，同时提供 SSP 与 Ad Exchange 能力。 | 广告交易 | 拦截 |
| `outbrain.com` | Outbrain | 与 Taboola 同类的内容推荐广告网络。 | 广告投放 | 拦截 |
| `pubmatic.com` | PubMatic | 卖方平台（SSP），帮媒体把广告位拿到交易所竞价。 | 广告交易 | 拦截 |
| `quantserve.com` | Quantcast | 受众测量与程序化投放，pixel.quantserve.com 是最常见的采集端点。 | 广告测量 | 拦截 |
| `rubiconproject.com` | Magnite（原 Rubicon Project） | 大型 SSP，2020 年与 Telaria 合并后更名 Magnite。 | 广告交易 | 拦截 |
| `scorecardresearch.com` | Comscore | 受众测量与流量统计，用像素记录站点访问人群特征。 | 广告测量 | 拦截 |
| `smartadserver.com` | Equativ（原 Smart AdServer） | 欧洲为主的广告服务器与 SSP。 | 广告投放 | 拦截 |
| `taboola.com` | Taboola | 内容推荐广告网络，网页底部「你可能感兴趣」「推荐阅读」的赞助内容。 | 广告投放 | 拦截 |
| `teads.tv` | Teads | 外播视频广告（outstream video），把视频广告插进图文正文中间。 | 广告投放 | 拦截 |

## 崩溃与性能监控

4 条 · [厂商详情](vendors/observability.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `bugsnag.com` | Bugsnag（SmartBear） | 异常与稳定性监控，按错误聚合与告警。 | 崩溃监控 | 拦截·代价 |
| `instabug.com` | Instabug | 应用内反馈 SDK，收集崩溃、卡顿、网络日志，并把用户反馈与现场数据一起上报。 | 崩溃监控 | 拦截·代价 |
| `newrelic.com` | New Relic | 应用性能监控（APM），采集请求耗时、数据库调用、错误率。 | 崩溃监控 | 拦截·代价 |
| `sentry.io` | Sentry | 崩溃、异常、性能追踪上报。 | 崩溃监控 | 拦截·代价 |

## 归因与深度链接

6 条 · [厂商详情](vendors/attribution.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `adjust.com` | Adjust | 与 AppsFlyer 同类的归因平台，欧洲市场占有率较高，同时提供防作弊。 | 安装归因 | 拦截 |
| `appsflyer.com` | AppsFlyer | 移动归因与营销分析的事实标准。 | 安装归因 | 拦截·代价 |
| `branch.io` | Branch | 深度链接与归因一体。 | 安装归因 | 拦截·代价 |
| `kochava.com` | Kochava | 归因与受众平台，游戏与工具类 App 使用较多。 | 安装归因 | 拦截 |
| `singular.net` | Singular | 归因与营销 ETL 平台，把多家渠道数据汇总做 ROI 分析。 | 安装归因 | 拦截 |
| `tenjin.com` | Tenjin | 面向独立游戏开发者的轻量归因与收入分析。 | 安装归因 | 拦截 |

## 营销自动化与推送

7 条 · [厂商详情](vendors/engagement.md)

| 域名 | 产品 / SDK | 用途 | 分类 | 判定 |
| --- | --- | --- | --- | --- |
| `airship.com` | Airship（原 Urban Airship） | 推送基础设施与消息编排，服务大量欧美媒体与零售 App。 | 推送消息 | 拦截·代价 |
| `appboy.com` | Braze 旧域（Appboy） | Braze 改名前的域名，老版本 SDK 仍在引用。 | 推送消息 | 拦截·代价 |
| `braze.com` | Braze | 跨渠道营销自动化，统一管理推送、站内信、邮件与短信的触达节奏。 | 推送消息 | 拦截·代价 |
| `clevertap.com` | CleverTap | 用户分群与营销自动化，主打推送与应用内消息。 | 推送消息 | 拦截·代价 |
| `flurry.com` | Flurry（Yahoo） | 移动应用分析与广告归因，Yahoo 旗下的老牌移动统计 SDK。 | 统计分析 | 拦截 |
| `onesignal.com` | OneSignal | 免费的跨平台推送服务，中小开发者常用。 | 推送消息 | 拦截·代价 |
| `pushwoosh.com` | Pushwoosh | 推送与营销自动化平台，东欧市场较多。 | 推送消息 | 拦截·代价 |

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。