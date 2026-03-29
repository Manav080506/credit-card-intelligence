# backend/workers/llm_card_parser.py

import json
import re
import os

from backend.engine.card_validator import validate_card


# -------------------------
# text cleaning
# -------------------------

def clean_text(text: str):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------
# extract basic info
# -------------------------

def extract_basic_fields(text: str):

    card_name_match = re.search(

        r"([A-Z][A-Za-z0-9\s]+Credit Card)",

        text

    )

    card_name = (

        card_name_match.group(1)

        if card_name_match

        else "Unknown Credit Card"

    )


    reward_type = "cashback"


    if "points" in text.lower():

        reward_type = "points"


    # detect reward percentage
    reward_rate = 0.01


    percent_match = re.search(

        r"(\d+)%",

        text

    )


    if percent_match:

        reward_rate = int(

            percent_match.group(1)

        ) / 100


    annual_fee = 0


    fee_match = re.search(

        r"₹\s?(\d{3,5})",

        text

    )


    if fee_match:

        annual_fee = int(fee_match.group(1))


    issuer = "unknown"


    if "hdfc" in text.lower():

        issuer = "hdfc"

    elif "icici" in text.lower():

        issuer = "icici"

    elif "axis" in text.lower():

        issuer = "axis"

    elif "sbi" in text.lower():

        issuer = "sbi"


    return {

        "card_name": card_name,

        "reward_type": reward_type,

        "reward_rate": reward_rate,

        "annual_fee": annual_fee,

        "issuer": issuer

    }

# -------------------------
# build structured json
# -------------------------

def build_card_json(parsed_data):

    card_id = parsed_data["card_name"].lower().replace(

        " ",

        "_"

    )


    return {

        "card_id": card_id,

        "card_name": parsed_data["card_name"],

        "issuer": parsed_data["issuer"],

        "network": ["Visa"],

        "tier": "unknown",

        "reward_type": parsed_data["reward_type"],

        "fees": {

            "joining_fee": 0,

            "annual_fee": parsed_data["annual_fee"]

        },

       "earn_rules": [

         {
           "category": "others",
           "reward_rate": parsed_data["reward_rate"],
           "reward_unit": parsed_data["reward_type"]
          }

           ],

        "constraints": {

            "excluded_categories": [],

            "monthly_cap": None

        },

        "meta": {

            "source": "llm_parser",

            "confidence": 0.6

        }

    }


# -------------------------
# parse page
# -------------------------

def parse_card_page(raw_text: str):

    cleaned = clean_text(raw_text)

    parsed = extract_basic_fields(cleaned)

    card_json = build_card_json(parsed)

    validate_card(

        card_json,

        card_json["card_name"]

    )

    return card_json


# -------------------------
# save file
# -------------------------

def save_card(card_json):

    issuer = card_json["issuer"]


    folder_path = f"backend/data/cards/{issuer}"


    # create folder if not exists
    os.makedirs(

        folder_path,

        exist_ok=True

    )


    file_path = f"{folder_path}/{card_json['card_id']}.json"


    with open(file_path, "w") as f:

        json.dump(

            card_json,

            f,

            indent=2

        )


    return file_path


# -------------------------
# full pipeline
# -------------------------

def parse_and_store_card(raw_text):

    card = parse_card_page(raw_text)

    path = save_card(card)


    return {

        "card_saved": path,

        "card_id": card["card_id"],

        "issuer": card["issuer"]

    }
