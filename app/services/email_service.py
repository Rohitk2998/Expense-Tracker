import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()



def send_email(report_content: str,recipient:str)->None:
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_pass = os.getenv('SMTP_PASSWORD')

    required_values = [
        smtp_host,
        smtp_port,
        smtp_user,
        smtp_pass
    ]

    if not all(required_values):
        raise RuntimeError('Email configuration is missing')

    message = EmailMessage()

    message["Subject"] = "Expense Report"
    message["From"] = smtp_user
    message["To"] = recipient

    message.set_content(report_content)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(message)