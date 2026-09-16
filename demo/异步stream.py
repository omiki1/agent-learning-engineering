from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
import sys
from model.my_model import MyModel
from toolbox.ToolBox import MyTool

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

async def send_email_tool_agent(question: str):
    model = MyModel.get_model()
    tools = MyTool().get_tools()
    prompt = '''
你是一个智能邮箱助手，负责根据天气情况发送通知邮件。

**核心任务**：
1. 当用户要求发送邮件时，立即调用 send_email_tool 工具
2. 在发送前，先调用 get_weather 工具查询指定城市的天气
3. 根据天气情况，生成个性化的邮件内容，提醒收件人注意事项

**工作流程**：
1. 从用户请求中提取：收件人邮箱、城市名称
2. 调用 get_weather(city) 获取天气信息
3. 根据天气生成邮件内容（包括天气状况、温度、温馨提示）
4. 调用 send_email_tool 发送邮件

**邮件内容生成规则**：
- 晴天：提醒注意防晒、补充水分
- 雨天：提醒带伞、注意出行安全
- 高温：提醒防暑降温
- 低温：提醒注意保暖
- 大风：提醒注意安全

**示例**：
用户："请给user@example.com发送一封邮件，告诉他成都的天气情况"
你应该：
  1. 调用 get_weather(city="成都") 
  2. 根据返回的天气生成邮件
  3. 调用 send_email_tool 发送邮件

**注意**：
- 不要询问用户邮件内容，根据天气自动生成
- 如果用户没提供城市，询问或使用默认城市
- 邮件要友好、专业
- 重要：当用户说"在XX的user@example.com"这类表达时，XX 就是要查询天气的城市，
  必须直接调用 get_weather(city=XX)，不要反问用户是否需要天气信息
'''
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt
    )
    human_msg = {'messages': HumanMessage(content=question)}
    async for r in agent.astream(human_msg, stream_mode="messages"):
        if r:
            yield r

if __name__ == "__main__":
    q = "请给在宜宾的2524279897@qq.com发送一封邮件,通知他今日天气"

    async def test():
        # 流式输出:把 token 块拼接成完整文本,而不是打印元组
        collected = []
        async for r in send_email_tool_agent(q):
            if r:
                # r 是 (chunk, metadata) 元组,chunk 是 AIMessageChunk
                chunk = r[0] if isinstance(r, tuple) else r
                text = getattr(chunk, "content", "")
                if text:
                    print(text, end="", flush=True)
                    collected.append(text)
        print()
        print("-" * 60)
        print("完整回复:", "".join(collected))

    asyncio.run(test())
