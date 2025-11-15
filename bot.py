import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# Récupération des variables depuis GitHub Secrets
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TARGET = os.getenv("TARGET_EMAIL")

def send_reminder(name):
    print(f"[INFO] Envoi de l'email pour : {name}")

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

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print("[SUCCÈS] Email envoyé !")
    except Exception as e:
        print(f"[ERREUR] Impossible d'envoyer l'email : {e}")

def check_birthdays():
    today = datetime.now().strftime("%d/%m")  # Format JJ/MM
    print(f"[INFO] Aujourd'hui : {today}")

    # Lecture du fichier JSON
    with open("reminders.json") as f:
        data = json.load(f)

    found = False
    for name, date in data.items():
        print(f"[CHECK] Vérification : {name} -> {date}")
        if date == today:
            found = True
            send_reminder(name)

    if not found:
        print("[INFO] Aucun anniversaire aujourd'hui.")

if __name__ == "__main__":
    check_birthdays()
