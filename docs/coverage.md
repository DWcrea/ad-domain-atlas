# 与主流规则库的覆盖对比

回答一个问题：这些域名，现成的规则库到底拦了多少？没被拦的部分，才是需要自己补规则的地方。


> 生成于 2026-10-23

## 参与比对的规则库

| 规则库 | 条目数 | 来源 |
| --- | --- | --- |
| anti-AD | 103,776 | `anti-ad-adguard.txt` |
| OISD big | 234,497 | `oisd_big.txt` |

## 总体覆盖

- 收录域名：**187** 条
- 被规则库直接命中：**135** 条
- 仅被上级域规则覆盖：**0** 条
- 完全未覆盖：**52** 条
- 覆盖率：**72.2%**

「仅被上级域覆盖」指规则库只封了某个子域（例如 `||ad.doubleclick.net^`），而没有封主机根域。这类条目在 DNS 层仍可能漏掉其他子域。

## 规则库漏掉的可拦域名（18 条）

这些条目判定为可拦，但上面参与比对的规则库里没有对应规则。把它们补进自己的规则集，效果会立竿见影。

| 域名 | 厂商 | 判定 | 用途 |
| --- | --- | --- | --- |
| `adash.ut.taobao.com` | Alibaba | 拦截·代价 | 阿里系 UT 埋点的实际上报端点。 |
| `alimama.com` | Alibaba | 拦截 | 淘宝联盟与直通车的投放管理、素材与点击跳转接口。 |
| `tanx.com` | Alibaba | 拦截 | 阿里的 RTB 广告交易市场，向媒体方提供广告位竞价与素材。 |
| `pangle.io` | ByteDance | 拦截 | 面向海外开发者的广告变现平台，提供广告请求、报表与素材接口。 |
| `adservice.google.com` | Google | 拦截 | 移动 App 内广告 SDK 的请求入口，常见路径 /adsid/integrator.js 与 /pagead/。 |
| `firebaseinstallations.googleapis.com` | Google | 拦截·代价 | 生成并维护 Firebase Installation ID（FID），Analytics、Remote Config、Cloud Messaging 都依赖它做实例标识。 |
| `connect.facebook.net` | Meta | 拦截·代价 | 网页端 SDK 宿主。 |
| `pgdt.gtimg.com` | Tencent | 拦截 | 存放广点通广告的图片与视频素材，由投放域引用。 |
| `heap.io` | 产品分析 | 拦截 | 全量自动采集（capture everything），不需要预先埋点。 |
| `metrics.data.hicloud.com` | 国产终端厂商 | 拦截·代价 | 华为分析服务（Analytics Kit）与系统遥测的数据上报端点。 |
| `mistat.xiaomi.com` | 国产终端厂商 | 拦截·代价 | MIUI/HyperOS 与小米系 App 的使用统计、广告归因、设备画像上报。 |
| `atm.youku.com` | 国内视频与音乐平台 | 拦截 | 优酷的广告投放与计数中枢。 |
| `ut.youku.com` | 国内视频与音乐平台 | 拦截·代价 | 阿里系统一的 UT 埋点上报域，adashx.ut 与 h-adashx.ut 记录播放、点击、停留时长。 |
| `ad.360.cn` | 国内门户与搜索引擎 | 拦截 | 360 广告平台的服务端，同族还有 ad.jia / ad.life / ad.iot 等按行业拆分的子域。 |
| `magnite.com` | 国际程序化广告与监测 | 拦截 | Magnite 现行主域，承担 SSP 竞价与素材分发。 |
| `tenjin.com` | 归因与深度链接 | 拦截 | 面向独立游戏开发者的轻量归因与收入分析。 |
| `airship.com` | 营销自动化与推送 | 拦截·代价 | 推送基础设施与消息编排，服务大量欧美媒体与零售 App。 |
| `clevertap.com` | 营销自动化与推送 | 拦截·代价 | 用户分群与营销自动化，主打推送与应用内消息。 |

另有 34 条「不建议拦截」的域名本来就不该出现在规则库里，未计入上表。它们见 [误杀黑名单](keep.md)。

---

> 本页由 `tools/build_docs.py` 从 `data/` 自动生成，请勿手工编辑。
> 修正内容请改 YAML 后重新构建，或直接提交 Pull Request。