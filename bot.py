from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import re

# ======= تنظیمات =======
TOKEN = "توکن_ربات_شما_اینجا"  # توکن ربات
CHANNEL_ID = "@alialisend123"     # آیدی عددی یا یوزرنیم کانال
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎉 سلام! خوش اومدی 🌟\nلطفاً نام و نام خانوادگی خود را ارسال کن:"
    )

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # نام و نام خانوادگی
    if "name" not in user_data:
        if len(text.split()) < 2:
            update.message.reply_text("❌ لطفاً نام و نام خانوادگی خود را به صورت کامل وارد کن.")
            return
        user_data["name"] = text
        update.message.reply_text(f"👋 خوش آمدی {text}! حالا شماره موبایل خود را ارسال کن:")
        return

    # شماره موبایل
    if "phone" not in user_data:
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("❌ شماره موبایل صحیح نیست! لطفاً شماره 11 رقمی شروع با 09 وارد کن.")
            return
        user_data["phone"] = text
        update.message.reply_text(
            "📸 لطفاً عکس دانشجویی یا عکس انتخاب واحد را ارسال کن:"
        )
        return

    update.message.reply_text(
        "❗ لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید."
    )

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"

    # فوروارد به کانال
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    # دکمه ثبت نهایی
    keyboard = [[InlineKeyboardButton("ثبت نهایی ✅", url=REGISTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "✅ اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید.",
        reply_markup=reply_markup
    )

    # پیام تشکر رسمی بعد از ثبت نهایی
    update.message.reply_text(
        "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت اتومات شمارو وارد گروه خواهند کرد. "
        "ممنون که در ارائه خدمات بهتر همراه ما هستید! 🌟"
    )

    # پاک کردن داده‌ها
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
