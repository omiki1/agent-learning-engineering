from langchain_core.tools import tool
from pydantic import BaseModel, Field
import os
import requests

class SearchParams(BaseModel):
    messages: str = Field(
        ...,
        description="用于百度检索的核心查询词或问题。要求：简明扼要，去除语气词和无关修饰，提取用户问题中最具区分度的实体和核心事件。例如：用户说'那个最近很火的AI公司叫什么来着'，应提取为'近期热门AI公司'。",
    )

@tool(
    name_or_callable="search_tool",
    description="当用户需要查询实时信息时使用此工具，返回搜索到的新闻标题和内容摘要。",
    args_schema=SearchParams,
)
def search_tool(messages: str) -> str:
    """
    百度千帆 AI 搜索：返回解析后的新闻文本（标题+摘要），而非原始 JSON。
    """
    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    api_key = os.getenv("BAIDU_KEY")
    headers = {
        "Content-Type": "application/json",
        "X-Appbuilder-Authorization": f"Bearer {api_key}",
    }
    payload = {
        "messages": [{"content": messages, "role": "user"}],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": 5}],
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()

        refs = result.get("references", [])
        if not refs:
            return f"未搜索到关于「{messages}」的结果。"

        lines = [f"关于「{messages}」的搜索结果："]
        for i, ref in enumerate(refs[:5], 1):
            title = ref.get("title", "").strip()
            website = ref.get("website", "")
            content = ref.get("snippet") or ref.get("content") or ""
            content = content.strip()
            lines.append(f"{i}. 【{title}】（来源：{website}）")
            if content:
                lines.append(f"   摘要：{content[:300]}")
        return "\n".join(lines)

    except requests.exceptions.RequestException as e:
        return f"搜索请求失败: {str(e)}"
    except Exception as e:
        return f"处理搜索结果时出错: {str(e)}"

baidu_search = search_tool
