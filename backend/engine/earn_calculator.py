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
            "explanation": "No reward rule applicable"
        }

    reward_rate = rule.get("reward_rate", 0)
    reward = amount * reward_rate

    cap_applied = False
    cap_info = rule.get("cap")

    if cap_info:
        cap_amount = cap_info.get("amount")
        if cap_amount is not None and reward > cap_amount:
            reward = cap_amount
            cap_applied = True

    reward_unit = rule.get("reward_unit", "unknown")

    explanation = f"{int(reward_rate * 100)}% {reward_unit} on {category.replace('_', ' ')}"

    if cap_applied:
        explanation += " (monthly cap applied)"

    return {
        "reward_amount": round(reward, 2),
        "reward_unit": reward_unit,
        "cap_applied": cap_applied,
        "explanation": explanation
    }
