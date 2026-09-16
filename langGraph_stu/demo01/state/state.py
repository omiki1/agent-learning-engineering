from typing_extensions import TypedDict,Annotated
from langchain.messages import AnyMessage
import operator
"""
节点
"""
class State(TypedDict):
    # 消息
    messages: Annotated[list[AnyMessage], operator.add]
    # 用户名
    name: str
    # 用户邮箱
    email: str
    subject: str
    # 内容
    content: str
    # 结果 ：可选
    result: str
    next_step: str
    intent: str
    count: int

