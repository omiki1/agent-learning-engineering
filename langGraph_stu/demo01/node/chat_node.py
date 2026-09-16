from langchain.agents import create_agent

from langGraph_stu.demo01.state.state import State
from langGraph_stu.demo01.state.state import State
from model.my_model import MyModel
from langchain_core.messages import HumanMessage
def chat_node(state:State):
    model = MyModel.get_model()
    tools = []
    prompt = '''
        你是一个闲聊助手
    '''
    user_msg = state["messages"][-1]
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
    )
    rs = agent.invoke(
        {"messages": [HumanMessage(content=user_msg.content)]},
    )
    ai_msg = rs["messages"][-1]

    return {"messages": [ai_msg]}