# Project 05｜Agentic RAG

离线小型 RAG：按字符/术语检索课程文档，Evidence Gate 不通过时扩展 Query，再检索一次。重点不是检索质量，而是分离 `rewrite → retrieve → gate → answer/abstain`。

```powershell
python projects/05_agentic_rag/main.py "Agent 和 Workflow 有什么区别"
```

扩展：替换为 BM25、Embedding、Hybrid 和 Rerank；建立至少 30 个问题，先测 Recall@k 再测答案。

