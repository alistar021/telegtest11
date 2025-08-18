from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import re

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"   # یا آیدی عددی کانال
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎉 سلام! خوش آمدید. لطفاً نام و نام خانوادگی خود را وارد کنید:")

def handle_text(update: Update, context: CallbackContext):
    # کد متن...
    pass

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data

    if "phone" not in user_data:
        update.message.reply_text("❗ ابتدا شماره موبایل را وارد کنید، سپس عکس ارسال کنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
    photo_file.download("temp.jpg")

    try:
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

        keyboard = [[InlineKeyboardButton("ثبت نهایی ✅", url=REGISTER_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "✅ اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:",
            reply_markup=reply_markup
        )

        update.message.reply_text(
            "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت اتومات شما را وارد گروه خواهند کرد."
        )

        user_data.clear()

    except Exception as e:
        update.message.reply_text("⚠️ مشکلی در ارسال اطلاعات به کانال پیش آمد.")
        logging.error(f"Error sending to channel: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
