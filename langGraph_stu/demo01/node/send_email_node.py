from langGraph_stu.demo01.state.state import State
from tool.send_email_tool import send_email_tool
from langchain_core.messages import AIMessage

def email_node(state: State):
    email = state['email']
    subject = state['subject']
    content = state['content']
    rs = send_email_tool.invoke(
        {"to":email,"subject":subject,"context":content},
    )
    if rs =="邮件发送成功":
        #自定义最终答案结果
        ai_msg =f"\n邮件发送成功\n"
        return {
            "messages":[AIMessage(content=ai_msg)],
            "result": "邮件发送成功"
        }
    else:
        ai_msg = f"\n邮件发送失败\n"
        return {
            "messages": [AIMessage(content=ai_msg)],
            "result": "邮件发送失败"
        }

