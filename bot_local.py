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

print("Starting bot")
updater = Updater(sys.argv[1])

setup(updater)

updater.start_polling()
print("Started!")
updater.idle()
