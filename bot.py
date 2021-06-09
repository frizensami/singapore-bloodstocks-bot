#!/usr/bin/env python3
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
import telegram
import sys
from datetime import datetime
import pytz

# Us
from scraper import get_bloodstocks
from strings import HELLO_MSG, ABOUT_MSG
from subscribe import subscribe_c, subscribe_cb, unsubscribe_c
from firebase_persistence import FirebasePersistence
from stocks import (
    format_stocks,
    get_stock_diffs,
    diffs_to_str,
    diffs_with_bloodtype_to_str,
)
from storage import *

# 30 min
UPDATE_INTERVAL_SECS = 20 * 60

# Already formatted string to pass to /check
STOCKS_STR = None
# Stocks retrieved from previous pass
OLD_STOCKS = None

# Current stocks
CURRENT_STOCKS = None

# Test: first message from bot should be an auto update if we are subscribed appropriately
"""
Original
{'A+': {'fill_level': '100', 'status': 'Healthy'},
 'A-': {'fill_level': '69', 'status': 'Healthy'},
 'AB+': {'fill_level': '100', 'status': 'Healthy'},
 'AB-': {'fill_level': '40', 'status': 'Low'},
 'B+': {'fill_level': '100', 'status': 'Healthy'},
 'B-': {'fill_level': '66', 'status': 'Healthy'},
 'O+': {'fill_level': '100', 'status': 'Healthy'},
 'O-': {'fill_level': '51', 'status': 'Moderate'}}

"""
# CURRENT_STOCKS_TEST = {
#     "A+": {"fill_level": "90", "status": "Healthy"},  # Lower fill, same state
#     "A-": {"fill_level": "69", "status": "Healthy"},
#     "AB+": {"fill_level": "100", "status": "Healthy"},
#     "AB-": {"fill_level": "20", "status": "Critical"},  # Lower fill, different state
#     "B+": {"fill_level": "100", "status": "Healthy"},
#     "B-": {"fill_level": "67", "status": "Healthy"},  # Higher fill, same state
#     "O+": {"fill_level": "100", "status": "Healthy"},
#     "O-": {"fill_level": "70", "status": "Healthy"},  # Higher fill, different state
# }
# CURRENT_STOCKS = CURRENT_STOCKS_TEST

# Last updated time
LAST_BOT_UPDATE_TIME = None
LAST_REDCROSS_UPDATE_TIME = None

# Diffs
CURRENT_DIFF = None
CURRENT_DIFF_STR = None

# Datetime
TIMEZONE = pytz.timezone("Asia/China")


def update_stocks(context: CallbackContext):
    global STOCKS_STR
    global OLD_STOCKS
    global CURRENT_STOCKS
    global LAST_BOT_UPDATE_TIME
    global LAST_REDCROSS_UPDATE_TIME
    global CURRENT_DIFF
    global CURRENT_DIFF_STR

    # Replace old stocks
    OLD_STOCKS = CURRENT_STOCKS

    # Update new stocks
    new_stocks = get_bloodstocks()
    CURRENT_STOCKS = new_stocks

    # Update our last update time
    current_time = pytz.utc.localize(datetime.utcnow()).astimezone(TIMEZONE)
    LAST_BOT_UPDATE_TIME = current_time

    # Format /check string
    stock_str = format_stocks(new_stocks, current_time)
    STOCKS_STR = stock_str

    # Check diffs between old and current stocks
    if OLD_STOCKS is not None and CURRENT_STOCKS is not None:
        diffs = get_stock_diffs(CURRENT_STOCKS, OLD_STOCKS)

        if diffs:
            # Update globals
            CURRENT_DIFF = diffs
            LAST_REDCROSS_UPDATE_TIME = current_time
            # Get a generic diffs string to send to all the alldiffs subscribers
            diffs_str = diffs_to_str(diffs, LAST_REDCROSS_UPDATE_TIME)
            CURRENT_DIFF_STR = diffs_str
            print(diffs_str)
            # Update all "any"-blood stock subscribers
            update_any_subscribers(context, diffs_str)
            # Update type-by-tye
            for key in diffs:
                update_subscribers_for_bloodtype(context, diffs, key)


