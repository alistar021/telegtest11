from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 توکن و کانال عمومی
BOT_TOKEN = "8476998300:AAGmZpHiHEpe69PERCBnrPnhXdpV5oaEjaY"
CHANNEL_USERNAME = "@Azadborojerdbot"   # کانال عمومی

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nپیام‌هات رو بفرست، من می‌فرستم داخل کانال 📢")

# هندلر پیام‌ها
async def forward_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # ارسال به کانال
    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"📩 پیام از {user.first_name} (@{user.username}):\n\n{text}"
    )

    # جواب به کاربر
    await update.message.reply_text("✅ پیام شما به کانال ارسال شد.")

# ران کردن ربات
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_channel))

    print("🤖 ربات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
