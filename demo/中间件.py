from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.agents.middleware import ModelCallLimitMiddleware,HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import  Command

def create_email_agent(question:str):
    model = MyModel.get_model()
    tools = [send_email_tool,]
    prompt = '''
    一 角色: 你是一个邮件发送助手
    二 任务：
         - 理解用户需求，从用户消息中提取收件人邮箱（形如 xxx@qq.com 的部分）
         - 如果用户没说明主题和内容，根据邮件用途合理推断（例如"上课通知"）
         - 必须调用 send_email_tool 工具发送邮件，禁止反问用户补充信息
    三 规则：
         - send_email_tool 参数：to=收件人邮箱, subject=主题, context=内容
         - 三个参数都必须提供完整值
    '''
    try:
        hum_middleware = HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email_tool":{
                    "allowed_decisions":["approve","reject","edit"],
                    "description":'邮件发送需要人工审核，请确认邮件内容是否正确',

                },
            },
            description_prefix = '【人工审核】'
        )
    except Exception as e:
        print(e)
        print("限制模型访问次数失败")
    memory = InMemorySaver()
    # 4 创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        debug=True,  # 可选参数，一般用于调试，生成环境必须设置未false
        checkpointer=memory,  # 记录Agent运行状体
        middleware=[hum_middleware]
    )
    human_msg = {"messages":[HumanMessage(content=question)]}
    config = {"configurable": {"thread_id": "1"}}
    rs = agent.invoke(human_msg,config)
    print(rs)
    d = rs.get("__interrupt__")
    if not d:
        # 模型没有调用 send_email_tool，不会触发人工审核
        print("模型未触发人工审核，回复：", rs["messages"][-1].content)
        return
    if d:
        print("请选择操作：")
        print("   1. approve - 批准发送")
        print("   2. edit - 编辑内容后发送")
        print("   3. reject - 拒绝发送")
        choice = input("请输入你的选择：")
        if choice == "1":
            print("批准发送邮件")
            data = agent.invoke(Command(
                resume={
                    "decisions": [
                        {"type": "approve"}
                    ]
                }
            ), config)
            print(data["messages"][-1].content)
        elif choice == "2":
            print("请输入编辑内容")
            to = input("请输入收件人邮箱：")
            subject = input("请输入标题")
            content = input("请输入内容")
            # 构建一个修改后的工具参数对象
            p = {
                "to": to,
                "subject": subject,
                "content": content
            }
            # 发送邮件
            data = agent.invoke(Command(
                resume={
                    "decisions": [
                        {"type": "edit", "edited_action": {
                            "name": "send_email_tool",
                            "args": p
                        }}
                    ]
                }
            ), config)
            print(data["messages"][-1].content)
        else:
            print("拒绝发送邮件")
            reason = input("请输入拒绝理由")
            data = agent.invoke(Command(
                resume={
                    "decisions": [
                        {"type": "reject", "message": reason}
                    ]
                }
            ), config)
            print(data)
            print(data["messages"][-1].content)

    else:
        print("模型不支持")
if __name__ =="__main__":
        q="邮件是2524279897@qq.com 发送一封邮件"
        create_email_agent(q)
