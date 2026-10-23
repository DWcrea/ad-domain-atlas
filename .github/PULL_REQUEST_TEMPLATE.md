## 这个 PR 做了什么

<!-- 一句话说明。新增了哪些域名 / 修正了哪条判定 / 改了哪个工具 -->

## 变更类型

- [ ] 新增域名
- [ ] 修正用途或判定
- [ ] 新增厂商
- [ ] 工具或文档改进

## 依据

<!-- 抓包、SDK 文档、实测现象。判定有翻转的必须写清楚。 -->

## 自检

- [ ] `python tools/validate.py` 通过
- [ ] `python tools/build_docs.py` 已运行
- [ ] `python tools/export_rules.py` 已运行（新增可拦条目时）
- [ ] 新增条目都写了具体的 `purpose` 和 `impact`
- [ ] 拿不准的条目已标 `confidence: medium` 或 `low`，并在 `notes` 说明依据
- [ ] 没有手工修改 `docs/` 或 `lists/` 下的文件
