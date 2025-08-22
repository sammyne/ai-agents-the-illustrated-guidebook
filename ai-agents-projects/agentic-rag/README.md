# Agentic RAG

## 快速开始
### 启动服务端
> 需填充 .env 文件的 `OPENAI_API_KEY`、`OPENAI_API_BASE_URL` 和 `OPENAI_MODEL`。

> 模型用 DeepSeek 比 Qwen 更好。Qwen 没能正确分析工具返回的结果

```bash
uv run src/server.py
```

### 使用客户端发送查询请求
```bash
uv run src/client.py --query "What's Qwen3"
```

## 参考文献
- https://www.dailydoseofds.com/p/deploy-a-qwen-3-agentic-rag/
- 源码 https://github.com/patchy631/ai-engineering-hub/tree/main/deploy-agentic-rag