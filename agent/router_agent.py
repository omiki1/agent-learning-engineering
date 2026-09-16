from langchain.agents import create_agent
from pydantic import BaseModel, Field
from model.my_model import MyModel
from langchain_core.messages import HumanMessage
from tool.send_email_tool import send_email_tool
class RouterResult(BaseModel):
    """路由决策的结构化输出:目标智能体 + 置信度"""
    agent: str = Field(..., description="目标智能体名称: email_agent / chat_agent / exam_agent")
    confidence: float = Field(..., description="置信度,0~1之间的小数")


class RouterAgent:
    def __init__(self):
        self._model=MyModel.get_model()
        self._agent = {
            "email_agent": self._create_email_agent(),
            "chat_agent": self._create_chat_agent(),
            "exam_agent": self._create_exam_agent(),
        }

    def router_tool(self,question: str):
        """根据用户问题判断该交给哪个智能体(email_agent/chat_agent/exam_agent)。

        Args:
            question: 用户的原始输入问题

        Returns:
            JSON 字符串,格式: {"agent": "xxx", "confidence": 0.88}
        规则：
            只输出{"agent":"chat_agent","confidence":1.0}不要带任何其他东西
        """
        structured_model = self._model.with_structured_output(
            RouterResult,
            method="function_calling",
        )
        rs = structured_model.invoke(question)
        print(rs)
        agent = self._agent[f'{rs.agent}']
        if not agent:
            return f"错误：未找到智能体 {rs.agent}"
        else:
            human_msg = {'messages':[HumanMessage(content=question)]}
            rs = agent.invoke(
                human_msg,
            )

            return rs

    def _create_exam_agent(self):
        return MyModel.get_model()

    def _create_chat_agent(self):
        model = MyModel.get_model()
        return model

    def _create_email_agent(self):
        model = MyModel.get_model()
        tools = [send_email_tool]
        propmt = '''
        你是一个发送邮件的智能助手。
        **任务流程（必须严格遵守）**：
         调用 `send_email_tool` 发送邮件
        '''

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=propmt,
            # debug=True,
        )
        return agent

if __name__ == "__main__":
    agent = RouterAgent()
    rs = agent.router_tool('帮我给 2524279897@qq.com发送邮件,告诉他今天不上课')
    print(rs)