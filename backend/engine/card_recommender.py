import os
import json

from backend.engine.earn_calculator import calculate_reward
from backend.engine.redeem_calculator import calculate_redemption

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CARD_DATA_DIR = os.path.join(BASE_DIR, "data", "cards")


def load_all_cards() -> list[dict]:
    cards = []
    for file in os.listdir(CARD_DATA_DIR):
        if file.endswith(".json"):
            with open(os.path.join(CARD_DATA_DIR, file), "r") as f:
                cards.append(json.load(f))
    return cards


def estimate_monthly_value(card: dict, monthly_spend: dict) -> dict:
    card_id = card["card_id"]
    total_earn_value = 0.0

    # 1) Earn value simulation
    for category, amount in monthly_spend.items():
        try:
            result = calculate_reward(
                card_id=card_id,
                amount=amount,
                category=category
            )

            # Cashback cards already give ₹
            if result["reward_unit"] == "cashback":
                total_earn_value += result["reward_amount"]

            # Points cards: approximate conversion via best redemption
            elif result["reward_unit"].startswith("points"):
                # crude assumption: 1 point per reward unit
                points = result["reward_amount"]
                redemption = calculate_redemption(card_id, int(points))
                if "best_option" in redemption:
                    total_earn_value += redemption["best_option"]["value"]

        except Exception:
            # category not supported / card missing rules
            continue

    # 2) Annual fee penalty
    annual_fee = card.get("fees", {}).get("annual_fee", 0)
    monthly_fee_penalty = annual_fee / 12 if annual_fee else 0

    net_monthly_value = round(total_earn_value - monthly_fee_penalty, 2)

    return {
        "card_id": card_id,
        "card_name": card.get("card_name"),
        "monthly_value": round(total_earn_value, 2),
        "annual_fee": annual_fee,
        "net_monthly_gain": net_monthly_value
    }


def recommend_cards(monthly_spend: dict, preferences: dict | None = None) -> dict:
    preferences = preferences or {}
    cards = load_all_cards()

    evaluations = []

    for card in cards:
        score = estimate_monthly_value(card, monthly_spend)
        evaluations.append(score)

    evaluations.sort(key=lambda x: x["net_monthly_gain"], reverse=True)

    best = evaluations[0]
    alternatives = evaluations[1:3]

    return {
        "best_card": best,
        "alternatives": alternatives
    }
