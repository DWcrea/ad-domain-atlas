PY ?= python

.PHONY: all validate docs rules coverage check clean

all: validate docs rules

## 校验数据
validate:
	$(PY) tools/validate.py

## 生成文档
docs:
	$(PY) tools/build_docs.py

## 导出规则
rules:
	$(PY) tools/export_rules.py

## 与主流规则库比对覆盖率（需要网络）
coverage:
	$(PY) tools/check_lists.py --list https://big.oisd.nl/ --name "OISD big"
	$(PY) tools/build_docs.py

## 检查生成物是否最新（CI 用）
check:
	$(PY) tools/validate.py
	$(PY) tools/build_docs.py --check

## 清理缓存
clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
