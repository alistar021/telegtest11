from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = -1006758587605
REGISTER_LINK = "https://t.me/azadunivercitybrj"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎓 سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # مرحله اسم و فامیل
    if "name" not in user_data:
        user_data["name"] = text
        update.message.reply_text(
            f"👋 خوش آمدی {text}!\n\n📌 ما برای امنیت و اطلاع‌رسانی، این ربات را طراحی کردیم. لطفاً شماره موبایل خود را وارد کنید:"
        )
    
    # مرحله شماره موبایل
    elif "phone" not in user_data:
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("❌ لطفاً شماره موبایل معتبر (11 رقم و با 09 شروع شود) وارد کنید.")
            return
        user_data["phone"] = text
        update.message.reply_text("📸 حالا لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید:")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data or "phone" not in user_data:
        update.message.reply_text("❗ لطفاً ابتدا نام و شماره موبایل خود را وارد کنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
    
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", url=REGISTER_LINK)]]
    update.message.reply_text(
        "✅ اطلاعات شما ثبت شد! بعد از بررسی تیم فنی، شما به گروه اضافه خواهید شد.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    user_data.clear()

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
