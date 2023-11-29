import requests
import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TELEGRAM_TOKEN, API_KEY, BASE_URL
from waitress import serve

# Function to generate text using Mancer API
def generate_text(prompt, model_id="mytholite"):
    url = f"{BASE_URL}/webui/{model_id}/api/v1/generate"

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY,
    }

    data = {
        "prompt": prompt,
        "max_new_tokens": 80,
        "min_tokens": 0,
        "stopping_strings": [],
        "ban_eos_token": False,
        "temperature": 0.5,
        "repetition_penalty": 1.6,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_k": 0,
        "top_p": 0.9,
        "top_a": 0,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    try:
        response.raise_for_status()
        result = response.json()
        text_result = result["results"][0]["text"]
        return text_result
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your assistant. Type something.')

def handle_message(update: Update, context: CallbackContext) -> None:
    with open("assistant_prompt.txt", "r", encoding="utf-8") as file:
        assistant_prompt = file.read()

    with open("conversation.txt", "r", encoding="utf-8") as file:
        conversation = file.read()

    with open("instruct.txt", "r", encoding="utf-8") as file:
        instruct = file.read()

    user_input = update.message.text
    conversation += f"\nRay: {user_input}\n"

    bot_response = generate_text(f"{assistant_prompt}\n{conversation}\n{instruct}\n")

    if bot_response:
        update.message.reply_text(bot_response)
        conversation += f"{bot_response}\n"

        with open("conversation.txt", "w", encoding="utf-8") as file:
            file.write(conversation)
            file.flush()
    else:
        update.message.reply_text("I'm sorry, but I couldn't generate a response.")

TOKEN = TELEGRAM_TOKEN

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    if __name__ == '__main__':
        serve(updater.bot, host="0.0.0.0", port=8443)

if __name__ == '__main__':
    main()
