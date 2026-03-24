import re


MERCHANT_CATEGORY_RULES = {

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
