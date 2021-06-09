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
CURRENT_DIFF = "current_diff"


def check_init_storage(context: CallbackContext):
    # print("Bot data:")
    # print(context.bot_data)
    if context.bot_data.get(USER_DATA) is None:
        print("No bot-user data, initializing..")
        context.bot_data[USER_DATA] = {}

    # print(context.user_data)
    # print(context.chat_data)


def update_user_bloodtype_subscription(
    user: User, context: CallbackContext, bloodtype: str
):
    """
    Stores the user blood type subscription as a list in the bot-user dict.
    """
    check_init_storage(context)
    user_id = str(user["id"])
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


def get_all_users(context: CallbackContext):
    check_init_storage(context)
    return context.bot_data[USER_DATA].keys()


def is_user_any_blood_subscription(context: CallbackContext, user_id: str):
    return is_user_blood_subscription(context, user_id, "any")


def is_user_blood_subscription(context: CallbackContext, user_id: str, bloodtype: str):
    check_init_storage(context)
    subscription = (
        context.bot_data[USER_DATA]
        .get(str(user_id), {})
        .get(USER_BLOOD_SUBSCRIPTION, None)
    )
    return bloodtype in subscription


def update_current_diff(context: CallbackContext, diff, diffstr, difftime):
    check_init_storage(context)
    context.bot_data[USER_DATA][CURRENT_DIFF] = {
        "diff": diff,
        "diff_string": diffstr,
        "difftime": difftime,
    }


def get_current_diff(context: CallbackContext, diff, diffstr, difftime):
    check_init_storage(context)
    return context.bot_data[USER_DATA].get(CURRENT_DIFF)
