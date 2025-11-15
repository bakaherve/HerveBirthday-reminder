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

def notify_brothers(name, notify_list, message_type="default"):
    # Messages
    if message_type == "papa":
        subject = "🎉 Aujourd'hui, notre cher Papa fête son anniversaire !"
        body = (
            "Salut les frères,\n\n"
            "Aujourd'hui c'est l'anniversaire de notre cher papa ❤️🎉.\n"
            "N'oublions pas de lui souhaiter un bon anniversaire et de l'appeler !\n\n"
            "— BakatambaBot 🤖"
        )
    else:
        subject = f"🎉 Aujourd'hui, un Bakatamba change d'âge : {name} !"
        body = (
            f"Salut les frères,\n\n"
            f"Aujourd'hui c'est l'anniversaire de {name} 🎂🎉.\n"
            "N'oubliez pas de lui souhaiter un bon anniversaire !\n\n"
            "— BakatambaBot 🤖"
        )

    # Envoi à toute la liste
    for email in notify_list:
        send_email(email, subject, body)

def check_birthdays():
    today = datetime.now().strftime("%m-%d")

    with open("birthdays.json") as f:
        data = json.load(f)

    for name, info in data.items():
        if info["date"] == today:

            print(f"🎯 ANNIVERSAIRE TROUVÉ : {name}")

            if name == "Papa":
                notify_brothers(name, info["notify"], message_type="papa")
            else:
                notify_brothers(name, info["notify"], message_type="default")

        else:
            print(f"— Pas d'anniversaire pour {name}")

if __name__ == "__main__":
    check_birthdays()
