import os
from dotenv import load_dotenv
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
load_dotenv()  # Load environment variables from .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def start(update, context):
    update.message.reply_text("Hi! Ask me anything 🤖")

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # or try others
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    reply = response.json()['choices'][0]['message']['content']
    return reply

def handle_message(update, context):
    user_input = update.message.text
    reply = ask_openrouter(user_input)
    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
