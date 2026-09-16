from langgraph.graph import END

from langGraph_stu.demo01.state.state import State


def query_router(state: State):
    data = state["next_step"]
    count = state["count"]
    if data == "email":
        return "go"
    else:
        if count<3:
            return "back"
        else:
            return "end"


def intention_router(state: State):
    mapping = {
        'email': 'email',
        'chat': 'chat',
    }
    intent = state.get('intent')
    return mapping.get(intent, 'chat')




