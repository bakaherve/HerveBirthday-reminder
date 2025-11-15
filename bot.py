import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email, subject, body):
    if "@" not in to_email:
        print(f"❌ Email invalide ignoré : {to_email}")
        return

    msg = MIMEText(body)
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"📨 Email envoyé à {to_email}")
    except Exception as e:
        print(f"⚠️ Erreur en envoyant à {to_email}: {e}")

def send_birthday_notifications(name, notify_list):
    subject = f"🎉 Aujourd'hui, un Bakatamba change d'âge : {name} !"
    
    body = (
        f"Salut les frères,\n\n"
        f"Aujourd'hui c'est l'anniversaire de {name} 🎂🎉.\n"
        f"N'oubliez pas de lui souhaiter un bon anniversaire !\n\n"
        f"— BakatambaBot 🤖"
    )

    for email in notify_list:
        send_email(email, subject, body)

def check_birthdays():
    today = datetime.now().strftime("%m-%d")

    with open("birthdays.json") as f:
        data = json.load(f)

    for name, info in data.items():
        if info["date"] == today:
            print(f"🎯 Anniversaire trouvé : {name}")
            send_birthday_notifications(name, info["notify"])
        else:
            print(f"— Pas d'anniversaire pour {name}")

if __name__ == "__main__":
    check_birthdays()
