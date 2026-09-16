from pandas.tseries.holiday import next_monday

from langGraph_stu.demo03.state.email_state03 import EmailState
from langgraph.graph import END
from langgraph.types import Command
"""
主管节点，处理任务分发
"""
def manager_node(state:EmailState):
    print(f"当前步骤是:{state}")
    #主管觉得下一步做什么，获取当前步骤信息
    current_step = state.get("current_step","start")
    if current_step =="start":
        next_node ="internet"
    elif current_step =="internet_node":
        next_node = "query"
    elif current_step == "query_node":
        next_node = "email"
    elif current_step == "email_node":
        next_node = END
    else:
        next_node = END
    #动态跳转节点
    return Command(goto=next_node)


if __name__ =="__main__":
    data ={"name":"","age":23}
    #print(f"name={data["address"]}")
    print(f"name={data.get("address","a")}")
