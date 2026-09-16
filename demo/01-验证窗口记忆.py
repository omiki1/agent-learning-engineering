from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from memory.manager.session_manager import SessionManager


def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    # 2 创建一个工具
    tools = []
    # 3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个聊天助手
       二 任务:
              - 理解用户问题，回答用户问题
       三 规则：
             -你需要回答用户问题，携带记忆内容

    """
    # 4 创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        # debug=True  # 可选参数，一般用于调试，生成环境必须设置未false
    )
    session_manager = SessionManager('002')
    # 先基于历史构建记忆提示词（不含当前问题），再保存当前问题，避免重复
    memory_prompt = session_manager.build_prompt()
    session_manager.save("user", q)
    human_msg = {"messages": [HumanMessage(content=q), memory_prompt]}
    rs = agent.invoke(human_msg)
    session_manager.save("ai", rs["messages"][-1].content)
    print(rs["messages"][-1].content)
if __name__ == "__main__":
    q1 = "我叫张三，今年23岁"
    q5="我是谁，今年多大了"
    for q in [q1, q5]:
        print("---------------------")
        create_email_agent(q)