# 项目参考实现

建议顺序：先只读每个项目 README 的需求，自己画架构并写伪代码，再打开实现。所有项目默认提供离线路径；外部 SDK 是可选扩展。

| 项目 | 默认运行 |
| --- | --- |
| 01 Tool Agent | `python projects/01_tool_agent/main.py` |
| 02 ReAct Agent | `python projects/02_react_agent/main.py` |
| 03 Memory Agent | `python projects/03_memory_agent/main.py --demo` |
| 04 Research Workflow | `python projects/04_research_workflow/main.py` |
| 05 Agentic RAG | `python projects/05_agentic_rag/main.py` |
| 06 MCP Agent | 安装 MCP SDK 后见项目 README |
| 07 Multi-Agent | `python projects/07_multi_agent/main.py` |
| 08 Agent Service | `python projects/08_agent_service/core.py`；Web 层可选 |
| 09 Agent Eval | `python projects/09_agent_eval/evaluate.py` |
| 10 Research Agent | `python projects/10_ai_research_agent/app.py` |

参考实现刻意保持小型，目的是暴露架构边界。它们不是生产部署模板。

