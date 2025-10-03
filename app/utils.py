# app/utils.py
from email.mime.text import MIMEText
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "shamijhn151@gmail.com"
SMTP_PASS = "vlvk rxzs abzb gtyh"

def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()                     # ✅ TLS start
            server.login(SMTP_USER, SMTP_PASS)    # ✅ Brevo login
            server.send_message(msg)
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")



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
