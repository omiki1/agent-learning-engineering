from langGraph_stu.demo03.state.email_state03 import EmailState
from tool.mysql_tool import mysql_tool
from langchain_core.messages import ToolMessage
import ast
"""
查询节点
"""
def query_node(state:EmailState):
    #获取用户姓名
    name = state["name"]
    #调用工具
    rs = mysql_tool.invoke({
        "sql":f"select `email` from `user` where user_name='{name}'"
    })

    # mysql_tool 内部把异常也 return 出来了（str(e)），例如 collation 冲突会
    # 返回 '(1267, "Illegal mix of collations ...")' —— 它长得像元组，若直接
    # 下标取值就会 TypeError。所以这里先解析，再判断它到底是不是查询结果。
    try:
        rows = ast.literal_eval(rs)
    except (ValueError, SyntaxError):
        rows = None

    # 正常结果一定是「元组的元组」，如 (('a@b.com',),)；空结果 () 也算合法。
    # 其余（错误码、报错文本）一律按查询失败处理。
    if not isinstance(rows, tuple) or not all(isinstance(r, tuple) for r in rows):
        return {
            "messages":[ToolMessage(content=f"查询失败:{rs}",tool_call_id="query_node")],
            "result":"查询失败",
            "current_step": "error_node"
        }

    if not rows:
        return {
            "messages":[ToolMessage(content="用户邮箱不存在",tool_call_id="query_node")],
            "result":"用户邮箱不存在",
            "current_step": "error_node"
        }

    #获取邮件
    email = rows[0][0]
    #定义结果
    tool_msg =f"\n查询节点成功\n邮箱是:{email}"
    return {
        "messages": [ToolMessage(content=tool_msg, tool_call_id="query_node")],
        "result": "\n用户邮箱查询成功\n",
        "email": email,
        "current_step": "query_node"
    }