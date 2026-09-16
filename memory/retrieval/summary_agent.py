from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from model.my_model import MyModel
from memory.save.summary_memory import SummaryMemory

"""
摘要智能体
"""


class SummaryAgent:

    def __init__(self, summary_memory: SummaryMemory):
        self.model = MyModel.get_model()
        self.prompt = self.get_prompt()
        self.agent = self.get_agent()
        # 获取摘要记忆的保存对象
        self.summary_memory = summary_memory

    def get_prompt(self):
        self.prompt = """
           一: 角色：你是一个摘要记忆助手
           二：任务：
                  - 根据旧摘要和最新聊天记录生成新的摘要
           三：规则：
                  1、保留重要信息,例如:姓名，年龄
                  2、去掉闲聊内容
                  3、避免重复
                  4、控制在200字以内
                  5、使用第三人称描述
                  6、只返回新的摘要

        """
        return self.prompt

    def get_agent(self):
        self.agent = create_agent(
            model=self.model,
            system_prompt=self.prompt,
            tools=[],
            # debug=True

        )
        return self.agent

    # 记忆更新
    # messages 窗口记忆的消息
    def update(self, messages):
        # 查询旧摘要
        old_summary_memory = self.summary_memory.query()
        # 最新聊天记录
        prompt = ""
        for i in messages:
            if i["role"] == "user":
                prompt += f"用户提问：{i['content']}"

        question = f"旧摘要:{old_summary_memory}和最新聊天记录:{prompt}"
        # 提问
        rs = self.agent.invoke({"messages": [HumanMessage(content=question)]})
        # 把新摘要存入到摘要记忆中
        print(rs)
        self.summary_memory.save(rs["messages"][-1].content)


if __name__ == "__main__":
    summary_memory = SummaryMemory("002")
    s = SummaryAgent(summary_memory)
    # 最近聊天记录
    record = [{'role': 'user', 'content': '你好，我叫张胜男'}, {'role': 'ai', 'content': '你好，张胜男'},
              {'role': 'user', 'content': 'langchain是什么'}, {'role': 'ai', 'content': 'langchain是一个智能体框架'}]
    s.update(record)




