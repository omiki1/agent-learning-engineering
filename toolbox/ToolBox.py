import requests
from langchain.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.header import Header
import smtplib
class EmailParams(BaseModel):
    to: str = Field(..., description='收件人邮箱')
    subject: str = Field(..., description='主题')
    context: str = Field(..., description='内容')
class WeatherTool(BaseModel):
    city: str = Field(..., description="城市名称，如 北京、上海")
class MyTool():
    def __init__(self):
        self._tools = self.build_tools()
    def build_tools(self)->[]:
        @tool(
            name_or_callable="get_weather",
            description="""
                        当用户需要查询某个城市的天气时，调用此工具。
                        参数：city，字符串类型，表示城市名称。
                    """,
            args_schema=WeatherTool,
        )
        def get_weather(city: str):
            print(f"查询天气的城市：{city}")
            print(f'正在查询天气')
            url = "https://restapi.amap.com/v3/weather/weatherInfo"
            params = {
                "key": os.getenv("WEATHER"),
                "city": city,
                "extensions": "base",  # 返回实时天气
            }
            try:
                rs = requests.get(url, params=params, timeout=10)
                data = rs.json()
                if data.get("status") == "1" and data.get("lives"):
                    live = data["lives"][0]
                    return f"{live['city']}的天气：{live['weather']}，温度：{live['temperature']}℃"
                return f"查询{city}天气失败：{data.get('info', '未知错误')}"
            except Exception as e:
                return f"查询天气时发生错误：{str(e)}"

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
                return f'邮件发送成功:{to}'
            except Exception as e:
                return f'邮件发送失败:{type(e).__name__}:{e}'

        @tool(
            name_or_callable="get_time",
            description="""当用户需要查询时间，调用此工具。""",
        )
        def get_time() -> str:
            """获取当前时间"""
            now = datetime.now()
            return now.strftime('%Y-%m-%d %H:%M:%S')



        return [get_weather, send_email_tool,get_time]
    def get_tools(self):
        return self._tools
