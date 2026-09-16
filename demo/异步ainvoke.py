import time
from langgraph.checkpoint.memory import InMemorySaver
from model.my_model import MyModel
from tool.web_searcher_tool import search_tool
from tool.send_email_tool import send_email_tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
async def send_email_agent(question:str):
    memory = InMemorySaver()
    model =     MyModel.get_model()
    tools = [search_tool,send_email_tool]
    propmt = '''
你是一个掌握联网搜索和发送邮件能力的智能助手。

**任务流程（必须严格遵守）**：
1. 调用 `baidu_search` 获取近期热点新闻
2. **关键**：从 `baidu_search` 的返回结果中提取实际新闻内容
3. 将提取到的新闻内容作为邮件的 `context`
4. 调用 `send_email_tool` 发送邮件

**禁止事项**：
- ❌ 禁止在邮件内容中使用"近期热点新闻汇总"这种占位文字
- ❌ 禁止自己编造新闻内容
- ✅ 必须使用 `baidu_search` 返回的实际信息

**邮件内容示例**（正确）：
"您好！以下是近期热点新闻：
1. 标题：XX地区发生地震...
   摘要：...
2. 标题：XX公司被罚款...
   摘要：..."

**注意**：邮件内容必须是从搜索工具获取的真实信息！
    '''

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=propmt,
        checkpointer=memory,
        debug=True,
    )
    human_msg = {'messages':[HumanMessage(content=question)]}
    rs = await agent.ainvoke(human_msg)
    await asyncio.sleep(1)
    print(rs)
if __name__ == '__main__':
    q1 = '请给2524279897@qq.com发送一封邮件,告诉他近期热点新闻'
    async def run_current_test():
        start = time.time()
        results = await asyncio.gather(
            send_email_agent(q1),
        )
        for r in results:
            print(r)
        print(f"并发执行完成，总耗时: {time.time() - start:.2f}秒")
    asyncio.run(run_current_test())

