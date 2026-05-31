from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://m.en.aruodas.lt/sklypai-kedainiuose-keleriskiu-k-jaunimo-g-parduodamas-aru-namu-valdos-sklypas-su-11-1463258/"

EMAIL = os.environ["EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

def send_email(old, new):
    msg = MIMEText(f"Price changed!\n\nOld: {old}\nNew: {new}\n\n{URL}")
    msg["Subject"] = "Aruodas Price Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

def get_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait for page to fully load
        page.wait_for_timeout(5000)

        # try multiple ways to find price
        selectors = [
            ".obj-price",
            "span:has-text('€')",
            "[class*='price']"
        ]

        for sel in selectors:
            el = page.query_selector(sel)
            if el:
                price = el.inner_text().strip()
                if "€" in price:
                    browser.close()
                    return price

        # fallback: search whole page text
        content = page.content()
        browser.close()

        return None

def main():
    current = get_price()

    if not current:
        print("No price found")
        return

    try:
        old = open("price.txt").read().strip()
    except:
        old = ""

    print("Old:", old)
    print("New:", current)

    if old and old != current:
        send_email(old, current)

    with open("price.txt", "w") as f:
        f.write(current)

main()
