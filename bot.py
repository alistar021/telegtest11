# bot.py
import subprocess
import sys
import os
import shutil
from flask import Flask
from telegram import Bot

# نصب خودکار کتابخونه‌ها
subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests==2.31.0"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.2"])

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
if name == "__main__":
    send_photo()
    clear_cache()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
