from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
model = MyModel.get_model()
tools = [add_tool,]
prompt="""请用中文总结以下对话。**重要：必须逐条列出用户提出的每一个具体问题**，包括计算题（如"1+1等于多少"、"10+20等于多少"），以及用户提供的所有个人信息（姓名、年龄、职业、学习内容）。

对话内容：
{conversation}

总结格式：
- 用户问题列表：
  1. [第一个问题原文]
  2. [第二个问题原文]
  ...
- 用户信息：
  - 姓名：...
  - 年龄：...
  - 职业：...
  - 学习内容：...
"""
summary = SummarizationMiddleware(
    model=model,
    trigger=("tokens",210),
    keep=("messages",3),
)
def print_memory(agent, thread_id=1):
    config = {"configurable": {"thread_id": thread_id}}
    state = agent.get_state(config)
    messages = state.values.get("messages", [])
    print("\n================ 当前记忆状态（已持久化到数据库） ================")
    print("消息数量：", len(messages))
    for i, message in enumerate(messages):
        print(f"\n--- Message {i + 1} ---")
        print("类型：", type(message).__name__)
        # 只打印前500个字符，避免输出太长
        content = str(message.content)
        print("内容：")
        print(content[:500])
    print("==============================================\n")
def create_email_agent(agent,q,user_id):
    human_msg ={'messages': [HumanMessage(content=q)]}
    config = {"configurable": {"thread_id": user_id}}
    rd = agent.invoke(human_msg, config)
    return rd
if __name__ == "__main__":
    url = os.getenv('POSTGRESQL_URL')
    with PostgresSaver.from_conn_string(url) as pg:
        pg.setup()

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            checkpointer=pg,
            middleware=[summary,],
        )
        config_clean = {"configurable": {"thread_id": 1}}
        q_list = [
            "1+1等于多少？",
            "我的名字叫张三，我是一名Java程序员。",
            "我今年23岁，目前正在学习LangChain和LangGraph。",
            "10+20等于多少？",
            "我之前问的第一个问题是什么？",  # 测试记忆保留
            "我是谁？多少岁了，目前在学习什么"
        ]
        for i in range(len(q_list)):
            print(f"第{i + 1}个问题:{q_list[i]}")
            rs = create_email_agent(agent, q_list[i], 1)
            print(f"第{i + 1}个的答案:{rs}")
        print("=============打印当前记忆信息（存在数据库里）=============")
        print_memory(agent, 1)