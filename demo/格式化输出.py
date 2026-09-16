from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from pydantic import BaseModel,Field

class CodeFormat(BaseModel):
    data:str =Field(...,description="验证码")
    code: str = Field(..., description="状态码,200表示成功,500表示失败")
    msg:str = Field(...,description="提示信息")

def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool,add_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
       二 任务：
             -理解用户需求
             -生成一个不规则的4位数的数字作为验证码
             - 根据用户需求发送邮件
       三 规则：
            -验证码必须是4位
            -如果邮件发送成功，状态码是200，提示信息是 "邮件发送成功"
            -如果邮件发送失败，状态码是500，提示信息是 "邮件发送失败"
       四 输出
            -输出内容是: 验证码，状态码，提示信息
       五 示例
           - 输入: 邮箱是444444@qqq.com,发送邮件
           - 输出：验证码，状态码，提示信息 
    """
    #4 创建智能体
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        response_format=CodeFormat,
        debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print(rs)
    json = rs["structured_response"].model_dump()
    print(json)
    print(type(json))

if __name__ =="__main__":
        q="邮件是2524279897@qq.com 发送一封邮件"
        create_email_agent(q)

