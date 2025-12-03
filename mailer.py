# mailer.py
import smtplib
from email.message import EmailMessage

from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = f"Nadeem Ahmed Mir <{GMAIL_ADDRESS}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
