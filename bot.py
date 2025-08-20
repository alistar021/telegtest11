from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ====== تنظیمات ربات ======
BOT_TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"  # توکن ربات
CHANNEL_USERNAME = "@alialisend123"  # نام کانال

# ساخت شیء ربات
bot = Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ====== دستور استارت ======
def start(update: Update, context):
    update.message.reply_text("سلام! پیام شما به کانال ارسال می‌شود.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# ====== دریافت پیام و ارسال به کانال ======
def forward_to_channel(update: Update, context):
    message_text = update.message.text
    bot.send_message(chat_id=CHANNEL_USERNAME, text=message_text)
    update.message.reply_text("پیام شما ارسال شد ✅")

message_handler = MessageHandler(Filters.text & (~Filters.command), forward_to_channel)
dispatcher.add_handler(message_handler)

# ====== اجرای ربات ======
updater.start_polling()
updater.idle()
