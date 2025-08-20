from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"
CHANNEL_USERNAME = "@alialisend123"

# هندلر برای دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام شما دریافت شد ✅")
    # ارسال پیام کاربر به کانال
    try:
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, 
                                       text=f"پیام جدید از کاربر: {update.message.text}")
    except Exception as e:
        print("ارسال به کانال ناموفق:", e)

# هندلر برای تمام پیام‌ها
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("پیام شما دریافت شد ✅")
    try:
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, 
                                       text=f"پیام جدید از کاربر: {update.message.text}")
    except Exception as e:
        print("ارسال به کانال ناموفق:", e)

# ساخت اپلیکیشن و اضافه کردن هندلرها
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# اجرای ربات
print("ربات در حال اجراست...")
app.run_polling()
