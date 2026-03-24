from backend.engine.bootstrap import CARDS
from backend.engine.cap_engine import apply_cap


def calculate_reward(card_id: str, amount: float, category: str):

    if card_id not in CARDS:
        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": "card not found"
        }

    card = CARDS[card_id]

    excluded = card.get("constraints", {}).get("excluded_categories", [])
    cap = card.get("constraints", {}).get("monthly_cap")

    if category in excluded:
        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": f"{category} excluded"
        }

    rules = card["earn_rules"]

    exact = []
    fallback = []

    for r in rules:

        if r["category"] == category:
            exact.append(r)

        elif r["category"] == "others":
            fallback.append(r)

    candidates = exact if exact else fallback

    if not candidates:
        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": "no rule"
        }

    best = sorted(candidates, key=lambda x: x["reward_rate"], reverse=True)[0]

    if best["reward_unit"] == "points_per_150":
        reward = (amount / 150) * best["reward_rate"]
        effective_rate = reward / amount

    else:
        reward = amount * best["reward_rate"]
        effective_rate = best["reward_rate"]

    final_reward, cap_applied = apply_cap(reward, cap)

    return {
        "reward_amount": round(final_reward, 2),
        "reward_unit": best["reward_unit"],
        "effective_rate": round(effective_rate, 4),
        "cap_applied": cap_applied,
        "explanation": f"{best['category']} reward applied"
    }
