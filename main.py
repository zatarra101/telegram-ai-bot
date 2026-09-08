import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI assistant. Send me a message to get started!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": user_text}]
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logging.error(f"Error calling API: {e}")
        await update.message.reply_text("Sorry, I encountered an error generating a response.")

if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN or not OPENROUTER_API_KEY:
        print("Missing required environment variables!")
        exit(1)
        
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    app.run_polling()
