#!/usr/bin/env python3
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
import telegram
import sys
from scraper import get_bloodstocks
from strings import HELLO_MSG, ABOUT_MSG

STOCKS_STR = None

# 30 min
UPDATE_INTERVAL_SECS = 30 * 60


def get_stock_str(current_stocks, key):
    pad = (3 if len(key) == 3 else 4) * " "
    stock_str = f"{key}{pad}{current_stocks[key]['status']} ({current_stocks[key]['fill_level']}%)\n"
    return stock_str


def update_stocks():
    global STOCKS_STR

    current_stocks = get_bloodstocks()
    stock_str = "*All Blood Levels*\n```\n"
    for k in current_stocks:
        stock_str += get_stock_str(current_stocks, k)
    stock_str += "```\n"

    stock_str += "*Moderate* ⚠️\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k]["status"] == "Moderate":
            has_condition = True
            stock_str += get_stock_str(current_stocks, k)
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    stock_str += "*Low* ❗\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k]["status"] == "Low":
            has_condition = True
            stock_str += get_stock_str(current_stocks, k)
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    stock_str += "*Critical* ‼️\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k]["status"] == "Critical":
            has_condition = True
            stock_str += get_stock_str(current_stocks, k)
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    STOCKS_STR = stock_str


def update_stocks_interval(context: CallbackContext):
    print("Updating stocks at interval")
    update_stocks()


def hello(update: Update, context: CallbackContext) -> None:
    """
    /start command, send hello message and then the check string
    """
    print(
        f"Received message: /start from chat id {update.message.chat_id} ({update.message.chat.first_name} {update.message.chat.last_name})"
    )
    update.message.reply_text(HELLO_MSG)
    check(update, context)


def helpc(update: Update, context: CallbackContext) -> None:
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
        f"Update caused error {context.error} from ({update.message.chat.first_name} {update.message.chat.last_name}) \n\nUpdate: {update}"
    )


def setup(token):
    updater = Updater(token)

    update_stocks()
    j = updater.job_queue
    job_minute = j.run_repeating(update_stocks_interval, interval=UPDATE_INTERVAL_SECS)

    # Handle initial start message
    updater.dispatcher.add_handler(CommandHandler("start", hello))
    updater.dispatcher.add_handler(CommandHandler("check", check))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("help", helpc))

    # Handle unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    updater.dispatcher.add_handler(unknown_handler)

    # Error handling
    updater.dispatcher.add_error_handler(error_callback)

    return updater
