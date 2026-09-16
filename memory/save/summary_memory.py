from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()

# 连接串只从 .env 的 POSTGRESQL_URL 读取，不要把真实口令写进代码
CONNINFO = os.getenv("POSTGRESQL_URL")

pool = ConnectionPool(
    conninfo=CONNINFO,
    max_size=20,#最大连接数，生成环境是20个
    min_size=10,#最小连接数，生成环境是10个
)
class SummaryMemory:
    def __init__(self, session_id):
        self.session_id = session_id
    def save(self,summary:str):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql =f"INSERT INTO conversation_summary(session_id, summary) VALUES('{self.session_id}','{summary}') ON CONFLICT(session_id) DO UPDATE SET summary=EXCLUDED.summary,update_time=NOW()"
                cur.execute(sql)
                con.commit()
    def query(self):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql = f"select summary from conversation_summary where session_id ='{self.session_id}'"
                cur.execute(sql)
                #查询单个值
                rs = cur.fetchone()

                if rs:
                    return rs[0]
                else:
                    return ""
if __name__ =="__main__":
    s = SummaryMemory("002")
    # s.save()
    s.query()

