import os
from flask import Flask, request
from telegram.ext import CommandHandler, Dispatcher
from telegram import Update, Bot

# ====================
# تنظیمات
# ====================
# توکن ربات (اینجا مستقیم گذاشتم، می‌تونی بعداً در Railway → Variables هم بذاری)
TOKEN = "8476998300:AAEk3pHApz2Ex1GbZjX7fFc6qL883opak2A"

# پورت Railway
PORT = int(os.getenv("PORT", 8080))

# آدرس Railway (اسم پروژه رو ali گذاشتیم)
APP_URL = f"https://ali.up.railway.app/"

# ====================
# تعریف دستورات
# ====================
def start(update, context):
    update.message.reply_text("سلام 👋 ربات با Webhook روی Railway فعاله 🚀")

# ====================
# تنظیم ربات
# ====================
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))

# ====================
# Flask Webhook
# ====================
app = Flask(_name_)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "ربات روشنه ✅"

if _name_ == "_main_":
    # ست کردن وبهوک
    bot.set_webhook(APP_URL + TOKEN)
    app.run(host="0.0.0.0", port=PORT)
