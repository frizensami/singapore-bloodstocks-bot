#!/usr/bin/env python3
import requests
from pprint import pprint
from bs4 import BeautifulSoup, Comment
import sys

URL = "https://www.redcross.sg/"

BLOOD_BANK_LVL = "blood_bank_level"
BLOOD_GROUP_PREFIX = "blood_group"
BLOOD_GROUPS = [
    {"class_": "a_group", "name": "A"},
    {"class_": "b_group", "name": "B"},
    {"class_": "o_group", "name": "O"},
    {"class_": "ab_group", "name": "AB"},
]

"""
Status structure
{
    <bloodtype:str> : { status: <STATUS>, fill_level: <int> }
}

"""


def get_bloodstocks():
    state = {}
    try:
        # Now we have a timeout to prevent an infinite hang of this method
        page = requests.get(URL, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        # Cycle through positive and negative blood types
        for group in BLOOD_GROUPS:
            bloodgroup_html_all = soup.find_all(
                "div", class_=group["class_"]
            )
            for bloodgroup_html in bloodgroup_html_all:
                # Get the blood group text via the h3 tag's text
                blood_group = bloodgroup_html.find("h3").text.strip()
                # Get the status via the h5 tag under the blood-grp-text class
                status_text = bloodgroup_html.find("h5").text.strip()
                # Get the fill level via a comment - first child of the 'blood-grp-hover' div
                fill_level = bloodgroup_html.find("div", class_="blood-grp-hover").find_all(string=lambda text: isinstance(text, Comment))[0].strip()
                # Add the blood group to the state
                state[blood_group] = {
                    "status": status_text,
                    "fill_level": fill_level,
                }
    except:
        print("Unexpected error while getting bloodstocks:", sys.exc_info()[0])

    pprint(state)
    return state


if __name__ == "__main__":
    print(get_bloodstocks())
