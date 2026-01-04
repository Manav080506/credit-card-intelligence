import json
import os
import math

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CARD_DATA_DIR = os.path.join(BASE_DIR, "data", "cards")


def load_card(card_id: str) -> dict:
    path = os.path.join(CARD_DATA_DIR, f"{card_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Card data not found for: {card_id}")

    with open(path, "r") as f:
        return json.load(f)


def calculate_reward(card_id: str, amount: float, category: str) -> dict:
    card = load_card(card_id)

    applicable_rule = None
    fallback_rule = None

    for rule in card.get("earn_rules", []):
        if rule["category"] == category:
            applicable_rule = rule
            break
        if rule["category"] == "others":
            fallback_rule = rule

    rule = applicable_rule or fallback_rule

    if not rule:
        return {
            "reward_amount": 0,
            "reward_unit": None,
            "cap_applied": False,
            "explanation": "No reward rule applicable",
            "metadata": {}
        }

    reward_unit = rule.get("reward_unit")
    cap_applied = False
    metadata = {}

    # CASE 1: Cashback cards
    if reward_unit == "cashback":
        reward = amount * rule.get("reward_rate", 0)

        cap_info = rule.get("cap")
        if cap_info:
            cap_amount = cap_info.get("amount")
            if cap_amount is not None and reward > cap_amount:
                reward = cap_amount
                cap_applied = True

        explanation = f"{int(rule['reward_rate'] * 100)}% cashback on {category.replace('_', ' ')}"
        if cap_applied:
            explanation += " (cap applied)"

        return {
            "reward_amount": round(reward, 2),
            "reward_unit": "cashback",
            "cap_applied": cap_applied,
            "explanation": explanation,
            "metadata": {}
        }

    # CASE 2: Points per spend (e.g. points_per_150)
    if reward_unit.startswith("points_per_"):
        spend_basis = int(reward_unit.split("_")[-1])
        points_per_unit = rule.get("reward_rate", 0)

        units = math.floor(amount / spend_basis)
        points_earned = units * points_per_unit

        metadata = {
            "points_earned": points_earned,
            "spend_basis": spend_basis
        }

        explanation = f"{points_per_unit} points per ₹{spend_basis} spent"

        return {
            "reward_amount": points_earned,
            "reward_unit": "points",
            "cap_applied": False,
            "explanation": explanation,
            "metadata": metadata
        }

    # Fallback
    return {
        "reward_amount": 0,
        "reward_unit": None,
        "cap_applied": False,
        "explanation": "Unsupported reward type",
        "metadata": {}
    }
