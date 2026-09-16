from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import smtplib
from email.header import Header

from fastmcp.server.dependencies import get_access_token
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

from tool.key_verifier import KeyVerifier

#创建应用程序
app = FastMCP(auth=KeyVerifier())
load_dotenv()

@app.tool("send_email_tool")
def send_email_tool(
    to: Annotated[EmailStr,Field(description='收件人的的邮箱')],
    subject:  Annotated[str, Field(description="邮件主题", min_length=1, max_length=200)],
    content:  Annotated[str, Field(description="邮件正文内容", min_length=1, max_length=10000)],
) -> str:
    token = get_access_token()
    print(f'当前请求的访问令牌信息:{token}')
    """
    发送邮件，通知
    """
    if token.client_id == '123456':
        if 'write' in token.scopes:
            sender = os.getenv('SENDER_EMAIL')
            password = os.getenv('SENDER_EMAIL_PASSWORD')
            host = os.getenv('SMTP_HOST')
            port = os.getenv('SMTP_PORT')

            if not all([sender, password, host, port]):
                return ('邮件发送失败:缺少 SMTP 配置,请检查 .env 中的 '
                        'SENDER_EMAIL / SENDER_EMAIL_PASSWORD / SMTP_HOST / SMTP_PORT')

            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = sender
            msg['To'] = to
            msg['Subject'] = Header(subject, 'utf-8')

            try:
                with smtplib.SMTP(host, int(port), timeout=15) as server:
                    server.starttls()
                    server.login(sender, password)
                    server.sendmail(sender, [to], msg.as_string())
                return f'邮件发送成功:{to}'
            except Exception as e:
                return f'邮件发送失败:{type(e).__name__}:{e}'
        else:
            return "必须是write权限"
    else:
        return "客户端无权限"
if __name__ =="__main__":
    app.run(host="localhost",port=9000,transport="sse")
