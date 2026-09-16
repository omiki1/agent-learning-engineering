from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from model.my_model import MyModel
from memory.save.long_memmory import LongMemory


class LongAgent:

    def __init__(self, long_memory: LongMemory):
        self.model = MyModel.get_local_model()
        self.prompt = self.get_prompt()
        self.agent = self.get_agent()
        # 获取长期记忆的保存对象
        self.long_memory = long_memory

    def get_prompt(self):
        self.prompt = """
           一: 角色：你是一个长期记忆助手
           二：任务：
                  - 根据用户问题提取相关长期记忆信息
           三：规则：
                  1、保持用户的爱好,兴趣,习惯,技能
                  2、去掉闲聊内容
                  3、避免重复
                  4、控制在200字以内
                  5、使用第三人称描述
                  6、不要做总结，只记录重要信息即可


        """
        return self.prompt

    def get_agent(self):
        self.agent = create_agent(
            model=self.model,
            system_prompt=self.prompt,
            tools=[],
            debug=True

        )
        return self.agent

    def update(self, user_id,question):
        # 提问
        rs = self.agent.invoke({"messages": [HumanMessage(content=question)]})
        # 把新摘要存入到摘要记忆中
        self.long_memory.save(user_id,rs["messages"][-1].content)
        print("长期记忆更新成功")

if __name__ == "__main__":
    Long_memory =LongMemory()
    agent = LongAgent(Long_memory)
    q1="我喜欢打游戏"
    q2="我擅长编程"
    agent.update(1,q2)