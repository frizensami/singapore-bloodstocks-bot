#!/usr/bin/env python3

HELLO_MSG = """Welcome to the SG Blood Stocks Bot!

We update you on the blood stock levels of the Singapore Red Cross.

You can subscribe (/subscribe) to updates for specific blood types so you know when to donate.

You can check for the latest change (/changes) in blood stock levels over the past day.

You can check blood stock levels manually (/check).

Find out how to donate with (/donate).

Read this help message anytime with (/help).
"""

ABOUT_MSG = """SG Blood Stocks Bot Version 0.4 (Beta)

This bot retrieves blood stock data from https://www.redcross.sg/

Please report any bugs to the email found at https://sriramsami.com

Alternatively, open a bug report at https://github.com/frizensami/sgbloodstocksbot/issues"""

DONATE_MSG = """1. Check your eligibility for blood donation at https://redcross.sg/give-blood/can-i-donate-blood.html

2. Find out where you can donate at https://redcross.sg/give-blood/where-to-donate-today.html

3. Book an appointment to donate at https://donateblood.hsa.gov.sg/
"""


STATUS = ["Healthy", "Moderate", "Low", "Critical"]

UP_ARROW = "⬆️"
DOWN_ARROW = "🔻"
