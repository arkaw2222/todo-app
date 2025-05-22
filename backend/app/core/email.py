import smtplib
from email.mime.text import MIMEText
from os import getenv
from dotenv import load_dotenv

load_dotenv()

async def send_verification_code(email: str, code: str):
    SMTP_HOST = getenv("SMTP_HOST")
    SMTP_PORT = int(getenv("SMTP_PORT", 465))
    SMTP_USER = getenv("SMTP_USER")
    SMTP_PASSWORD = getenv("SMTP_PASSWORD")

    message = MIMEText(f"Your verification code: {code}", 'plain', 'utf-8')
    message["Subject"] = "Account Verification"
    message["From"] = SMTP_USER
    message["To"] = email

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        raise RuntimeError(f"Email sending failed: {str(e)}")