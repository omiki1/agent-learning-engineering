from langchain_core.messages import HumanMessage

from langGraph_stu.demo03.graph.email_agent import email_agent

import asyncio
async def test1():
    graph = email_agent()
    input = {"messages": [HumanMessage(content="给bobo你发个邮件，说今晚开会")]}
    async for chunk, metadata in graph.astream(input, stream_mode="messages",):
            yield chunk.content

#画流程图
def draw_graph():
    agent = email_agent()
    #画图
    data = agent.get_graph().draw_mermaid_png()
    #
    with open("动态路由图.png","wb") as f:
        f.write(data)
    print("动态路由图.png")

if __name__=="__main__":
    draw_graph()
    async def test():
        async for rs in test1():
            print(rs,end="")
    asyncio.run(test())