# Agent Debug 实验室

每个实验先写“期望轨迹”，再注入故障，最后只改一层。

## Lab 1：非法 JSON

让模型返回缺引号的 arguments。确认 Registry 产生 `invalid_arguments`，而不是工具函数收到脏数据。

## Lab 2：未知工具

返回 `weather_now`，Registry 只有 `weather`。检查是 Schema 暴露错误、模型选择错误还是版本不一致。

## Lab 3：路径逃逸

调用 `read_file("../README.md")`。应在路径解析后检查允许根目录，不能只拒绝字符串 `..`。

## Lab 4：重复循环

模型连续产生等价调用，参数 JSON 的键顺序不同。对 arguments 归一化后生成 fingerprint。

## Lab 5：超时与重复副作用

模拟发送邮件工具已成功但客户端超时。加入 idempotency key 和状态查询，证明盲目重试会重复发送。

## Lab 6：Context 膨胀

让工具每次返回 100 KB 文本。记录每步 Context 大小，再改为 Artifact id + 摘要 + 引用片段。

## Lab 7：Memory 污染

用户先说“我喜欢简洁”，后说“只在本次详细回答”。验证临时指令不会错误覆盖长期偏好。

## Lab 8：RAG 归因

构造正确文档未进入 top-k 和正确文档已进入但回答错误两例。前者改检索，后者改生成/证据使用。

## Lab 9：HITL 恢复

任务暂停后修改了订单金额。恢复前校验动作版本，旧审批不能批准新状态。

## Lab 10：Multi-Agent 错误传播

Researcher 给出错误来源，Developer 和 Reviewer 全部接受。加入来源独立验证，不只是增加 Reviewer Prompt。

## Lab 11：服务断开

SSE 客户端中断。分别实现“取消任务”和“转后台继续”策略，并说明业务选择。

## Lab 12：评测回归

Prompt 修改后总体成功率不变，但安全切片下降。报告必须按 category 分层，并设置安全硬门槛。

## Debug 报告模板

```text
症状：
期望轨迹：
实际轨迹：
首次偏离步骤：
故障层：model / schema / registry / tool / state / retrieval / stop / service
根因：
最小修复：
新增回归用例：
```

