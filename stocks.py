#!/usr/bin/env python3
from scraper import get_bloodstocks
from strings import *

STATUS_CHANGE = "status_change"
FILL_CHANGE = "fill_change"


def get_stock_str(current_stocks, key):
    pad = (3 if len(key) == 3 else 4) * " "
    stock_str = f"{key}{pad}{current_stocks[key]['status']} ({current_stocks[key]['fill_level']}%)\n"
    return stock_str


def format_stocks(current_stocks, current_time):
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

    stock_str += f"\n*Disclaimer*: This is not an official source of data.\n""
    # stock_str += f"*Last Checked*: {current_time.strftime('%-d %B %Y %H:%M')}\n"
    # stock_str += (
    #     f"*Last Red Cross Update*: {last_update_time.strftime('%-d %B %Y %H:%M')}\n"
    # )
    return stock_str


def get_stock_diffs(current, old):
    """
    Find all the differences between the current and old stock levels so that we can update subscribers.
    """
    if current is None or old is None:
        return None

    diffs = {}
    for key in current:
        if key not in old:
            continue  # Defensive in case of updates
        current_status = current[key]["status"]
        old_status = old[key]["status"]
        current_fill = current[key]["fill_level"]
        old_fill = old[key]["fill_level"]

        if current_status != old_status or current_fill != old_fill:
            diffs[key] = {}
        if current_status != old_status:
            diffs[key][STATUS_CHANGE] = [old_status, current_status]
        if current_fill != old_fill:
            diffs[key][FILL_CHANGE] = [old_fill, current_fill]
    return diffs


def get_diffs_str(diffs, key):
    """
    For a key in the diffs structure, return a string describing the status change
    """
    # pad = (3 if len(key) == 3 else 4) * " "
    status_change = ""
    fill_change = ""
    if STATUS_CHANGE in diffs[key]:
        got_better = (
            STATUS.index(diffs[key][STATUS_CHANGE][1])
            - STATUS.index(diffs[key][STATUS_CHANGE][0])
            < 0
        )
        emoji = UP_ARROW if got_better else DOWN_ARROW
        status_change = f"Status Changed:      {diffs[key][STATUS_CHANGE][0]} ➜ {diffs[key][STATUS_CHANGE][1]} {emoji}\n"
    if FILL_CHANGE in diffs[key]:
        got_better = (
            int(diffs[key][FILL_CHANGE][1]) - int(diffs[key][FILL_CHANGE][0]) > 0
        )
        emoji = UP_ARROW if got_better else DOWN_ARROW
        fill_change = f"Blood Level Changed: {diffs[key][FILL_CHANGE][0]}% ➜ {diffs[key][FILL_CHANGE][1]}% {emoji}\n"
    diffs_str = f"*{key}*\n```\n{status_change}{fill_change}\n```\n"
    return diffs_str


def diffs_to_str(diffs, last_update_time):
    """
    Convert all diffs to a string
    """
    diffs_str = "*Blood Stocks Changed!*\n\n"
    for key in diffs:
        diff_str = get_diffs_str(diffs, key)
        diffs_str += diff_str

    diffs_str += "\n"
    diffs_str += (
        f"*Last Red Cross Update*: {last_update_time.strftime('%-d %B %Y %H:%M')}\n"
    )
    return diffs_str


def diffs_with_bloodtype_to_str(diffs, bloodtype, last_update_time):
    """
    Convert all diffs to a string
    """
    if bloodtype not in diffs:
        return None
    diffs_str = "*Blood Stocks Changed!*\n\n"
    diff_str = get_diffs_str(diffs, bloodtype)
    diffs_str += diff_str

    diffs_str += "\n"
    diffs_str += (
        f"*Last Red Cross Update*: {last_update_time.strftime('%-d %B %Y %H:%M')}\n"
    )
    return diffs_str
