import requests
from bs4 import BeautifulSoup

from backend.engine.card_validator import validate_card


CARD_SOURCES = [

    {
        "issuer": "hdfc",

        "url": "https://www.hdfcbank.com/personal/pay/cards/credit-cards"
    },

    {
        "issuer": "icici",

        "url": "https://www.icicibank.com/personal-banking/cards/credit-card"
    }

]


def discover_cards():

    discovered_cards = []


    for source in CARD_SOURCES:

        try:

            response = requests.get(source["url"], timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")


            card_names = soup.find_all("h3")


            for c in card_names:

                card_name = c.text.strip()


                card_data = {

                    "card_id": card_name.lower().replace(" ", "_"),

                    "card_name": card_name,

                    "issuer": source["issuer"],

                    "network": ["Visa"],

                    "tier": "unknown",

                    "reward_type": "unknown",

                    "fees": {

                        "joining_fee": 0,

                        "annual_fee": 0

                    },

                    "earn_rules": [

                        {

                            "category": "others",

                            "reward_rate": 0.01,

                            "reward_unit": "cashback"

                        }

                    ]

                }


                try:

                    validate_card(card_data, card_name)

                    discovered_cards.append(card_data)

                except Exception:

                    pass


        except Exception:

            pass


    return {

        "cards_found": len(discovered_cards)

    }
