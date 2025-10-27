# # app/utils.py

# import smtplib
# from email.mime.text import MIMEText

# def send_email(to, subject, body):
#     SMTP_SERVER = "smtp.gmail.com"
#     SMTP_PORT = 587
#     SMTP_USER = "shamijhn151@gmail.com"
#     SMTP_PASS = "ffyl vrvw iqmi zmeu"

#     msg = MIMEText(body, "html")
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USER
#     msg["To"] = to

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASS)
#             server.send_message(msg)
#         print(f"✅ Email sent successfully to {to}")
#         return True
#     except Exception as e:
#         print(f"❌ Email failed: {e}")
#         return False

# ...existing code...
import os
import logging
import smtplib
from email.mime.text import MIMEText
from typing import Any

logger = logging.getLogger(__name__)

def send_email(to: str, subject: str, body: str) -> bool:
    """
    Synchronous email sender using SMTP. Credentials are read from env vars:
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS.
    Returns True on success, False on failure (and logs the error).
    """
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("shamijhn151@gmail.com")
    SMTP_PASS = os.getenv("ffyl vrvw iqmi zmeu")

    if not SMTP_USER or not SMTP_PASS:
        logger.error("SMTP_USER or SMTP_PASS not set in environment")
        return False

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        logger.info("✅ Email sent successfully to %s", to)
        return True
    except Exception as e:  # pragma: no cover
        logger.exception("❌ Email failed to %s: %s", to, e)
        return False
# ...existing code...