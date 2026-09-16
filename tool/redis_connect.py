import os
from pathlib import Path

import redis
from dotenv import load_dotenv


def redis_connect():
    base = Path(__file__).resolve()
    candidates = [
        base.parents[1] / ".env",
        base.parent / ".env",
    ]
    loaded = any(p.exists() and load_dotenv(p) is not None for p in candidates)
    if not loaded:
        load_dotenv()

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None  # 空串视为无密码
    client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )
    return client