def update_any_subscribers(context: CallbackContext, diffs_str):
    """
    For subscribers that want the "any" subscription, send them the diff string
    """
    users = get_all_users(context)
    for user in users:
        if is_user_any_blood_subscription(context, user):
            context.bot.send_message(
                chat_id=int(user),
                text=diffs_str,
                parse_mode=telegram.constants.PARSEMODE_MARKDOWN,
            )


def update_subscribers_for_bloodtype(context: CallbackContext, diffs, bloodtype: str):
    """
    For specific updates on specific bloodtypes.
    Don't send them this update if they are already subscribed to "any"
    """
    diffs_str = diffs_with_bloodtype_to_str(diffs, bloodtype, LAST_REDCROSS_UPDATE_TIME)
    users = get_all_users(context)
    for user in users:
        if is_user_blood_subscription(
            context, user, bloodtype
        ) and not is_user_any_blood_subscription(context, user):
            context.bot.send_message(
                chat_id=int(user),
                text=diffs_str,
                parse_mode=telegram.constants.PARSEMODE_MARKDOWN,
            )


def update_stocks_interval(context: CallbackContext):
    print("Updating stocks at interval")
    update_stocks(context)


def hello(update: Update, context: CallbackContext) -> None:
    """
    /start command, send hello message and then the check string
    """
    print(
        f"Received message: /start from chat id {update.message.chat_id} ({update.message.chat.first_name} {update.message.chat.last_name})"
    )
    update.message.reply_text(HELLO_MSG)
    check(update, context)


def help_c(update: Update, context: CallbackContext) -> None:
    """
    /help command, /start without the blood bank info
    """
    print(
        f"Received message: /help from chat id {update.message.chat_id} ({update.message.chat.first_name} {update.message.chat.last_name})"
    )
    update.message.reply_text(HELLO_MSG)


def check(update: Update, context: CallbackContext) -> None:
    """
    /check command, send blood stock string
    """
    print(
        f"Received or processing code for: /check from chat id {update.message.chat_id} ({update.message.chat.first_name} {update.message.chat.last_name})"
    )
    update.message.reply_text(
        STOCKS_STR, parse_mode=telegram.constants.PARSEMODE_MARKDOWN
    )


def about(update: Update, context: CallbackContext) -> None:
    """
    /about command, send info message
    """
    print(
        f"Received message: /about from chat id {update.message.chat_id} ({update.message.chat.first_name} {update.message.chat.last_name})"
    )
    update.message.reply_text(
        ABOUT_MSG, parse_mode=telegram.constants.PARSEMODE_MARKDOWN
    )


def unknown(update, context):
    print(
        f"Received unknown command: {update.message.text} from chat id {update.message.chat_id}"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def error_callback(update, context):
    print(
        f"\n!!!!!!!! Update caused error: [[ {context.error} ]] \nFrom Update: {update}\n"
    )


def setup(token):
    my_persistence = FirebasePersistence.from_environment(
        store_user_data=False,
        store_chat_data=False,
        store_bot_data=True,
    )
    updater = Updater(
        token,
        persistence=my_persistence,
        use_context=True,
    )

    # update_stocks()
    j = updater.job_queue
    job_minute = j.run_repeating(
        update_stocks_interval, interval=UPDATE_INTERVAL_SECS, first=1
    )

    # Handle initial start message
    updater.dispatcher.add_handler(CommandHandler("start", hello))
    updater.dispatcher.add_handler(CommandHandler("check", check))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("help", help_c))
    updater.dispatcher.add_handler(CommandHandler("subscribe", subscribe_c))
    updater.dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe_c))
    updater.dispatcher.add_handler(CallbackQueryHandler(subscribe_cb))

    # Handle unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    updater.dispatcher.add_handler(unknown_handler)

    # Error handling
    updater.dispatcher.add_error_handler(error_callback)

    return updater
