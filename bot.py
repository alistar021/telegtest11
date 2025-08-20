from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- توکن ربات و یوزرنیم کانال عمومی ---
TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"
CHANNEL_ID = "@alialisend123"  # کانال عمومی

# --- دیتاست کاربر ---
user_data = {}

# --- دستور /start ---
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="سلام! به ربات خوش آمدید.\nلطفا نام و نام خانوادگی خود را ارسال کنید."
    )
    user_data[chat_id] = {}

# --- دریافت نام ---
def get_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in user_data and 'name' not in user_data[chat_id]:
        user_data[chat_id]['name'] = update.message.text
        context.bot.send_message(chat_id=chat_id, text="لطفا شماره موبایل خود را وارد کنید.")

# --- دریافت شماره موبایل ---
def get_phone(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in user_data and 'name' in user_data[chat_id] and 'phone' not in user_data[chat_id]:
        user_data[chat_id]['phone'] = update.message.text
        context.bot.send_message(chat_id=chat_id, text="لطفا عکس انتخاب واحد خود را ارسال کنید.")

# --- دریافت عکس ---
def get_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in user_data and 'name' in user_data[chat_id] and 'phone' in user_data[chat_id]:
        file_id = update.message.photo[-1].file_id
        user_data[chat_id]['photo'] = file_id

        # ارسال اطلاعات به کانال عمومی
        context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=(
                f"📌 نام: {user_data[chat_id]['name']}\n"
                f"📱 شماره: {user_data[chat_id]['phone']}\n"
                f"🖼️ عکس انتخاب واحد: {file_id}"
            )
        )

        # پیام تایید به کاربر
        context.bot.send_message(chat_id=chat_id, text="با تشکر! اطلاعات شما ثبت شد.")

        # پاک کردن داده کاربر
        del user_data[chat_id]

# --- اجرای ربات ---
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # هندلرها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_name))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_phone))
    dispatcher.add_handler(MessageHandler(Filters.photo, get_photo))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
