import os
import sys
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8816958390:AAHDcNT8zJqMgeDDexHIZikAa9Dud4P8oSE" 
GROUP_USERNAME = "@sahiyatracker"
GROUP_LINK = "https://t.me/sahiyatracker"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")],
    ]
    await update.message.reply_text(
        "👋 Welcome to Sahiya Tracker!\n\n"
        "Please join our Telegram Group first.\n"
        "Then click the Verify button below.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=GROUP_USERNAME,
            user_id=user_id,
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                "✅ Verification Successful!\n\n"
                "You have successfully joined the Sahiya Tracker Group."
            )
        else:
            await query.answer(
                "❌ Please join the Group first.",
                show_alert=True,
            )

    except Exception as e:
        logger.error(f"Verification check failed: {e}")
        await query.answer(
            "❌ Unable to check your group membership. Make sure the bot is an admin in the group.",
            show_alert=True,
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
