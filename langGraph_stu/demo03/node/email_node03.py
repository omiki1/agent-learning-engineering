from langGraph_stu.demo03.state.email_state03 import EmailState
from tool.send_email_tool import send_email_tool
from langchain_core.messages import AIMessage

def email_node(state:EmailState):
    #邮箱
    email =state["email"]

    #标题
    subject = state["subject"]
    #内容
    content= state["content"]

    #调用邮件工具
    rs = send_email_tool.invoke(
        {"to":email,"subject":subject,"context":content}
    )
    if rs =="邮件发送成功":
        #自定义最终答案结果
        ai_msg =f"\n邮件发送成功\n"
        return {
            "messages":[AIMessage(content=ai_msg)],
            "result": "邮件发送成功",
            "current_step": "email_node"
        }
    else:
        ai_msg = f"\n邮件发送失败\n"
        return {
            "messages": [AIMessage(content=ai_msg)],
            "result": "邮件发送失败",
            "current_step": "error_node"
        }

