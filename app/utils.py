# app/utils.py
from email.mime.text import MIMEText
import smtplib

def send_email(to: str, subject: str, body: str):
    """
    Simple utility for sending emails.
    For development it just prints the message.
    Replace the print block with SMTP settings when ready.
    """
    # Development / testing: just show the message in console
    # print(f"\n[DEV EMAIL] To: {to}\nSubject: {subject}\n\n{body}\n")

    # --- Example SMTP (commented out) ---
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "ahtishamjhn@gmail.com"
    msg["To"] = to
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("ahtishamjhn@gmail.com", "hzra jzzj yphq uxhh")
        server.send_message(msg)


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
