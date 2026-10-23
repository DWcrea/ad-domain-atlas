# 误杀黑名单：这些域名不要拦

规则库里混进这些域名，会造成 App 白屏、登录失败、推送收不到、图片加载不出来。很多「广告拦截后 App 坏了」的报障都出在这里。


共 44 条。

| 域名 | 厂商 | 为什么不能拦 | 拦了会怎样 |
| --- | --- | --- | --- |
| `unity3d.com` | 国际广告网络与聚合 | Unity 引擎的资源、License 校验、云服务入口。 | Unity 打包的游戏可能无法校验授权或加载资源，出现启动失败。 |
| `alicdn.com` | Alibaba | 淘宝、天猫、支付宝、闲鱼等业务的图片与静态资源 CDN，体量极大。 | 阿里系 App 与网页大面积白图、样式丢失，基本不可用。 |
| `baichuan-sdk.taobao.com` | Alibaba | 阿里百川，让第三方 App 直接接入淘宝的商品、交易、购物车能力。 | 接入百川的 App 会出现商品打不开、加购失败、跳转淘宝失败。 |
| `taobao.com` | Alibaba | 商品、订单、支付、账号登录的宿主域。 | 淘宝打不开、下不了单、付不了款。 |
| `baidu.com` | Baidu | 搜索、账号、网盘、地图、百家号等业务的宿主域。 | 百度搜索打不开、百度网盘无法登录，大量依赖百度 OAuth 的 App 登录失效。 |
| `baidustatic.com` | Baidu | 百度各业务的前端静态资源（JS/CSS/图片）分发。 | 百度系页面样式与交互脚本加载失败，页面错乱。 |
| `bytedance.com` | ByteDance | 企业官网与部分 SDK 的配置、鉴权入口。 | 部分字节系 App 的 SDK 初始化与配置拉取失败，可能卡启动。 |
| `is.snssdk.com` | ByteDance | 设备注册、服务端地址下发，App 启动阶段的第一跳。 | App 启动时拿不到服务端地址，可能卡在启动页或反复重试。 |
| `isnssdk.com` | ByteDance | snssdk.com 的海外对应域，承载 TikTok 的业务接口。 | TikTok 无法加载内容与登录。 |
| `pstatp.com` | ByteDance | 图片、视频、头像、封面等静态资源的 CDN。 | 字节系 App 与内嵌头条内容的第三方 App 大面积白图、视频无法播放。 |
| `snssdk.com` | ByteDance | 内容流、账号、支付、直播等业务接口的宿主域，抖音与头条 App 的主干。 | 抖音、今日头条无法刷新内容、无法登录、无法播放视频，基本等于 App 报废。 |
| `tnc3-bjlgy.snssdk.com` | ByteDance | 字节的 CDN 边缘节点。 | 拦掉单个节点基本无效（CDN 会自动切到其他节点），但可能让部分图片或接口请求变慢、失败。 |
| `hicloud.com` | 国产终端厂商 | 华为云服务、HMS Core 能力、云空间与推送的基础设施域。 | 华为手机 HMS 服务异常，推送、云空间、应用市场可能集体失效。 |
| `oppomobile.com` | 国产终端厂商 | ColorOS 系统服务、OPPO 推送（PUSH）与账号体系的宿主域。 | OPPO 手机收不到系统推送，账号登录异常。 |
| `vivo.com.cn` | 国产终端厂商 | Funtouch OS / OriginOS 系统服务、vivo 推送与账号体系。 | vivo 手机推送与账号登录异常。 |
| `xiaomi.com` | 国产终端厂商 | 小米账号登录、云服务、应用商店、系统更新的宿主域。 | 小米手机无法登录账号、应用商店打不开、系统更新失败。 |
| `163.com` | 国内门户与搜索引擎 | 网易新闻、邮箱、云音乐、游戏的账号与内容接口宿主域。 | 网易全系产品无法登录，邮箱打不开。 |
| `360.cn` | 国内门户与搜索引擎 | 360 安全卫士、浏览器、手机助手的账号与更新接口宿主域。 | 360 系软件无法登录、无法更新。 |
| `fp-upload.dun.163.com` | 国内门户与搜索引擎 | 易盾的设备指纹与风控数据上传。 | 部分 App 的验证码、登录风控可能降级，极端情况下验证过不去。 |
| `sina.com.cn` | 国内门户与搜索引擎 | 新浪新闻、微博登录、邮箱等业务的宿主域。 | 新浪新闻打不开，微博网页版登录失败。 |
| `sogou.com` | 国内门户与搜索引擎 | 搜狗搜索、输入法、浏览器的宿主域。 | 搜狗搜索与输入法云同步失效。 |
| `sohu.com` | 国内门户与搜索引擎 | 搜狐新闻、视频、邮箱的宿主域。 | 搜狐各业务打不开。 |
| `getui.com` | 国内第三方 SDK | 个推消息推送服务，同时提供用户画像与数据服务（个推大数据）。 | 使用个推的 App 收不到推送，部分 App 的启动引导依赖推送注册会卡住。 |
| `igexin.com` | 国内第三方 SDK | 个推早期域名，老版本 SDK 仍在引用。 | 老版本 App 推送失效。 |
| `jiguang.cn` | 国内第三方 SDK | 极光推送的长连接与 API 入口，同时承载一键登录（JVerification）与统计（JAnalytics）。 | App 收不到推送通知；用极光做一键登录的 App 会登录失败。 |
| `jpush.cn` | 国内第三方 SDK | JPush 的短域名，用于推送通道与消息回执。 | 同 jiguang.cn。 |
| `mob.com` | 国内第三方 SDK | 社交分享与第三方登录（ShareSDK）、本机号码一键登录（秒验）。 | App 的微信/QQ 分享与一键登录按钮失效，登录页可能卡住。 |
| `cloudpush.iqiyi.com` | 国内视频与音乐平台 | 爱奇艺的消息推送服务，负责更新提醒、会员到期、互动通知。 | 爱奇艺收不到任何推送通知。 |
| `iqiyi.com` | 国内视频与音乐平台 | 爱奇艺的内容、播放、会员与账号接口宿主域。 | 爱奇艺无法播放与登录。 |
| `kugou.com` | 国内视频与音乐平台 | 酷狗音乐的曲库、播放、账号接口宿主域。 | 酷狗无法播放与登录。 |
| `mgtv.com` | 国内视频与音乐平台 | 芒果TV 的内容、播放、会员接口宿主域。 | 芒果TV 无法播放与登录。 |
| `youku.com` | 国内视频与音乐平台 | 优酷的内容分发、播放、会员与登录接口宿主域。 | 优酷无法播放视频、无法登录，App 与网页基本报废。 |
| `google.com` | Google | 搜索、账号、登录、验证码、地图等核心服务的宿主域。 | 无法登录 Google 账号、无法通过 reCAPTCHA 验证，大量第三方 App 的 Google 登录一并失效。 |
| `googleapis.com` | Google | 承载 Firebase、地图、登录、云服务的统一 API 网关，大量 App 的基础能力都在这个域下。 | 整域封禁会导致 Google 登录、地图、Firebase 推送、Play 服务集体失效，App 可能直接白屏或闪退。 |
| `gstatic.com` | Google | 提供字体、JS 库、公共静态资源。 | 页面字体回退、部分站点 JS 加载失败、布局错乱。 |
| `jd.com` | 京东 | 商品、订单、支付、账号登录的宿主域。 | 京东打不开、下不了单、付不了款。 |
| `mars.jd.com` | 京东 | 京东内部以行星/神话命名的服务之一（同族还有 uranus、mercury、hermes、cactus）。 | 用途未公开，无法确认与广告有关；拦掉可能让京东某个页面模块拉不到数据。 |
| `gifshow.com` | Kuaishou | 快手（原快手 GIF 秀）的视频与封面 CDN，仍被大量客户端引用。 | 快手视频封面与播放地址加载失败。 |
| `kuaishou.com` | Kuaishou | 快手 App 与网页版的账号、内容、直播接口宿主域。 | 快手无法登录与刷新内容。 |
| `facebook.com` | Meta | 账号登录、OAuth 授权、分享、Messenger 跳转的宿主域。 | 所有「用 Facebook 登录」的 App 与网站失效，分享按钮报错，OAuth 回调失败。 |
| `facebook.net` | Meta | 承载 connect.facebook.net 等前端 SDK 资源。 | 网页内嵌的 Facebook 组件（登录、评论、分享）全部失效。 |
| `fbcdn.net` | Meta | 头像、图片、视频、静态资源分发。 | 图片与视频大面积加载失败，社交类 App 界面破版。 |
| `gtimg.com` | Tencent | 腾讯全系产品的图片与静态资源 CDN，头像、表情、封面、新闻配图都在这里。 | 微信、QQ、腾讯新闻大面积白图，界面破版。 |
| `qq.com` | Tencent | QQ 登录、微信开放平台回调、腾讯文档、邮箱等业务的宿主域。 | QQ / 微信登录失效，大量第三方 App 的「QQ 登录」按钮报错。 |

