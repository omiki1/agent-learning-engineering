from memory.retrieval.summary_agent import SummaryAgent
from memory.manager.session_manager import SessionManager
from memory.retrieval.long_agent import LongAgent

class MemoryManager:

   def __init__(self,sessionManger:SessionManager):
       #摘要智能体
       self.summary_agent = SummaryAgent(sessionManger.summary_memory)
       #获取窗口记忆对象
       self.window_memory = sessionManger.window_memory
       #创建长期记忆智能体
       self.long_agent = LongAgent(sessionManger.long_memory)

   def update(self,user_id,question):
       #获取查询的窗口记忆
       query_window = self.window_memory.query()
       #更新长期记忆
       self.long_agent.update(user_id,question)

       if len(self.window_memory.query()) >=2:
           self.summary_agent.update(query_window)