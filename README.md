# Code Sentinel

A project to... (add project description here)



## 环境搭建 & 工程规范
### 1. 初始化 Poerty
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
在工程目录下执行
```shell
poetry init
```
安装依赖, 可根据需要添加
```shell
# 生产依赖 (运行时需要)
poetry add fastapi uvicorn python-dotenv langchain langchain-openai langgraph pydantic httpx

# 开发依赖 (仅开发/测试需要)
poetry add --group dev ruff pre-commit pytest
```

### 2. 配置代码格式化工具 Ruff
在上一步生成的 pyproject.toml 文件下加入以下内容:
```toml
# pyproject.toml

[tool.ruff]
# 设置行宽 (Python 建议 88 或 120)
line-length = 88
# 目标 Python 版本
target-version = "py313"

[tool.ruff.lint]
# 启用常见规则:
# E: pycodestyle errors
# W: pycodestyle warnings
# F: Pyflakes
# I: isort (自动导入排序)
# B: flake8-bugbear (发现潜在 bug)
select = ["E", "W", "F", "I", "B"]

# 忽略某些规则 (如果需要)
ignore = []

[tool.ruff.format]
quote-style = "double"
```

```shell
检查代码:
poetry run ruff check .
自动格式化代码:
poetry run ruff format .
```

### 3.配置 Pre-commit Hooks
防止坏代码提交到 git
1. 在根目录创建 .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format
```
2. 安装 pre-commit hooks
```shell
poetry run pre-commit install
```