## 使用建议

把上表的域名转成放行规则，加在过滤器的**最前面**（AdGuard 的自定义规则里`@@||domain^` 即白名单），可以抵消上游规则库的误杀：

```text
@@||163.com^
@@||360.cn^
@@||alicdn.com^
@@||baichuan-sdk.taobao.com^
@@||baidu.com^
@@||baidustatic.com^
@@||bytedance.com^
@@||cloudpush.iqiyi.com^
@@||facebook.com^
@@||facebook.net^
@@||fbcdn.net^
@@||fp-upload.dun.163.com^
@@||getui.com^
@@||gifshow.com^
@@||google.com^
@@||googleapis.com^
@@||gstatic.com^
@@||gtimg.com^
@@||hicloud.com^
@@||igexin.com^
@@||iqiyi.com^
@@||is.snssdk.com^
@@||isnssdk.com^
@@||jd.com^
@@||jiguang.cn^
@@||jpush.cn^
@@||kuaishou.com^
@@||kugou.com^
@@||mars.jd.com^
@@||mgtv.com^
@@||mob.com^
@@||oppomobile.com^
@@||pstatp.com^
@@||qq.com^
@@||sina.com.cn^
@@||snssdk.com^
@@||sogou.com^
@@||sohu.com^
@@||taobao.com^
@@||tnc3-bjlgy.snssdk.com^
@@||unity3d.com^
@@||vivo.com.cn^
@@||xiaomi.com^
@@||youku.com^
```

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。