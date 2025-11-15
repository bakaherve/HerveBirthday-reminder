import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(targets, birthday_person):
    subject = f"🎉 Aujourd'hui, un Bakatamba change d'âge : {birthday_person} !"
    body = (
        f"Salut les frères,\n\n"
        f"Aujourd'hui c'est l'anniversaire de {birthday_person} 🎂🎉.\n"
        f"N'oubliez pas de lui souhaiter un bon anniversaire !\n\n"
        "— BakatambaBot 🤖"
    )

    msg = MIMEText(body)
    msg["From"] = EMAIL
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            for t in targets:
                msg["To"] = t
                server.send_message(msg)
                print(f"[OK] Email envoyé à → {t}")
    except Exception as e:
        print(f"[ERREUR SMTP] {e}")

def check_birthdays():
    today = datetime.now().strftime("%d/%m")
    print(f"[INFO] Aujourd'hui : {today}")

    with open("reminders.json") as f:
        data = json.load(f)

    is_birthday = False

    for name, info in data.items():
        date = info["date"]
        if date == today:
            is_birthday = True
            print(f"[INFO] 🎉 Anniversaire détecté : {name}")

            target_email = info["email"]
            other_emails = [d["email"] for p, d in data.items() if p != name]

            send_email(other_emails, name)

    if not is_birthday:
        print("[INFO] Aucun anniversaire aujourd'hui.")

if __name__ == "__main__":
    check_birthdays()
