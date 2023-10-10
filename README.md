# Singapore Blood Stocks Telegram Bot (Unofficial)

Telegram bot that informs users of Singapore's blood stocks levels from https://www.redcross.sg. 

Bot is live at http://t.me/sgbloodstocksbot or @sgbloodstocksbot.

*Disclaimer*: This is an unofficial data source: I do not know for sure if these are the exact numbers, but I strongly believe that they are via some educated guesses. Regardless, this information comes without any warranty or guarantees of any sort.

## Features
- `/check` current blood stocks level
- `/subscribe` to updates on blood stocks changes for either a specific blood type, or for any changes at all.
- `/changes` shows the blood stock changes since the previous day
- `/about`, `/help`, `/unsubscribe` work as expected

## Stack
- Hosted on a $5/mo DigitalOcean instance, with a free Firebase Realtime Database as the backend.
- `BeautifulSoup` to get updates from the Red Cross website, `python-telegram-bot` for the bot itself

## Running the bot
- Clone the repo
- Install libraries with `pip install -r requirements.txt`
- Get a Firebase `.json` private key file and the URL for your Firebase database. Save it as `firebase.json`.
- Before running the bot, add at least `{'bot_data': {'users_data': {'1111': {'blood_subscription': 'all'}}}}` to the Firebase database through the web UI. This minimal seeding is necessary so that the persistence layer doesn't complain.
- Then, run the bot with `FIREBASE_URL="YOUR URL HERE" FIREBASE_CREDENTIALS=$(< firebase.json) python3 bot_local.py "TELEGRAM BOT API KEY"`
