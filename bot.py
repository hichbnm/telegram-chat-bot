import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = '7633719713:AAE3mDbewW9tqNp1h8ZB14PowQJKLsg-748'
OPENROUTER_API_KEY = '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'

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

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Ensure a successful response
        response_data = response.json()
        
        # Log the entire response to inspect it
        print("Response JSON:", response_data)
        
        # Check if 'choices' key exists in the response
        if 'choices' in response_data:
            reply = response_data['choices'][0]['message']['content']
        else:
            reply = "Sorry, I couldn't find an answer for you at the moment."
        
        return reply
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Sorry, there was an error with the request. Please try again later."
    except KeyError as e:
        print(f"KeyError: {e}")
        return "Sorry, something went wrong while processing the response. Please try again later."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later."

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
