import os
import shutil
from flask import Flask
from telegram import Bot

# ---------- تنظیمات ----------
TOKEN = "8476998300:AAEk3pHApz2Ex1GbZjX7fFc6qL883opak2A"
CHANNEL_ID = "@alialisend123"
PHOTO_PATH = "image.jpg"  # مسیر عکس برای ارسال

bot = Bot(token=TOKEN)

# ---------- ارسال عکس ----------
def send_photo():
    try:
        with open(PHOTO_PATH, "rb") as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=photo)
        print("عکس ارسال شد.")
    except Exception as e:
        print("خطا در ارسال عکس:", e)

# ---------- پاک کردن کش و فایل‌های موقت ----------
def clear_cache():
    temp_dirs = ["./downloads", "./temp"]
    for d in temp_dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"پاک شد: {d}")

# ---------- Webhook و Flask ----------
app = Flask(__name__)

@app.route("/")
def index():
    return "ربات فعال است!"

# ---------- اجرای اصلی ----------
if __name__ == "__main__":
    send_photo()
    clear_cache()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
