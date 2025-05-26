import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

async def send_verification_code(email: str, code: str):
    SMTP_HOST = getenv("SMTP_HOST")
    SMTP_PORT = int(getenv("SMTP_PORT", 465))
    SMTP_USER = getenv("SMTP_USER")
    SMTP_PASSWORD = getenv("SMTP_PASSWORD")

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('send_verification_code.html')
    html_content = template.render(code=code)

    message = MIMEMultipart()
    message["Subject"] = "Account Verification"
    message["From"] = SMTP_USER
    message["To"] = email
    message.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Email sending failed: {str(e)}")