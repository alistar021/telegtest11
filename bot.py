from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"
CHANNEL_ID = "@alialisend123"  # کانال عمومی

# مرحله‌ای برای ذخیره وضعیت کاربر
user_state = {}
user_data = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_state[chat_id] = "WAIT_NAME"
    user_data[chat_id] = {}
    context.bot.send_message(chat_id=chat_id, text="سلام! لطفا نام خود را وارد کنید.")

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_state:
        context.bot.send_message(chat_id=chat_id, text="لطفا ابتدا /start را بزنید.")
        return

    # مرحله دریافت نام
    if user_state[chat_id] == "WAIT_NAME":
        user_data[chat_id]['name'] = text
        user_state[chat_id] = "WAIT_PHONE"
        context.bot.send_message(chat_id=chat_id, text="شماره خود را وارد کنید.")
        return

    # مرحله دریافت شماره
    if user_state[chat_id] == "WAIT_PHONE":
        user_data[chat_id]['phone'] = text
        user_state[chat_id] = "WAIT_PHOTO"
        context.bot.send_message(chat_id=chat_id, text="لطفا عکس خود را ارسال کنید.")
        return

def handle_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in user_state or user_state[chat_id] != "WAIT_PHOTO":
        context.bot.send_message(chat_id=chat_id, text="لطفا ابتدا /start را بزنید.")
        return

    photo_file = update.message.photo[-1].get_file()
    context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo_file.file_id,
        caption=f"📌 نام: {user_data[chat_id]['name']}\n📱 شماره: {user_data[chat_id]['phone']}"
    )

    context.bot.send_message(chat_id=chat_id, text="اطلاعات شما ثبت شد.")
    # پاک کردن داده‌ها بعد از ارسال
    del user_state[chat_id]
    del user_data[chat_id]

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
