from telegram import Update
from telegram.ext import CallbackContext

import json

MESSAGE = []
CUSTOM_MESSAGES_DICT = {}
CUSTOM_MESSAGES_FILENAME = ""


def set_message(update: Update, context: CallbackContext) -> None:
    """Change alarm message to be sent"""
    new_message = " ".join(context.args)
    MESSAGE[0] = new_message
    text = f"Message set to \"{new_message}\""
    update.message.reply_text(text)


def delete_custom_message(update: Update, context: CallbackContext):
    pass


def view_custom_message(update: Update, context: CallbackContext):
    """View custom messages"""
    user_id = update.message.from_user.id
    output_text = ""
    if user_id in CUSTOM_MESSAGES_DICT:
        for message in CUSTOM_MESSAGES_DICT[user_id]:
            counter = 1
            output_text += f"{counter}. {message}\n"
    update.message.reply_text(output_text)


def add_custom_message(update: Update, context: CallbackContext):
    """Add custom messages to alarm"""
    new_message = " ".join(context.args)
    user_id = update.message.from_user.id

    if user_id in CUSTOM_MESSAGES_DICT:
        CUSTOM_MESSAGES_DICT[user_id].append(new_message)
    else:
        CUSTOM_MESSAGES_DICT[user_id] = [new_message]

    with open(CUSTOM_MESSAGES_FILENAME) as file:
        file.write(json.dumps(CUSTOM_MESSAGES_DICT, indent=4))