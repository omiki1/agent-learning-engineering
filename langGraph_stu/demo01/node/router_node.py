from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langGraph_stu.demo01.state.state import State
from model.my_model import MyModel
from pydantic import BaseModel,Field
from typing import Literal

Intent = Literal["email", "database", "chat"]
class RouterNode(BaseModel):
    intent:Intent = Field(...,description='用户意图识别')


def router_node(state: State):
    model = MyModel.get_model()
    structured_model = model.with_structured_output(RouterNode,method="json_mode")
    prompt = [
        SystemMessage(content="""
                你是一个意图分类助手。根据用户的消息，判断他属于哪一类业务：
                - email: 涉及发送邮件、写邮件
                - database: 涉及查询数据、数据库操作
                - chat: 普通聊天、问答
                只输出分类结果，不要做其他事。
                请以 JSON 格式输出，例如：{"intent": "email"}
                {"intent": "email"} 或 {"intent": "database"} 或 {"intent": "chat"}
                键名必须且只能是 intent，不要输出任何其他键
            """),
        state["messages"][-1],
    ]
    rs = structured_model.invoke(prompt)
    print(rs)
    return {'intent': rs.intent}
if __name__ == "__main__":
    test_state = {"messages": [HumanMessage(content="帮我给张三发一封邮件")]}

    # 调用 nodewu
    result = router_node(test_state)
    print("识别结果:", result)
