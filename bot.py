import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TARGET = os.getenv("TARGET_EMAIL")

def send_reminder(name):
    subject = f"🎉 Rappel : Anniversaire de {name} aujourd'hui !"
    body = (
        f"Salut Hervé,\n\n"
        f"Aujourd'hui c'est l'anniversaire de {name} 🎂🎉.\n\n"
        "— BirthdayReminderBot 🤖\n"
    )

    msg = MIMEText(body)
    msg["From"] = EMAIL
    msg["To"] = TARGET
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

def check_birthdays():
    today = datetime.now().strftime("%m-%d")

    with open("reminders.json") as f:
        data = json.load(f)

    for name, date in data.items():
        if date == today:
            send_reminder(name)

if __name__ == "__main__":
    check_birthdays()
