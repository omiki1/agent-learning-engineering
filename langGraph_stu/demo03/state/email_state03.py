from typing_extensions import TypedDict,Annotated
from langchain.messages import AnyMessage
import operator

"""
邮件状态节点
"""
class EmailState(TypedDict):
     #消息
     messages:Annotated[list[AnyMessage], operator.add]
     #用户名
     name:str
     #邮箱
     email:str
     #主题
     subject:str
     #内容
     content:str
     #结果 ：可选
     result:str
     #当前节点的步骤
     current_step:str
