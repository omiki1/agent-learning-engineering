import json
from dotenv import load_dotenv
import os
from tool.redis_connect import redis_connect
load_dotenv()
class WindowMemory:
    def __init__(self,session_id):
        self.redis =  redis_connect()
        self.window_size = int(os.getenv("WINDOW_MEMORY_ROUNDS"))
        self.session_id = session_id
        self.key = f"window_memory:{self.session_id}"
        # 过期时间
        self.window_limit_time = int(os.getenv("WINDOW_MEMORY_TIME"))

    # 保存记忆
    def save(self, role: str, content: str):
        # 构建字典
        data = {"role": role, "content": content}
        # 添加到列表种
        self.redis.rpush(self.key, json.dumps(data, ensure_ascii=False))
        # 设置保留窗口记忆
        self.redis.ltrim(self.key, -self.window_size, -1)
        # 设置过期时间
        self.redis.expire(self.key, self.window_limit_time)

    # 提取记忆
    def query(self):
        # 判断建是否存在
        if self.redis.exists(self.key):
            data = self.redis.lrange(self.key, 0, -1)
            return [json.loads(i) for i in data]
if __name__ =="__main__":
    w= WindowMemory("001")
    # 模拟人类消息添加
    w.save("user", "你好")
    # 模拟AI回复消息
    w.save("ai", "你好，我是AI助手")
    # 模拟人类消息添加
    w.save("user", "你好1")
    # 模拟AI回复消息
    w.save("ai", "你好1，我是AI助手1")
    # 模拟人类消息添加
    w.save("user", "你好2")
    # 模拟AI回复消息
    w.save("ai", "你好2，我是AI助手2")
    w.save("user", "你好3")
    # 模拟AI回复消息
    w.save("ai", "你好3，我是AI助手2")
    # 查询记忆
    rs = w.query()
    print(rs)