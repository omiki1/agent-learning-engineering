from tool.redis_connect import redis_connect
client = redis_connect()


# 保存
def test01():
    # 同一个键只能是一种数据类型：上一个示例（列表.py）把 user:1 存成了 List，
    client.delete("user:1")
    # 存取
    client.hset("user:1", "name", "李四")
    client.hset("user:1", "email", "1111@qq.com")
    client.hset("user:1", "department", "部门")
    client.hset("user:1", "num", 10)
    # 设置失效时间（15 秒后该键自动删除）
    client.expire("user:1", 15)
    print("保存成功")


# 获取
def test02():
    rs = client.hgetall("user:1")
    if rs:
        # 连接时已 decode_responses=True，返回的就是 str，不需要再 .decode()
        name = client.hget("user:1", "name")
        email = client.hget("user:1", "email")
        department = client.hget("user:1", "department")
        num = client.hget("user:1", "num")
        print(name, email, department, num)


if __name__ == "__main__":
    test01()
    test02()