

from langchain.agents.middleware import before_model, AgentState, after_model

from langgraph.runtime import  Runtime
import re
from langchain_core.messages import AIMessage

"""
过滤黄，毒，赌信息
"""
@before_model
def word_filter_middleware(state:AgentState,time:Runtime):
    print("验证是否在模型调用之前执行")
    print(state)
    print(time)
    #用户问题
    question = state["messages"][-1].content
    #查询数据库或者查询外部文件
    word_list =["赌博","嫖娼","吸毒"]
    for x in word_list:
        if x in question:
            raise ValueError("包含敏感词，不允许生成")

    return {}

@after_model
def word_ping_middleware(state:AgentState,time:Runtime):
    print("验证是否在模型调用之后执行")
    print(state)
    print(time)
    # 用户问题
    question = state["messages"][-1].content
    # 查询数据库或者查询外部文件
    word_list = ["赌博", "嫖娼", "吸毒"]
    for x in word_list:
        if x in question:
           #获取过滤后的内容
           data = re.sub(x,"***",question)
           return {
                "messages":[ AIMessage(content=data)]
           }
    #没有任何修改
    return {}


