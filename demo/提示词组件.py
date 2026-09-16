from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
import sys
from model.my_model import MyModel
from prompt.builder_prompt_yaml import BuilderPromptYaml
from toolbox.ToolBox import MyTool

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

async def send_email_tool_agent(question: str):
    model = MyModel.get_model()
    tools = MyTool().get_tools()
    prompt = BuilderPromptYaml.get_prompt("send_email_agent.yaml")
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
    q = "请给在宜宾的2524279897@qq.com发送一封邮件,通知他今日天气和时间"

    async def test():
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
