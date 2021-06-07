#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User

"""
Storage structure for bot_data is:

{
    user_data: {
        <chat_id>:

    }
}

"""

USER_DATA = "users_data"


def check_init_storage(context: CallbackContext):
    print("Bot data:")
    print(context.bot_data)
    if context.bot_data.get(USER_DATA) is None:
        print("No bot-user data, initializing..")
        context.bot_data[USER_DATA] = {}

    print(context.user_data)
    print(context.chat_data)


def update_user_bloodtype_subscription(
    user: User, context: CallbackContext, bloodtype: str
):
    check_init_storage(context)
    user_id = user["id"]
    context.bot_data[USER_DATA][str(user_id)] = bloodtype


def get_user_bloodtype_subscription(user: User, context: CallbackContext):
    check_init_storage(context)
    user_id = user["id"]
    return context.bot_data[USER_DATA].get(str(user_id))


def delete_user_bloodtype_subscription(user: User, context: CallbackContext):
    check_init_storage(context)
    user_id = user["id"]
    return context.bot_data[USER_DATA].pop(str(user_id), None)
