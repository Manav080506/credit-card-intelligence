"""Merchant Category Classifier.

Classifies merchants into reward categories based on MCC codes and merchant names.
Uses deterministic rule-based classification with optional ML enhancement.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MERCHANT_TRAINING_DATA = DATA_DIR / "merchants" / "training_data.json"


class MerchantCategoryClassifier:
    """Classify merchants into reward categories."""
    
    # MCC (Merchant Category Code) to reward category mapping
    MCC_MAPPING = {
        # Airlines
        4511: "travel",
        4582: "travel",  # Parking
        
        # Ground transportation
        4121: "travel",  # Taxi, limousine
        4112: "travel",  # Passenger railways
        4513: "travel",  # Rental car agencies
        
        # Lodging
        7011: "travel",  # Hotels, motels
        7012: "travel",  # Timeshares
        
        # Dining
        5812: "dining",  # Eating places (restaurants)
        5813: "dining",  # Drinking places (bars)
        7299: "dining",  # Miscellaneous food services
        
        # Groceries
        5411: "groceries",  # Grocery stores
        5412: "groceries",  # Supermarkets
        5422: "groceries",  # Freezer and locker provisioning
        
        # Fuel
        5172: "fuel",  # Gas stations
        5541: "fuel",  # Gasoline stations
        
        # Online shopping
        5942: "online_shopping",  # Book stores
        5961: "online_shopping",  # Mail order
        5965: "online_shopping",  # Hobby shops
        
        # Utilities
        4814: "utilities",  # Telephone services
        4899: "utilities",  # Electric, gas, water agencies
        9399: "utilities",  # Government services
        
        # General
        6211: "general",  # Securities brokers
        6012: "general",  # Banks
    }
    
    # Keyword-based category mapping
    KEYWORD_MAPPING = {

    "online_shopping": [

        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "meesho",
        "snapdeal",
        "nykaa",
        "tatacliq",
        "paytm mall",
        "shopclues"

    ],

    "dining": [

        "swiggy",
        "zomato",
        "dominos",
        "pizza hut",
        "mcdonald",
        "burger king",
        "kfc",
        "barbeque nation",
        "haldiram",
        "ccd",
        "starbucks"

    ],

    "travel": [

        "irctc",
        "makemytrip",
        "goibibo",
        "yatra",
        "air india",
        "indigo",
        "spicejet",
        "vistara",
        "uber",
        "ola",
        "redbus",
        "booking.com"

    ],

    "groceries": [

        "bigbasket",
        "blinkit",
        "zepto",
        "instamart",
        "reliance smart",
        "dmart",
        "more retail",
        "grofers",
        "spencer"

    ],

    "fuel": [

        "indian oil",
        "bharat petroleum",
        "hp petrol",
        "shell",
        "essar oil"

    ],

    "utilities": [

        "electricity",
        "bsnl",
        "jio",
        "airtel",
        "vodafone",
        "vi ",
        "broadband",
        "dth",
        "tataplay"

    ]

}


DEFAULT_CATEGORY = "others"


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(

        r'[^a-z0-9 ]',

        '',

        text

    )

    return text


def classify_merchant(

    merchant_name: str

):

    clean_name = normalize_text(

        merchant_name

    )


    for category, keywords in MERCHANT_CATEGORY_RULES.items():

        for keyword in keywords:

            if keyword in clean_name:

                return {

                    "category": category,

                    "confidence": 0.9,

                    "matched_keyword": keyword

                }


    return {

        "category": DEFAULT_CATEGORY,

        "confidence": 0.3,

        "matched_keyword": None

    }
