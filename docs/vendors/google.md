# Google（谷歌）

广告、分析、崩溃上报三条产品线共用同一套基础设施，域名高度交叉。只拦一个入口通常无效，广告请求会走备用域。


- 官网：https://www.google.com
- 隐私政策：https://policies.google.com/privacy
- 登记域名：14 条

## `2mdn.net`

- **产品 / SDK**：DoubleClick Studio 素材 CDN
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：素材CDN

**用途**

存放 DoubleClick 广告素材（图片、视频、富媒体创意），由广告投放域引用。

**拦截后果**

广告素材加载失败，广告位显示空白或占位图。

**规则**

```text
||2mdn.net^
```

## `adservice.google.com`

- **产品 / SDK**：AdMob / AdX 移动端广告请求
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：仅该子域（含其下级）
- **置信度**：已确认
- **标签**：AdMob、移动广告

**用途**

移动 App 内广告 SDK 的请求入口，常见路径 /adsid/integrator.js 与 /pagead/。与 googlesyndication.com 互为补充，只拦一个会漏。

**拦截后果**

App 内 Google 广告请求失败，广告位空白。

**规则**

```text
||adservice.google.com^
```

## `app-measurement.com`

- **产品 / SDK**：Firebase Analytics（GA4 for Firebase）
- **分类**：统计分析（`analytics`）
- **判定**：可拦，有代价（`block-cost`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：App统计、Firebase

**用途**

移动 App 的 Firebase 埋点上报端点，负责事件、用户属性、受众同步。

**拦截后果**

App 内埋点全丢。少数 App 依赖远端配置返回值，极端情况下首次启动会卡在初始化。

**规则**

```text
||app-measurement.com^
```

## `crashlytics.com`

- **产品 / SDK**：Firebase Crashlytics
- **分类**：崩溃监控（`crash`）
- **判定**：可拦，有代价（`block-cost`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：崩溃上报

**用途**

崩溃与 ANR 上报，附带设备型号、系统版本、堆栈与最近操作路径。

**拦截后果**

开发者收不到崩溃数据；终端用户无感知。

**规则**

```text
||crashlytics.com^
```

## `doubleclick.net`

- **产品 / SDK**：Google Ad Manager / DoubleClick（DFP）
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：展示广告、RTB、海外

**用途**

Google 展示广告的核心投放域。ad.doubleclick.net 承载广告素材与点击跳转，stats.g.doubleclick.net 负责曝光与点击计数，securepubads.g.doubleclick.net 提供网页广告位接口。

**拦截后果**

网页与 App 内的 Google 系广告位变为空白，广告链接点不开，属预期行为。

**规则**

```text
||doubleclick.net^
```

## `firebaseinstallations.googleapis.com`

- **产品 / SDK**：Firebase Installations
- **分类**：行为追踪（`tracking`）
- **判定**：可拦，有代价（`block-cost`）· 粒度：仅该子域（含其下级）
- **置信度**：较可信
- **标签**：设备标识、Firebase

**用途**

生成并维护 Firebase Installation ID（FID），Analytics、Remote Config、Cloud Messaging 都依赖它做实例标识。

**拦截后果**

依赖 FID 的推送 token 注册可能失败，导致收不到推送；纯统计类 App 只是丢数据。

**规则**

```text
||firebaseinstallations.googleapis.com^
```

## `google-analytics.com`

- **产品 / SDK**：Google Analytics（UA / GA4）
- **分类**：统计分析（`analytics`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：网站统计

**用途**

GA 的数据采集端点，analytics.js、gtag/js 与 /g/collect 上报都指向这里。

**拦截后果**

站点统计数据缺失，对访客无感知。

**规则**

```text
||google-analytics.com^
```

## `google.com`

- **产品 / SDK**：Google 主域
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：基础设施、高危误杀

**用途**

搜索、账号、登录、验证码、地图等核心服务的宿主域。

**拦截后果**

无法登录 Google 账号、无法通过 reCAPTCHA 验证，大量第三方 App 的 Google 登录一并失效。

**规则**

```text
@@||google.com^
```

## `googleadservices.com`

- **产品 / SDK**：Google Ads 点击与转化跟踪
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：点击跟踪、转化

**用途**

广告点击后的跳转与转化归因（pagead/aclk、pagead/conversion）。用户点广告时先到这里记账，再跳到落地页。

**拦截后果**

广告点击无法记账与跳转；正常站内跳转不受影响。

**规则**

```text
||googleadservices.com^
```

## `googleapis.com`

- **产品 / SDK**：Google APIs 公共入口
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：基础设施、高危误杀

**用途**

承载 Firebase、地图、登录、云服务的统一 API 网关，大量 App 的基础能力都在这个域下。

**拦截后果**

整域封禁会导致 Google 登录、地图、Firebase 推送、Play 服务集体失效，App 可能直接白屏或闪退。

**规则**

```text
@@||googleapis.com^
```

## `googlesyndication.com`

- **产品 / SDK**：AdSense / AdMob
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：展示广告、AdMob、AdSense

**用途**

pagead2.googlesyndication.com 下发广告脚本，tpc.googlesyndication.com 存放广告素材，googleads.g.doubleclick.net 与它同源。移动端 AdMob 与网页 AdSense 都走这里。

**拦截后果**

广告位空白；不影响 Google 账号、搜索、地图等业务。

**规则**

```text
||googlesyndication.com^
```

## `googletagmanager.com`

- **产品 / SDK**：Google Tag Manager（GTM）
- **分类**：行为追踪（`tracking`）
- **判定**：可拦，有代价（`block-cost`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：标签管理、高风险误杀

**用途**

标签管理器容器。除了 GA4 与广告像素，很多网站把业务脚本、客服组件、A/B 测试也塞在同一个容器里。

**拦截后果**

会同时屏蔽该容器内的所有第三方脚本。若站点把业务逻辑放进 GTM，可能出现按钮失效、表单不提交。

**规则**

```text
||googletagmanager.com^
```

> 拦之前先确认目标站点有没有把非广告脚本放进 GTM。移动 App 一般不用 GTM，影响面小。

## `googletagservices.com`

- **产品 / SDK**：Google Publisher Tag（GPT）
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：网页广告

**用途**

网页广告位的调度脚本（gpt.js），负责向 Ad Manager 请求广告并渲染到页面。

**拦截后果**

使用 GPT 的网站广告位不渲染；若站点把业务脚本挂在该域会异常（少见）。

**规则**

```text
||googletagservices.com^
```

## `gstatic.com`

- **产品 / SDK**：Google 静态资源 CDN
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：根域及其所有子域（整域通配）
- **置信度**：已确认
- **标签**：CDN、高危误杀

**用途**

提供字体、JS 库、公共静态资源。许多网站与 App 从 gstatic.com 加载非广告资源。

**拦截后果**

页面字体回退、部分站点 JS 加载失败、布局错乱。

**规则**

```text
@@||gstatic.com^
```

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。