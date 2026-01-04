import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CARD_DATA_DIR = os.path.join(BASE_DIR, "data", "cards")


def load_card(card_id: str) -> dict:
    path = os.path.join(CARD_DATA_DIR, f"{card_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Card data not found for: {card_id}")

    with open(path, "r") as f:
        return json.load(f)


def calculate_redemption(card_id: str, points: int) -> dict:
    card = load_card(card_id)

    rules = card.get("redemption_rules", [])
    if not rules:
        return {
            "error": "This card does not support point redemption"
        }

    options = []

    for rule in rules:
        if points < rule["min_points"]:
            continue

        value = round(points * rule["value_per_point"], 2)

        options.append({
            "id": rule["id"],
            "type": rule["type"],
            "partner": rule["partner"],
            "value": value,
            "value_per_point": rule["value_per_point"],
            "notes": rule["notes"]
        })

    if not options:
        return {
            "error": "Insufficient points for any redemption option"
        }

    options.sort(key=lambda x: x["value"], reverse=True)

    return {
        "best_option": options[0],
        "all_options": options
    }
