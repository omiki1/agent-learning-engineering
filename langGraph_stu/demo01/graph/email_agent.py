from langgraph.graph import StateGraph, START, END
from langGraph_stu.demo01.node.chat_node import chat_node
from langGraph_stu.demo01.node.condition_node import query_router, intention_router
from langGraph_stu.demo01.state.state import State
from langGraph_stu.demo01.node.send_email_node import email_node
from langGraph_stu.demo01.node.query_node import query_node
from langGraph_stu.demo01.node.intention_node import intention_node
from langGraph_stu.demo01.node.router_node import router_node

def email_agent():
    graph = StateGraph(State)
    graph.add_node('router',router_node)
    graph.add_node('chat', chat_node)
    graph.add_node('intention', intention_node)
    graph.add_node('query', query_node)
    graph.add_node('email', email_node)

    graph.add_edge(START, 'router')
    graph.add_conditional_edges(
        'router',
        intention_router,
        {
            'chat':'chat',
            'email':'intention',
        }

    )

    graph.add_edge('chat', END)
    graph.add_edge('intention', 'query')
    graph.add_conditional_edges(
        'query',
        query_router,
        {
            "go": "email",
            "end": END,
            'back':'intention',
        }
    )
    graph.add_edge('email', END)

    agent = graph.compile()
    return agent
