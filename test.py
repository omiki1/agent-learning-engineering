import json
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from model.my_model import MyModel
from tool.router_tool import router_tool


if __name__ == '__main__':
    # 方案 A(推荐):直接调用路由工具,拿到标准 JSON 字符串
    # router_tool 内部用的是非流式模型(get_router_model),稳定且干净
    result_str = router_tool.invoke({"question": "我想要聊天"})
    print("工具返回的 JSON 字符串:", result_str)

    route = json.loads(result_str)
    print("解析结果:", route)
    print("目标智能体:", route["agent"], "| 置信度:", route["confidence"])
