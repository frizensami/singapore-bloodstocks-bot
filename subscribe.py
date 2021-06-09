#!/usr/bin/env python3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from storage import *
import telegram

SUBSCRIBE_TEXT = """Please choose a blood type to receive alerts about its stock level.

Alternatively, you may choose to receive updates for *any* changes in blood stock levels.

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
        [InlineKeyboardButton("Any Changes", callback_data="any")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bloodtype = get_user_bloodtype_subscription(update.message.from_user, context)
    final_msg = SUBSCRIBE_TEXT
    if bloodtype is not None:
        if len(bloodtype) == 1:
            if bloodtype[0] == "any":
                final_msg += (
                    f"\nYou are currently subscribed to *any* blood stock changes."
                )
            else:
                final_msg += (
                    f"\nYou are currently subscribed to blood type *{bloodtype[0]}*."
                )
        else:
            final_msg += f"\nYou are currently subscribed to blood types *{', '.join(bloodtype)}*."
    update.message.reply_text(
        final_msg,
        reply_markup=reply_markup,
        parse_mode=telegram.constants.PARSEMODE_MARKDOWN,
    )


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

    if query.data != "any":
        query.edit_message_text(
            text=f"Subscribed to updates for blood type *{query.data}*",
            parse_mode=telegram.constants.PARSEMODE_MARKDOWN,
        )
    else:
        query.edit_message_text(
            text=f"Subscribed to *any* updates about blood stock changes.",
            parse_mode=telegram.constants.PARSEMODE_MARKDOWN,
        )
