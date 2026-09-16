from langchain.agents import create_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from model.my_model import MyModel
from langchain_core.messages import HumanMessage
import json


class RouterResult(BaseModel):
    """路由决策的结构化输出:目标智能体 + 置信度"""
    agent: str = Field(..., description="目标智能体名称: email_agent / chat_agent / exam_agent")
    confidence: float = Field(..., description="置信度,0~1之间的小数")


@tool(
    'router_tool',
    description='''
        当用户输入问题需要确定使用哪个智能体的时候，使用这个路由工具决定走哪个智能体,email_agent/chat_agent/exam_agent
    ''',
)
def router_tool(question: str) -> str:
    """根据用户问题判断该交给哪个智能体(email_agent/chat_agent/exam_agent)。

    Args:
        question: 用户的原始输入问题

    Returns:
        JSON 字符串,格式: {"agent": "xxx", "confidence": 0.88}
    规则：
        只输出{"agent":"chat_agent","confidence":1.0}不要带任何其他东西
    """
    structured_model = MyModel.get_router_model().with_structured_output(
        RouterResult,
        method="function_calling",
    )
    rs = structured_model.invoke(question)
    print(rs)
    return rs.model_dump_json()

