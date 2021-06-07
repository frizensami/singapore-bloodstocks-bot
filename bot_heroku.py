#!/usr/bin/env python3
import os
from bot import setup

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

TOKEN = sys.argv[1]
PORT = int(os.environ.get("PORT", "8443"))
updater = Updater(TOKEN)

setup(updater)

# add handlers
updater.start_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url="https://sg-bloodstocks.herokuapp.com/" + TOKEN,
)
updater.idle()
