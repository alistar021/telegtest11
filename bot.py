import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# دریافت توکن ربات و نام کانال از Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # مثال: @alialisend123

if not BOT_TOKEN or not CHANNEL_USERNAME:
    raise ValueError("لطفاً BOT_TOKEN و CHANNEL_USERNAME را در Environment Variables تعریف کنید!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # پیام خوش آمد
    await update.message.reply_text(f"سلام {user.first_name}! پیام شما دریافت شد.")
    
    # ارسال اطلاعات کاربر به کانال
    message = f"کاربر جدید:\nاسم: {user.first_name}\nآیدی: {user.id}\nیوزرنیم: @{user.username if user.username else 'ندارد'}"
    await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    app.add_handler(start_handler)
    
    print("Bot is running...")
    app.run_polling()
