# Finacial Analyst

本项目稍作调整，将 MCP 工具直接注入到 `code_writer_agent` 和 `code_execution_agent`。

当前效果是能生成 stock_analysis.py 文件，但是看样子没有执行代码绘图。

## 快速开始

### 1. 部署 MCP 服务工具
```bash
uv run src/server.py
```

### 2. 运行 CrewAI Agent
```bash
uv run src/main.py
```

## 温馨提示
- crewai 包的 Agent 指定用 `unsafe`（非容器模式）执行代码时，依然会检查 docker 是否存在。本项目使用 src/hack.py 绕过这个问题。
- 源码参考 https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek
