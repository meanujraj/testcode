import os
import requests
from telegram import ParseMode, Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define an empty dictionary to store the data
data = {}

# Define the bot token and server URL from environment variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SERVER_URL = os.environ.get("SERVER_URL")

# Define the bot and updater objects
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message = "Welcome to my Telegram bot! Please enter your name:"
    context.bot.send_message(chat_id=chat_id, text=message)

# Define the message handler for each data field
def store_name(update: Update, context: CallbackContext) -> None:
    name = update.message.text
    data["name"] = name
    message = "Thanks! Please enter your date of birth (DD/MM/YYYY):"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_dob(update: Update, context: CallbackContext) -> None:
    dob = update.message.text
    data["dob"] = dob
    message = "Got it! Please enter your address:"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_address(update: Update, context: CallbackContext) -> None:
    address = update.message.text
    data["address"] = address
    message = "Great! Please enter your email address:"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_email(update: Update, context: CallbackContext) -> None:
    email = update.message.text
    data["email"] = email
    message = "Awesome! Please enter your phone number:"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_phone(update: Update, context: CallbackContext) -> None:
    phone = update.message.text
    data["phone"] = phone
    message = "Almost done! Please enter the URL of your photo:"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_photo(update: Update, context: CallbackContext) -> None:
    photo_url = update.message.text
    # Download the photo from the URL and store it on the Render server
    response = requests.get(photo_url)
    filename = f"{data['name']}.jpg"
    with open(filename, "wb") as f:
        f.write(response.content)
    # Store the photo filename in the data dictionary
    data["photo"] = filename
    message = "Nice! Finally, please enter your hobby:"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def store_hobby(update: Update, context: CallbackContext) -> None:
    hobby = update.message.text
    data["hobby"] = hobby
    # Store the data dictionary on the Render server
    response = requests.post(SERVER_URL, json=data)
    if response.status_code == 200:
        message = "Data stored successfully!"
    else:
        message = "Oops! Something went wrong while storing your data. Please try again later."
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

#
