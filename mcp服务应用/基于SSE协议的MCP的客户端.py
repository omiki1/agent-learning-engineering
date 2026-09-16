import asyncio
from fastmcp import Client
async def test():
    async with Client(
        'http://localhost:9000/sse'
    ) as client:
        rs = await client.list_tools()
        print(rs)
        data = await client.call_tool(
            "send_email_tool", {"to": "2524279897@qq.com", "subject": "测试", "content": "这是测试"}
        )
        print(data)
if __name__ =="__main__":
    asyncio.run(test())
