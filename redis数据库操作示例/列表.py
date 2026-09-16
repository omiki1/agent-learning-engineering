from tool.redis_connect import redis_connect
client = redis_connect()
def test01():
    left_data = client.lpush("user:1","a","b","c")
    data = client.lrange("user:1", 0, -1)
    print(data)
def test03():
    #删除一个元素并且弹出一个元素
    data =client.rpop("user:1")
    print(data)
if __name__ == '__main__':
    test01()
