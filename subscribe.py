#!/usr/bin/env python3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from storage import *

SUBSCRIBE_TEXT = """Please choose your blood type to receive alerts about its stock level.
"""


def subscribe_c(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("A+", callback_data="A+"),
            InlineKeyboardButton("B+", callback_data="B+"),
            InlineKeyboardButton("O+", callback_data="O+"),
            InlineKeyboardButton("AB+", callback_data="AB+"),
        ],
        [
            InlineKeyboardButton("A-", callback_data="A-"),
            InlineKeyboardButton("B-", callback_data="B-"),
            InlineKeyboardButton("O-", callback_data="O-"),
            InlineKeyboardButton("AB-", callback_data="AB-"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bloodtype = get_user_bloodtype_subscription(update.message.from_user, context)
    final_msg = SUBSCRIBE_TEXT
    if bloodtype is not None:
        final_msg += f"\nYou are currently subscribed to blood type {bloodtype}."
    update.message.reply_text(final_msg, reply_markup=reply_markup)


def unsubscribe_c(update: Update, context: CallbackContext) -> None:
    delete_user_bloodtype_subscription(update.message.from_user, context)
    update.message.reply_text("Unsubscribed from blood stock updates.")


def subscribe_cb(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # Update the bot data
    update_user_bloodtype_subscription(query.from_user, context, query.data)

    query.edit_message_text(text=f"Subscribed to updates for blood type {query.data}!")
