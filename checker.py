import requests
from bs4 import BeautifulSoup
import os
import json

BOT_TOKEN = os.getenv("8069792519:AAG7U4gQ9TFaP4eKsFNtTHwc1NdU1_DVJ0w")
CHAT_ID = os.getenv("1356464009")

URL = "https://rds4.northsouth.ac.bd/index.php/offeredcourses"

COURSE_CODE = "CSE299"
SECTION = "17"
STATE_FILE = "state.json"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"alerted": False}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

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
    state = load_state()
    seats = check_seat()

    if seats is None:
        return

   if True:

        send_telegram(f"🎉 Seat Available!\n{COURSE_CODE} Section {SECTION}\nSeats: {seats}")
        state["alerted"] = True

    if seats == 0:
        state["alerted"] = False

    save_state(state)

if __name__ == "__main__":
    main()
