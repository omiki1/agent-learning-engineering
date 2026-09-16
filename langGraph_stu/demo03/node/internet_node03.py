from langGraph_stu.demo03.state.email_state03 import EmailState
from pydantic import BaseModel,Field
from langchain.agents import create_agent
from model.my_model import MyModel
from langchain_core.messages import AIMessage
#响应参数
class InternetResponse(BaseModel):
    name:str = Field(...,description="姓名")
    subject: str = Field(..., description="邮件主题")
    content: str = Field(..., description="邮件内容")
"""
意图识别节点
"""
def internet_node(state:EmailState):

    model = MyModel.get_model()
    prompt ="""
         一 角色 你是一个意图识别助手
         二 任务 
                - 理解用户需求
                - 根据用户问题，提取姓名，邮件主题，邮件内容
        三 规则
                - 姓名，邮件主题，邮件内容不能为空
        四 输出
                 - 输出以下内容:{"name": "xx", "subject": "xx", "content": "xx"}
        五 示例
                 -用户输入：给张三发邮件，说今晚开会
                 -输出:{"name": "张三", "subject": "开会通知", "content": "今晚开会"}         
    """
    agent = create_agent(
        model =model,
        tools=[],
        system_prompt=prompt,
        response_format=InternetResponse
    )
    msg ={"messages":[{"role":"user","content":state["messages"][0].content}]}
    #获取结果
    rs = agent.invoke(msg)
    #把响应结果转换成字典
    json = rs["structured_response"].model_dump()
    #定义AI返回的内容
    ai_msg =f"\n意图节点识别成功:\n 姓名:{json["name"]}\n主题:{json["subject"]}\n邮件内容:{json["content"]}\n"

    #只返回当前节点修改的状态信息
    return {
        "messages":[AIMessage(content=ai_msg)],
        "name":json["name"],
        "subject": json["subject"],
        "content": json["content"],
        "result":"意图识别成功",
        "current_step":"internet_node"
    }

