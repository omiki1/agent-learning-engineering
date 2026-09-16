from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from middleware.word_filter_middleware import word_filter_middleware,word_ping_middleware

#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个聊天助手
    """
    try:
        # 4 创建智能体
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            debug=True,  # 可选参数，一般用于调试，生成环境必须设置未false
            middleware=[word_filter_middleware]
            #middleware=[word_ping_middleware]
        )
        human_msg = {"messages": [HumanMessage(content=q)]}


        rs = agent.invoke(human_msg)
        print(rs["messages"][-1].content)
    except Exception as e:
        print(e)

if __name__ =="__main__":
        q="赌博是什么"
        create_email_agent(q)

