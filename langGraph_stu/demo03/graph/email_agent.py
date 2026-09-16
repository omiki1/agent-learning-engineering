from langgraph.graph import StateGraph,START,END
from langGraph_stu.demo03.state.email_state03 import EmailState
from langGraph_stu.demo03.node.email_node03  import email_node
from langGraph_stu.demo03.node.query_node03 import query_node
from langGraph_stu.demo03.node.internet_node03 import internet_node
from langGraph_stu.demo03.node.manager_node import manager_node
"""
创建一个大脑或者智能体
"""
def email_agent():
    #获取图行结构
    graph = StateGraph(EmailState)
    #顺序图添加
    graph.add_node("internet",internet_node)
    graph.add_node("query", query_node)
    graph.add_node("email",email_node)
    graph.add_node("manager_node",manager_node)
    #画边
    graph.add_edge(START, "manager_node")
    graph.add_edge("internet","manager_node")
    graph.add_edge("query", "manager_node")
    graph.add_edge("email", "manager_node")

    #编译
    agent = graph.compile()
    return agent


