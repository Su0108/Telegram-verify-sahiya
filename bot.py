from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

GROUP_ID = "@sahiyatracker"

async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_member = await check_membership(user_id, context)

    if not is_member:
        keyboard = [
            [InlineKeyboardButton("Join Group", url="https://t.me/sahiyatracker")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ]
        await update.message.reply_text(
            "You must join our group before using this bot.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("Welcome! The bot is ready to use.")

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if await check_membership(user_id, context):
        await query.answer()
        await query.message.reply_text("Membership confirmed ✅ You can now use the bot.")
    else:
        await query.answer("You haven't joined the group yet!", show_alert=True)

app = Application.builder().token("8816958390:AAHDcNT8zJqMgeDDexHIZikAa9Dud4P8oSE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
app.run_polling()
