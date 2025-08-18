from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import re

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = -1006758587605  # آیدی عددی کانال
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎓👋 سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید تا با شما آشنا شویم:"
    )

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # مرحله اسم و فامیل
    if "name" not in user_data:
        user_data["name"] = text
        update.message.reply_text(
            f"خوش آمدی {text}!\n\n📌 ما برای امنیت، اطلاع‌رسانی و تکمیل لیست دانشجویان، این ربات را طراحی کردیم. لطفاً برای استفاده از خدمات گروه از دکمه زیر شروع کنید."
        )
        # دکمه شیشه‌ای شروع اعتبارسنجی
        keyboard = [[InlineKeyboardButton("🚀 شروع اعتبارسنجی", callback_data="start_validation")]]
        update.message.reply_text(
            "برای ادامه روی دکمه زیر بزنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # مرحله شماره موبایل
    elif "phone" not in user_data:
        # بررسی شماره موبایل
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("❌ لطفاً شماره موبایل معتبر (11 رقم و با 09 شروع شود) وارد کنید.")
            return
        user_data["phone"] = text
        update.message.reply_text("📸 لطفاً عکس دانشجویی یا عکس انتخاب واحد خود را ارسال کنید:")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data or "phone" not in user_data:
        update.message.reply_text("❗ لطفاً ابتدا نام و شماره موبایل خود را وارد کنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
    
    # فوروارد به کانال
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    # دکمه ثبت نهایی
    keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", url=REGISTER_LINK)]]
    update.message.reply_text(
        "اطلاعات شما ثبت شد! بعد از بررسی تیم فنی، شما به گروه اضافه خواهید شد. لطفاً روی دکمه زیر کلیک کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # پاک کردن داده‌ها
    user_data.clear()

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "start_validation":
        query.message.reply_text("📱 لطفاً شماره موبایل خود را وارد کنید (11 رقم و با 09 شروع شود):")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
