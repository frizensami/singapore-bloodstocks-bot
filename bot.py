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

HELLO_MSG = """Welcome to the SG Blood Stocks Bot!

We update you on the blood stock levels of the Singapore Red Cross.

You can also subscribe to updates for specific blood types so you know when to donate (IN PROGRESS).

You can use the /check command to check stocks manually."""

STOCKS_STR = None

# 30 min
UPDATE_INTERVAL_SECS = 30 * 60


def update_stocks():
    global STOCKS_STR

    current_stocks = get_bloodstocks()
    stock_str = "*All Blood Levels*\n```\n"
    for k in current_stocks:
        pad = (3 if len(k) == 3 else 4) * " "
        stock_str += f"{k}{pad}{current_stocks[k]}\n"
    stock_str += "```\n"

    stock_str += "*Moderate*\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k] == "Moderate":
            has_condition = True
            pad = (3 if len(k) == 3 else 4) * " "
            stock_str += f"{k}{pad}{current_stocks[k]}\n"
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    stock_str += "*Low*\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k] == "Low":
            has_condition = True
            pad = (3 if len(k) == 3 else 4) * " "
            stock_str += f"{k}{pad}{current_stocks[k]}\n"
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    stock_str += "*Critical*\n```\n"
    has_condition = False
    for k in current_stocks:
        if current_stocks[k] == "Critical":
            has_condition = True
            pad = (3 if len(k) == 3 else 4) * " "
            stock_str += f"{k}{pad}{current_stocks[k]}\n"
    if not has_condition:
        stock_str += "None\n"
    stock_str += "```\n"

    STOCKS_STR = stock_str


def update_stocks_interval(context: CallbackContext):
    print("Updating stocks at interval")
    update_stocks()


def hello(update: Update, context: CallbackContext) -> None:
    print("Received message: /start")
    update.message.reply_text(HELLO_MSG)
    update.message.reply_text(
        STOCKS_STR, parse_mode=telegram.constants.PARSEMODE_MARKDOWN
    )


def check(update: Update, context: CallbackContext) -> None:
    print("Received message: /check")
    update.message.reply_text(
        STOCKS_STR, parse_mode=telegram.constants.PARSEMODE_MARKDOWN
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def setup(updater):
    update_stocks()
    j = updater.job_queue
    job_minute = j.run_repeating(update_stocks_interval, interval=UPDATE_INTERVAL_SECS)

    # Handle initial start message
    updater.dispatcher.add_handler(CommandHandler("start", hello))
    updater.dispatcher.add_handler(CommandHandler("check", check))

    # Handle unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    updater.dispatcher.add_handler(unknown_handler)
