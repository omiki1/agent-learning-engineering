from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
from dotenv import load_dotenv

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_PROJECT_ROOT, '.env'))

api_key = os.getenv("DASHSCOPE_API_KEY1")

client = MultiServerMCPClient(
    {
        "mytool":{
            "transport":'http',
            "url":'https://dashscope.aliyuncs.com/api/v1/mcps/WebFetch/mcp',
            "headers":{
                "Authorization": f"Bearer {api_key}"
            }
        }
    }
)
async def create_agent_search(q):
    model = MyModel.get_model()
    tools = await client.get_tools()
    print(tools)
    prompt = """
          一 角色:  你是一个聊天助手
       """
    # 4 创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        debug=True  # 可选参数，一般用于调试，生成环境必须设置未false
    )
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = await agent.ainvoke(human_msg)

    print(rs["messages"][-1].content)


if __name__ == "__main__":
    q = "请爬取这个网址：https://www.swpu.edu.cn/，提取通知公告，6月16日的数据"
    q1 = "请爬取西南石油大学官网，提取通知公告，6月16日的数据"
    # 异步调用
    asyncio.run(create_agent_search(q1))