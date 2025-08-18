from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging
import re

# ======= تنظیمات =======
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"
REGISTER_LINK = "https://t.me/azadborojerd"
# ========================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

WELCOME_STICKER = "CAACAgUAAxkBAAIBh2J6eB9V5c3j1FvHkT6vCqk8L1pSAAJgAAOwLwABKshs9wN87LXQAQ"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! 🌸\nلطفاً نام و نام خانوادگی خود را وارد کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text.strip()
    
    if "name" not in user_data:
        user_data["name"] = text
        update.message.reply_sticker(WELCOME_STICKER)
        update.message.reply_text(f"خوش آمدی {text}! 😊\nحالا لطفاً شماره موبایل خود را وارد کنید:")
        
    elif "phone" not in user_data:
        if not re.fullmatch(r"09\d{9}", text):
            update.message.reply_text("⚠️ شماره موبایل وارد شده صحیح نیست!\n"
                                      "لطفاً شماره‌ای 11 رقمی که با 09 شروع می‌شود وارد کنید و حروف نگذارید.")
            return
        user_data["phone"] = text
        update.message.reply_text("عالی! حالا لطفاً عکس دانشجویی یا عکس انتخاب واحد خود را ارسال کنید:")
    else:
        update.message.reply_text("لطفاً عکس دانشجویی یا عکس انتخاب واحد خود را ارسال کنید:")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    try:
        photo_file = update.message.photo[-1].get_file()
        caption = f"📌 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
        
        # فوروارد به کانال
        photo_file.download("temp.jpg")
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)
        
        # دکمه ثبت نهایی با callback
        keyboard = [[InlineKeyboardButton("ثبت نهایی ✅", callback_data="register")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🎉 اطلاعات شما با موفقیت ثبت شد!\nبرای ثبت نهایی روی دکمه زیر کلیک کنید:", 
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        update.message.reply_text("❌ مشکلی پیش آمد! لطفاً دوباره امتحان کنید.")

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "register":
        # باز کردن لینک ثبت نهایی
        query.edit_message_text(f"لینک ثبت نهایی: {REGISTER_LINK}\n\n💛 از اینکه ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید، بی‌نهایت سپاسگزاریم!\nهمچنین ما را در تریبون دانشگاه آزاد بروجرد دنبال کنید.")

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
