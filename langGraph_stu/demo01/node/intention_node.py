from langchain_core.messages import HumanMessage,AIMessage

from langGraph_stu.demo01.state.state import State
from langGraph_stu.demo01.model_local import LocalModel
from langchain.agents import create_agent
from pydantic import BaseModel,Field

class EmailParams(BaseModel):
    name:str = Field(...,description="收件人姓名")
    subject:str = Field(...,description="邮件标题")
    content:str = Field(...,description="邮件内容")

def intention_node(state:State):
    model = LocalModel.get_model()
    tools = []
    prompt = """
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
        model=model,
        tools=tools,
        system_prompt=prompt,
        response_format=EmailParams,
    )
    rs = agent.invoke(
        {"messages": [
            HumanMessage(content=state["messages"][0].content),
        ]},
    )
    json = rs["structured_response"].model_dump()
    # 定义AI返回的内容
    ai_msg = f"\n意图节点识别成功:\n 姓名:{json["name"]}\n主题:{json["subject"]}\n邮件内容:{json["content"]}\n"

    return {
        "messages": [AIMessage(content=ai_msg)],
        "name": json["name"],
        "subject": json["subject"],
        "content": json["content"],
        "result": "意图识别成功"
    }