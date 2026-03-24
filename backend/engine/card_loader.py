import json
import os
from backend.engine.card_validator import validate_card, CardValidationError

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CARD_DATA_DIR = os.path.join(BASE_DIR, "data", "cards")


class CardLoadResult:
    def __init__(self):
        self.cards = {}
        self.errors = []

    def register(self, card):
        self.cards[card["card_id"]] = card


def load_all_cards() -> CardLoadResult:
    result = CardLoadResult()

    for root, _, files in os.walk(CARD_DATA_DIR):
        for file in files:
            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)

            try:
                with open(path, "r") as f:
                    card = json.load(f)

                validate_card(card, file)
                result.register(card)

            except (json.JSONDecodeError, CardValidationError, Exception) as e:
                result.errors.append(f"{file}: {str(e)}")

    return result
