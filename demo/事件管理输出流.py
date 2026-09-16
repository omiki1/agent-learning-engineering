from tool.send_email_tool import send_email_tool
from tool.web_searcher_tool import search_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio


async def create_agent_email(q):
    model = MyModel.get_model()
    tools = [send_email_tool, add_tool, search_tool]
    prompt = '''
你是一个掌握联网搜索和发送邮件能力的智能助手。

**任务流程（必须严格遵守）**：
1. 调用 `search_tool` 获取与用户问题相关的实时信息（天气、热点新闻等）
2. **关键**：从 `search_tool` 的返回结果中提取实际信息内容
3. 将提取到的信息作为邮件的 `context`
4. 调用 `send_email_tool` 发送邮件

**禁止事项**：
- ❌ 禁止在邮件内容中使用"近期热点新闻汇总"这种占位文字
- ❌ 禁止自己编造内容
- ✅ 必须使用 `search_tool` 返回的实际信息

**邮件内容示例**（正确）：
"您好！以下是相关信息：
1. 标题：宜宾今日天气...
   摘要：...
2. 标题：XX公司被罚款...
   摘要：..."

**注意**：邮件内容必须是从搜索工具获取的真实信息！
    '''
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
    )
    human_msg = {"messages": [HumanMessage(content=q)]}
    async for event in agent.astream_events(human_msg, version="v2"):
        event_name = event["event"]

        yield "\n"
        yield event

        if event_name == 'on_chain_start' and event.get("name") == "LangGraph":
            yield f"\n邮件智能体开始运行\n"

        elif event_name == 'on_chat_model_start':
            yield f"\n大模型开始思考\n"

        elif event_name == 'on_chat_model_stream':
            chunk = event["data"]["chunk"]
            data = chunk.content if hasattr(chunk, "content") else str(chunk)
            if isinstance(data, str) and data:
                yield data

        elif event_name == 'on_tool_start':
            tool_name = event["name"]
            if tool_name == "send_email_tool":
                yield f"\n开始发送邮件\n"
            elif tool_name == "search_tool":
                yield f"\n正在联网搜索信息\n"

        elif event_name == "on_tool_end":
            output = event["data"]["output"]
            tool_output = output.content if hasattr(output, "content") else output
            yield f"\n工具执行完毕，返回值为：{tool_output}\n"


async def test(q):
    async for rs in create_agent_email(q):
        print(rs, end="")


if __name__ == "__main__":
    q = "宜宾热点时事，请给2524279897@qq.com 发送一封邮件，告诉他热点新闻"
    asyncio.run(test(q))