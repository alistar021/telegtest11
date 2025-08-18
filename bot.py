from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"  # توکن ربات شما
CHANNEL_ID = "@alialisend123"  # یا آیدی عددی کانال خصوصی مثل -1001234567890
REGISTER_LINK = "https://t.me/YourFinalRegisterLink"       # لینک ثبت نهایی
# ========================

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        update.message.reply_text("لطفاً شماره موبایل خود را به صورت صحیح ارسال کنید:")
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text("لطفاً عکس دانشجویی یا عکس انتخاب واحد موجود در سایت را ارسال کنید:")
    else:
        update.message.reply_text("لطفاً عکس دانشجویی یا عکس انتخاب واحد موجود در سایت را ارسال کنید.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    photo_file = update.message.photo[-1].get_file()
    caption = f"نام: {user_data.get('name')}\nشماره: {user_data.get('phone')}"
    
    # فوروارد به کانال
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)
    
    # دکمه ثبت نهایی
    keyboard = [[InlineKeyboardButton("ثبت نهایی", url=REGISTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:\n\n"
        "تشکر از اینکه ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید. "
        "مارا در تریبون دانشگاه آزاد بروجرد دنبال کنید.",
        reply_markup=reply_markup
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
