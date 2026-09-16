# 06｜RAG 与 Agentic RAG

## 1. 它是什么

普通 RAG：

```text
Query → Retrieve → Context → LLM → Answer
```

Agentic RAG：

```text
Query → Decide
 ├─ Rewrite?
 ├─ Vector/BM25/Hybrid?
 ├─ Rerank?
 ├─ Web Search?
 ├─ Retry?
 └─ Answer/Abstain?
```

## 2. 为什么出现

知识库问题常因 Query 表达、切块、索引、召回或证据冲突而失败。Agentic RAG 允许根据中间结果调整检索策略，但只在动态选择有实际收益时使用。

## 3. 不使用会怎样

固定 RAG 对简单知识库通常足够。复杂问题可能召回不足或无法处理多跳证据；但引入 Agent 会增加费用、延迟和循环风险。

## 4. 核心原理

### 4.1 Pipeline

```text
Ingest → Parse → Chunk → Metadata → Index
Query → Rewrite → Retrieve → Filter → Rerank → Pack Context
→ Generate with Citations → Verify
```

### 4.2 检索

- BM25：词法匹配，适合专有名词和精确术语。
- Vector Search：语义相似，适合改写表达。
- Hybrid：合并两者，需定义归一化和 fusion。
- Rerank：对候选精排，改善 top-k 顺序但增加成本。

### 4.3 失败分层

- Index Failure：文档没进入索引。
- Recall Failure：正确块未进 top-k。
- Ranking Failure：正确块排名太低。
- Context Failure：截断/拼接破坏证据。
- Generation Failure：证据存在但回答错。

### 4.4 Evidence Gate

回答前检查：是否有直接证据、来源是否独立、日期是否满足、引用是否真的支持结论。证据不足时应补检或明确 abstain，而不是用模型常识填空。

## 5. 最小代码实现

```python
def lexical_score(query, doc):
    q = set(tokenize(query))
    d = set(tokenize(doc.text))
    return len(q & d) / max(1, len(q))

ranked = sorted(docs, key=lambda d: lexical_score(query, d), reverse=True)
context = ranked[:3]
```

先用小语料验证评测链，再接 Embedding 和向量库。`projects/05_agentic_rag` 提供离线可运行版本。

## 6. 框架实现

向量库、LangChain Retriever 或托管 File Search 都可以替换检索层。框架不会替你决定正确的 chunk、metadata、过滤条件和评测集。Agentic 路由建议用显式 Graph 设置最大改写/检索次数。

## 7. 实际场景

内部政策问答适合 Hybrid + metadata filter；跨文档调研需要多跳检索和证据合并；实时信息应补 Web 搜索并保留发布日期。

## 8. 常见错误

只评最终答案、不评 Recall；chunk 太大/太小；没有文档版本；引用 URL 存在但不支持句子；对所有问题都循环改写；把用户上传文本中的恶意指令当系统指令。

## 9. Debug 方法

保存 query、rewrite、filter、候选 id/score、rerank、最终上下文和逐句引用。先检查 Recall@k，再检查生成；不要直接调 Prompt 掩盖检索失败。

## 10. 思考题

1. Query Rewrite 会不会改变用户原意？如何检测？
2. Top-k 增大为何可能让答案更差？
3. Web 与内部知识冲突时谁优先？

## 11. 实战任务与验收

构建 50–100 个文档块、30 个问题的评测集，对比 lexical、vector、hybrid、rerank 和 agentic retry。验收：报告 Recall@k、答案正确率、引用正确率、平均检索次数、Token、延迟和 abstain 质量。

