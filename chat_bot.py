import os
from google import genai
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler,ContextTypes, filters

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 About the Bot", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 <b>Welcome!</b>\n\n"
        "I'm an intelligent chatbot powered by <i>Google GenAI</i>.\n"
        "You can ask me anything - from tech and science to jokes and advice.\n\n")
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query= update.callback_query
    await query.answer()

    if query.data == 'about':
        await query.edit_message_text(
            "🤖 <b>About this Bot:</b>\n\n"
            "I'm a smart chatbot built with <i>Google Gemini Pro</i> (GenAI).\n"
            "I can help you with all sorts of questions - whether it's science, coding, advice, or just fun stuff!\n\n"
            "Feel free to ask me.",
            parse_mode="HTML")
async def chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = client.models.generate_content(
            model= "gemini-2.5-flash",
            contents=user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatbot))

app.run_polling()