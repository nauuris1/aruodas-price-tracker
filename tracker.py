import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://m.en.aruodas.lt/sklypai-kedainiuose-keleriskiu-k-jaunimo-g-parduodamas-aru-namu-valdos-sklypas-su-11-1463258/"

SENDER_EMAIL = os.environ["landplotbot@gmail.com"]
SENDER_PASSWORD = os.environ["$26NPlane26$"]
RECEIVER_EMAIL = os.environ["naurisnaruse@gmail.com"]

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    price = soup.find(string=lambda t: t and "€" in t)
    return price.strip() if price else None

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
