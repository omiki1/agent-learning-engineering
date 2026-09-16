from tool.send_email_tool import send_email_tool
from model.my_model import MyModel
from langchain.agents import create_agent

def create_agent_demo(question:str):
    model = MyModel.get_model()
    # 创建工具
    tools = [send_email_tool,]
    # 创建提示词
    prompt = '''
        你是一个邮件发送助手
    '''
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        debug=True
    )
    human_msg = {
        "messages": [{'role':'user','content':question}],
    }
    rs = agent.invoke(human_msg)

    print(rs)
if __name__ == '__main__':
    create_agent_demo('帮我发送邮件到3435113586@qq.com,通知他快去上课')

