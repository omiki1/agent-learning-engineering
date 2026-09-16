import os
from pathlib import Path

import redis
from dotenv import load_dotenv

# 始终加载"本脚本所在目录"下的 .env（不依赖当前工作目录）
load_dotenv(Path(__file__).resolve().parent / ".env")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None  # 空串视为无密码
client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,  # 返回 str 而不是 bytes，方便查看
)

if client.ping():
    client.set('name', 'pl')
    print(client.get('name'))