from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
import re
import logging

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"   # یا آیدی عددی کانال -100xxxx
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎓 سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # مرحله اسم و فامیل
    if "name" not in user_data:
        user_data["name"] = text
        update.message.reply_text(
            f"👋 خوش آمدی {text}!\n\n"
            "📌 برای ادامه روند احراز هویت، لطفاً شماره موبایل خود را وارد کنید:"
        )
        return

    # مرحله شماره موبایل
    elif "phone" not in user_data:
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("❌ شماره موبایل معتبر نیست! (باید 11 رقم و با 09 شروع شود)")
            return
        user_data["phone"] = text
        update.message.reply_text("📸 لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید:")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data or "phone" not in user_data:
        update.message.reply_text("❗ لطفاً اول نام و شماره موبایل خود را وارد کنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"

    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", callback_data="final_register")]]
    update.message.reply_text(
        "✅ اطلاعات شما با موفقیت ثبت شد!\n\n"
        "برای تکمیل مراحل روی دکمه زیر کلیک کنید 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    user_data.clear()

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "final_register":
        # پیام فعلی رو ویرایش می‌کنیم
        query.edit_message_text(
            "🙏 از همراهی شما سپاسگزاریم.\n\n"
            "👨‍💻 تیم فنی پس از بررسی اطلاعات شما، شما را به گروه اضافه خواهد کرد."
        )
        # پیام جدید با لینک کانال
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                "📢 برای اطلاع‌رسانی و دسترسی سریع‌تر به اخبار، به کانال رسمی دانشگاه بپیوندید:\n\n"
                f"👉 {REGISTER_LINK}"
            ),
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button_callback))

    # جلوگیری از تداخل با وبهوک
    try:
        updater.bot.delete_webhook()
    except Exception as e:
        logging.warning(f"delete_webhook failed: {e}")

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
