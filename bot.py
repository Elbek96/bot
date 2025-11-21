from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ⚠️ YANGI TOKENNI SHU YERGA QO'YING ( eski tokenni ishlatmang! )
TOKEN = "8590694654:AAGAJ7w8ZxbejP48qCn8VVCqX6UqkUVw6Co"

# ✔ Sizning kanal username'ingiz
CHANNEL_ID = "@video_rolik_ku"

# ✔ Tanlov mavzulari
TOPICS = [
    "Mening universitetim",
    "Mening ustozim",
    "Mening mahallam",
    "Mening ota-onam – mening faxrim",
    "Ixtiyoriy mavzu"
]

# Foydalanuvchi vaqtinchalik ma'lumotlari
user_data = {}

# START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 *Videoroliklar tanloviga xush kelibsiz!*\n\n"
        "Iltimos, avval VIDEO yuboring 📹.",
        parse_mode="Markdown"
    )

# 1) VIDEO QABUL QILISH
async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    video = update.message.video

    user_data[user_id] = {"video_id": video.file_id}

    await update.message.reply_text(
        "📌 Video qabul qilindi!\nEndi *Ism Familiya* yuboring.",
        parse_mode="Markdown"
    )

# 2) MATN QABUL QILISH (Ism → Guruh → Mavzu)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text

    if user_id not in user_data:
        return await update.message.reply_text("Avval video yuboring.")

    # 2.1 — Ism familiya
    if "name" not in user_data[user_id]:
        user_data[user_id]["name"] = text
        return await update.message.reply_text(
            "📚 Endi guruh yoki yo'nalishingizni yuboring.",
            parse_mode="Markdown"
        )

    # 2.2 — Guruh
    if "group" not in user_data[user_id]:
        user_data[user_id]["group"] = text

        # Mavzular tugma holatida chiqadi
        keyboard = ReplyKeyboardMarkup([[t] for t in TOPICS], resize_keyboard=True, one_time_keyboard=True)

        return await update.message.reply_text(
            "📌 Tanlov mavzusini tanlang:",
            reply_markup=keyboard
        )

    # 2.3 — Mavzu tanlandi → yakunimiz
    if "topic" not in user_data[user_id]:
        user_data[user_id]["topic"] = text

        name = user_data[user_id]["name"]
        group = user_data[user_id]["group"]
        topic = user_data[user_id]["topic"]
        video_id = user_data[user_id]["video_id"]

        caption = (
            "🎬 *Kokand University Videoroliklar Tanlovi*\n"
            f"👤 *Ism:* {name}\n"
            f"📚 *Guruh:* {group}\n"
            f"📌 *Mavzu:* {topic}"
        )

        # 🔥 FAQAT KANALGA YUBORILADI
        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=video_id,
            caption=caption,
            parse_mode="Markdown"
        )

        await update.message.reply_text("✅ Videongiz qabul qilindi! Omad tilaymiz!")

        del user_data[user_id]  # Foydalanuvchi maʼlumotlarini tozalaymiz

# Asosiy ishga tushirish
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
