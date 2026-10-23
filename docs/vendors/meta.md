# Meta（前 Facebook）

同一批域名同时承担登录、分享与广告归因，是典型的「拦了会坏功能」区域，必须按主机名区分。


- 官网：https://www.meta.com
- 隐私政策：https://www.facebook.com/privacy/policy
- 登记域名：6 条

## `an.facebook.com`

- **产品 / SDK**：Meta Audience Network
- **分类**：广告投放（`ad-serving`）
- **判定**：直接拦截（`block`）· 粒度：仅该主机名
- **置信度**：已确认
- **标签**：移动广告

**用途**

面向第三方 App 的横幅、插屏、激励视频广告请求与素材下发。

**拦截后果**

App 内 Audience Network 广告位空白，不影响 Facebook 登录。

**规则**

```text
||an.facebook.com^
```

## `connect.facebook.net`

- **产品 / SDK**：Facebook JS SDK / Pixel
- **分类**：行为追踪（`tracking`）
- **判定**：可拦，有代价（`block-cost`）· 粒度：仅该主机名
- **置信度**：已确认
- **标签**：Pixel、网页SDK、混用

**用途**

网页端 SDK 宿主。sdk.js 负责登录与分享，fbevents.js 负责 Meta Pixel 转化追踪，两者同域。

**拦截后果**

Pixel 被彻底阻断，但依赖 FB 登录的站点登录按钮也会一起失效。

**规则**

```text
||connect.facebook.net^
```

> 只做广告拦截、不介意坏登录的场景可整域拦；否则建议只拦 `/signals/` 路径。

## `facebook.com`

- **产品 / SDK**：Facebook 主域
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：基础设施、高危误杀

**用途**

账号登录、OAuth 授权、分享、Messenger 跳转的宿主域。

**拦截后果**

所有「用 Facebook 登录」的 App 与网站失效，分享按钮报错，OAuth 回调失败。

**规则**

```text
@@||facebook.com^
```

## `facebook.net`

- **产品 / SDK**：Facebook 静态资源域
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：基础设施

**用途**

承载 connect.facebook.net 等前端 SDK 资源。

**拦截后果**

网页内嵌的 Facebook 组件（登录、评论、分享）全部失效。

**规则**

```text
@@||facebook.net^
```

## `fbcdn.net`

- **产品 / SDK**：Facebook 内容 CDN
- **分类**：基础服务（`infra`）
- **判定**：不建议拦截（`keep`）· 粒度：整域通配（含所有子域）
- **置信度**：已确认
- **标签**：CDN、高危误杀

**用途**

头像、图片、视频、静态资源分发。

**拦截后果**

图片与视频大面积加载失败，社交类 App 界面破版。

**规则**

```text
@@||fbcdn.net^
```

## `graph.facebook.com`

- **产品 / SDK**：Facebook Graph API
- **分类**：行为追踪（`tracking`）
- **判定**：部分拦截（`partial`）· 粒度：仅该主机名
- **置信度**：已确认
- **标签**：登录、广告归因、混用

**用途**

Graph API 统一入口。既服务登录与好友关系（/me、/oauth），也承担广告归因与事件回传（/tr、/activities）。

**拦截后果**

整域拦截会同时废掉 Facebook 登录与分享；只能按路径拦 /tr 一类广告端点。

**规则**

```text
||graph.facebook.com^
```

> AdGuard 可用路径规则，例如 `||graph.facebook.com/tr^`。但 App 内 SDK 常把参数拼进同一路径，按路径拦的稳定性不如按主机名。

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。