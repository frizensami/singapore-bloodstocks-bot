#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User

"""
Storage structure for bot_data is:

{
    user_data: {
        <user_id>:

    }
}

"""

USER_DATA = "users_data"
USER_BLOOD_SUBSCRIPTION = "blood_subscription"


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
    if context.bot_data[USER_DATA].get(user_id) is None:
        context.bot_data[USER_DATA][user_id] = {USER_BLOOD_SUBSCRIPTION: [bloodtype]}
    else:
        context.bot_data[USER_DATA][user_id][USER_BLOOD_SUBSCRIPTION] = [bloodtype]


def get_user_bloodtype_subscription(user: User, context: CallbackContext):
    check_init_storage(context)
    user_id = str(user["id"])

    user_data = context.bot_data[USER_DATA].get(user_id)
    if user_data == None:
        return None
    else:
        return user_data.get(USER_BLOOD_SUBSCRIPTION)


def delete_user_bloodtype_subscription(user: User, context: CallbackContext):
    check_init_storage(context)
    user_id = str(user["id"])
    return context.bot_data[USER_DATA].pop(user_id, None)
