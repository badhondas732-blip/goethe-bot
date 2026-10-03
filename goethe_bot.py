from telegram import Bot
import asyncio
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

TOKEN = "8986025791:AAHUhdVOuLZpCuEvkTaWEoy5lOrabeYZ6Lw"
CHAT_ID = "5761204561"

URLS = {
    "A1 Exam": "https://www.goethe.de/ins/bd/en/spr/prf/gzsd1.cfm",
    "A2 Exam": "https://www.goethe.de/ins/bd/en/spr/prf/gzsd2.cfm",
    "B1 Exam": "https://www.goethe.de/ins/bd/en/spr/prf/gzb1.cfm",
    "B2 Exam": "https://www.goethe.de/ins/bd/en/spr/prf/gzb2.cfm",
    "Courses": "https://www.goethe.de/ins/bd/en/spr/kur/all.html",
    "Registration": "https://www.goethe.de/dha-reg",
}

bot = Bot(token=TOKEN)

async def send_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print("Message error:", e)

def check_page(name, url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        if "A1" in name or "A2" in name:
            if "book" in page_text:
                return True

        if "B1" in name or "B2" in name:
            if "select modules" in page_text:
                return True

        if "Courses" in name or "Registration" in name:
            if any(word in page_text for word in ["bookable", "select", "registration open"]):
                if not any(word in page_text for word in ["fully booked", "sold out", "booking period expired"]):
                    return True
        return False
    except Exception as e:
        print("Error:", e)
        return False

async def main():
    await send_message("Goethe bot started successfully!")
    last_status = {name: False for name in URLS}

    while True:
        print("[" + datetime.now().strftime("%H:%M:%S") + "] Checking...")

        for name, url in URLS.items():
            is_available = check_page(name, url)
            previous = last_status.get(name, False)

            if is_available and not previous:
                msg = "Alert! " + name + " seats available!\n\nLink: " + url
                await send_message(msg)
                print("Notification sent for " + name)

            last_status[name] = is_available
            time.sleep(2)

        time.sleep(180)

if __name__ == "__main__":
    asyncio.run(main())