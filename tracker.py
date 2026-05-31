import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://m.en.aruodas.lt/sklypai-kedainiuose-keleriskiu-k-jaunimo-g-parduodamas-aru-namu-valdos-sklypas-su-11-1463258/"

SENDER_EMAIL = os.environ["EMAIL"]
SENDER_PASSWORD = os.environ["APP_PASSWORD"]
RECEIVER_EMAIL = os.environ["EMAIL"]

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)

    print("Status code:", r.status_code)
    print("Page length:", len(r.text))

    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(r.text)

    return "DEBUG"

def send_email(old, new):
    msg = MIMEText(f"Price changed!\n\nOld: {old}\nNew: {new}\n\n{URL}")
    msg["Subject"] = "Aruodas Price Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def main():
    current = get_price()
    if not current:
        print("No price found")
        return

    try:
        old = open("price.txt").read().strip()
    except:
        old = ""

    print("Old:", old, "New:", current)

    if old and old != current:
        send_email(old, current)

    with open("price.txt", "w") as f:
        f.write(current)

main()
