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
# import os
# import logging
# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv  # Import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# logger = logging.getLogger(__name__)

# def send_email(to: str, subject: str, body: str) -> bool:
#     """
#     Synchronous email sender using SMTP. Credentials are read from env vars:
#     SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS.
#     Returns True on success, False on failure (and logs the error).
#     """
#     SMTP_SERVER = os.getenv("SMTP_SERVER")
#     SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
#     SMTP_USER = os.getenv("SMTP_USER")
#     SMTP_PASS = os.getenv("SMTP_PASS")

#     if not SMTP_USER or not SMTP_PASS:
#         print("SMTP_USER or SMTP_PASS not set in environment")
#         return False

#     msg = MIMEText(body, "html")
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USER
#     msg["To"] = to

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
#             # server.ehlo()
#             server.starttls()
#             # server.ehlo()
#             server.login(SMTP_USER, SMTP_PASS)
#             server.send_message(msg)
#         print("✅ Email sent successfully to %s", {to})
#         return True
#     except Exception as e:
#         print(f"❌ Email failed to {to}: {e}")
#         return False
# # ...existing code...

import resend
import os

# Set the Resend API key from environment
resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(to, subject, body):
    try:
        params = {
            "from": "Shami App <shamijhn151@resend.dev>",  # You can later verify your own email/domain
            "to": [to],
            "subject": subject,
            "html": body,
        }

        # Send the email
        email = resend.Emails.send(params)
        print("✅ Email sent successfully:", email)
        return True

    except Exception as e:
        print("❌ Error sending email:", e)
        return False
