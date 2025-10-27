# app/utils.py

import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "shamijhn151@gmail.com"
    SMTP_PASS = "ffyl vrvw iqmi zmeu"

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {to}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import EmailStr
# from typing import List

# conf = ConnectionConfig(
#     MAIL_USERNAME="ahtishamjhn@gmail.com",
#     MAIL_PASSWORD="hzra jzzj yphq uxhh",
#     MAIL_FROM="ahtishamjhn@gmail.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True
# )

# async def send_email(to: EmailStr, subject: str, body: str):
#     fm = FastMail(conf)
#     message = MessageSchema(
#         subject=subject,
#         recipients=[to],
#         body=body,
#         subtype="plain"
#     )
#     await fm.send_message(message)
