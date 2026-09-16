import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = 8816958390:AAHsQfgwuVsfhizrahdwbY75bVHAJrVBKG0
GROUP_USERNAME = sahiyatracker
GROUP_LINK = https://t.me/sahiyatracker


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Join Group",
                url=GROUP_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Please join our Telegram Group first.\n"
        "After joining, click the Verify button below.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=GROUP_USERNAME,
            user_id=user_id
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                "✅ Verification Successful!\n\n"
                "You have successfully joined the group."
            )
        else:
            await query.answer(
                "❌ Please join the group first.",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "❌ Unable to verify your group membership.",
            show_alert=True
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(verify, pattern="^verify$")
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
