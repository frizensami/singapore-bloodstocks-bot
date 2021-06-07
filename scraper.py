#!/usr/bin/env python3
import requests
from pprint import pprint
from bs4 import BeautifulSoup

URL = "https://www.redcross.sg/"

BLOOD_BANK_LVL = "blood_bank_level"
POS_NEG = [{"class_": "positives", "name": "+"}, {"class_": "negatives", "name": "-"}]
BLOOD_GROUP_PREFIX = "blood_group"
BLOOD_GROUPS = [
    {"class_": "a_group", "name": "A"},
    {"class_": "b_group", "name": "B"},
    {"class_": "o_group", "name": "O"},
    {"class_": "ab_group", "name": "AB"},
]
STATUS = ["Healthy", "Moderate", "Low", "Critical"]


def get_bloodstocks():
    state = {}
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # Cycle through positive and negative blood types
    for pos_neg in POS_NEG:
        pos_or_negs = soup.find("div", class_=BLOOD_BANK_LVL + " " + pos_neg["class_"])
        # Cycle through each blood group
        for group in BLOOD_GROUPS:
            bloodgroup_html = pos_or_negs.find(
                "div", class_=BLOOD_GROUP_PREFIX + " " + group["class_"]
            )
            info_text = bloodgroup_html.find("div", class_="info_text")
            status_text = info_text.findAll("span", class_="status_text")[
                1
            ].text.strip()
            fill_level = (
                bloodgroup_html.findAll("div", class_="fill_humam")[0]
                .get("style")[8:]
                .split("%")[0]
                .strip()
            )
            # pprint(status_text)
            state[group["name"] + pos_neg["name"]] = {
                "status": status_text,
                "fill_level": fill_level,
            }

    pprint(state)
    return state


if __name__ == "__main__":
    print(get_bloodstocks())
