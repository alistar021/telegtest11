def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data

    if "phone" not in user_data:
        update.message.reply_text("❗ ابتدا شماره موبایل را وارد کنید، سپس عکس ارسال کنید.")
        return

    # دریافت عکس
    photo_file = update.message.photo[-1].get_file()
    caption = f"👤 نام: {user_data.get('name')}\n📱 شماره: {user_data.get('phone')}"
    photo_file.download("temp.jpg")

    try:
        # ارسال به کانال
        context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=open("temp.jpg", "rb"),
            caption=caption
        )

        # دکمه ثبت نهایی
        keyboard = [[InlineKeyboardButton("ثبت نهایی ✅", url=REGISTER_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "✅ اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:",
            reply_markup=reply_markup
        )

        update.message.reply_text(
            "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت اتومات شما را وارد گروه خواهند کرد. "
            "ممنون از همراهی شما 🌟"
        )

        # 🧹 پاک‌کردن اطلاعات کاربر
        user_data.clear()

    except Exception as e:
        update.message.reply_text("⚠️ مشکلی در ارسال اطلاعات به کانال پیش آمد. لطفاً دوباره تلاش کنید.")
        logging.error(f"Error sending to channel: {e}")
