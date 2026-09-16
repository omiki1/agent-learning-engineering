# -*- coding: utf-8 -*-
"""
基于 stdio 协议的 MCP 服务端 (FastMCP)

提供两个工具：
1. send_email_tool : 通过 SMTP 发送邮件
2. mysql_tool      : 只读执行 SQL 查询(查询 MySQL)
"""
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from typing import Annotated

import pymysql
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import EmailStr, Field

# 创建应用程序
app = FastMCP()

# 加载 .env(自动向上查找 C:\workspace\stu_agent\.env)
load_dotenv()


@app.tool("send_email_tool")
def send_email_tool(
    to: Annotated[EmailStr, Field(description="收件人的邮箱")],
    subject: Annotated[str, Field(description="邮件主题", min_length=1, max_length=200)],
    content: Annotated[str, Field(description="邮件正文内容", min_length=1, max_length=10000)],
) -> str:
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


@app.tool(description=(
    "只读执行 SQL 查询,禁止执行任何写操作。"
    "数据库模型:agent_test 库中的 user 用户信息表,字段:"
    "user_id 用户编号, user_name 用户名, email 邮箱。"
    "规则:只允许 SELECT / SHOW 查询语句,禁止生成 DELETE,UPDATE,INSERT,DROP,CREATE,ALTER 语句"
))
def mysql_tool(sql: Annotated[str, Field(description="要执行的 SQL 查询语句,例如:SELECT * FROM user")]) -> str:
    """
    执行 sql 语句查询 MySQL 数据库(只读)
    """
    con = None
    cursor = None
    try:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        if not all([host, port, user, password, db_name]):
            return ("数据库连接参数未配置:请在 .env 中配置 "
                    "DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME")

        # 只读兜底:只放行查询类语句
        sql_stripped = sql.strip()
        sql_upper = sql_stripped.upper()
        if not sql_stripped or not sql_upper.startswith(("SELECT", "SHOW")):
            return "禁止执行非法sql语句操作,只允许 SELECT / SHOW 查询语句"

        con = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            db=db_name,
            charset="utf8",  # 中文编码设置
        )
        cursor = con.cursor()
        # 执行sql
        cursor.execute(sql_stripped)
        rs = cursor.fetchall()
        return str(rs)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


if __name__ == "__main__":
    app.run(transport="stdio")
