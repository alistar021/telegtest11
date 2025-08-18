from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import re

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"  # توکن ربات شما
CHANNEL_ID = "@alialisend123"  # آیدی کانال یا یوزرنیم
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎉 سلام! خوش آمدی 🌟\nلطفاً نام و نام خانوادگی خود را ارسال کن:"
    )

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    # نام و نام خانوادگی
    if "name" not in user_data:
        if len(text.split()) < 2:
            update.message.reply_text("❌ لطفاً نام و نام خانوادگی خود را به صورت کامل وارد کنید.")
            return
        user_data["name"] = text
        
        # پیام رسمی و دکمه شروع اعتبارسنجی
        keyboard = [[InlineKeyboardButton("🚀 شروع اعتبارسنجی", callback_data="start_verification")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            f"👋 خوش آمدید {text}!\n\n"
            "برای امنیت، اطلاع‌رسانی و تکمیل لیست اعضای گروه و جلوگیری از ورود افراد غیردانشجو، "
            "این ربات ساخته شده است. لطفاً برای استفاده از خدمات گروه از دکمه زیر شروع کنید.",
            reply_markup=reply_markup
        )
        return

    # شماره موبایل (بعد از دکمه)
    if "phone" not in user_data:
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("❌ شماره موبایل صحیح نیست! لطفاً شماره 11 رقمی شروع با 09 وارد کنید.")
            return
        user_data["phone"] = text
        update.message.reply_text("📸 لطفاً عکس دانشجویی یا عکس انتخاب واحد خود را ارسال کنید:")
        return

    update.message.reply_text("❗ لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید.")

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

    user_data.clear()

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_data = context.user_data
    if query.data == "start_verification":
        user_data.clear()
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
