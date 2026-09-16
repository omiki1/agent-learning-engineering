"""使用 SDK v2 内存 Client 测试 Server，不启动子进程。"""

from __future__ import annotations

import asyncio
import json
import sys

from mcp import Client
from server import mcp

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("TOOLS", [tool.name for tool in tools.tools])
        result = await client.call_tool("query_course_topics", {"keyword": "Agent", "limit": 3})
        print("RESULT", json.dumps(result.structured_content, ensure_ascii=False, indent=2))
        resource = await client.read_resource("course://overview")
        print("RESOURCE_BLOCKS", len(resource.contents))


if __name__ == "__main__":
    asyncio.run(main())
