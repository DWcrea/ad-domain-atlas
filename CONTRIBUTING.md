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
