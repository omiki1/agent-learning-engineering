from langchain.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from pathlib import Path
from email.mime.text import MIMEText
from email.header import Header
import smtplib

load_dotenv()

class EmailParams(BaseModel):
    to: str = Field(..., description='收件人邮箱')
    subject: str = Field(..., description='主题')
    context: str = Field(..., description='内容')

@tool('send_email_tool', args_schema=EmailParams)
def send_email_tool(to: str, subject: str, context: str) -> str:
    """
    发送邮件，通知
    """
    sender = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_EMAIL_PASSWORD')
    host = os.getenv('SMTP_HOST')
    port = os.getenv('SMTP_PORT')

    if not all([sender, password, host, port]):
        return ('邮件发送失败:缺少 SMTP 配置,请检查 .env 中的 '
                'SENDER_EMAIL / SENDER_EMAIL_PASSWORD / SMTP_HOST / SMTP_PORT')

    msg = MIMEText(context, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        with smtplib.SMTP(host, int(port), timeout=15) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, [to], msg.as_string())
        return f'邮件发送成功'
    except Exception as e:
        return f'邮件发送失败'
