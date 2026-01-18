import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("8069792519:AAG7U4gQ9TFaP4eKsFNtTHwc1NdU1_DVJ0w")
CHAT_ID = os.getenv("1356464009")

URL = "https://rds4.northsouth.ac.bd/index.php/offeredcourses"
COURSE_CODE = "CSE299"
SECTION = "17"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print("Telegram response:", r.text)


def check_seat():
    r = requests.get(URL, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    for row in soup.find_all("tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 6:
            continue

        if cols[0] == COURSE_CODE and cols[1] == SECTION:
            return int(cols[5])

    return None


def main():
    print("Bot token loaded:", BOT_TOKEN is not None)
    print("Chat ID loaded:", CHAT_ID is not None)

    seats = check_seat()
    print("Seats found:", seats)

    # ---- Force test message ----
    send_telegram(
        f"✅ Bot is working!\n{COURSE_CODE} Section {SECTION}\nSeats: {seats}"
    )


if __name__ == "__main__":
    main()
