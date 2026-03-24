from backend.engine.bootstrap import CARDS
from backend.engine.cap_engine import apply_reward_cap


def calculate_reward(
    card_id: str,
    amount: float,
    category: str
):

    if card_id not in CARDS:

        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": "card not found"
        }


    card = CARDS[card_id]


    excluded = card.get(
        "constraints",
        {}
    ).get(
        "excluded_categories",
        []
    )


    if category in excluded:

        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": f"{category} excluded"
        }


    rules = card.get("earn_rules", [])


    exact_rules = []
    fallback_rules = []


    for rule in rules:

        if rule["category"] == category:

            exact_rules.append(rule)

        elif rule["category"] == "others":

            fallback_rules.append(rule)


    candidates = exact_rules if exact_rules else fallback_rules


    if not candidates:

        return {
            "reward_amount": 0,
            "reward_unit": None,
            "effective_rate": 0,
            "cap_applied": False,
            "explanation": "no matching rule"
        }


    best_rule = sorted(

        candidates,

        key=lambda x: x.get("reward_rate", 0),

        reverse=True

    )[0]


    reward_rate = best_rule.get("reward_rate", 0)

    reward_unit = best_rule.get("reward_unit", "cashback")


    if reward_unit == "points_per_150":

        effective_rate = reward_rate / 150

    else:

        effective_rate = reward_rate


    final_reward = apply_reward_cap(

        spend=amount,

        reward_rate=effective_rate,

        cap=best_rule.get("cap"),

        post_cap_rate=best_rule.get("post_cap_reward_rate")

    )


    cap_applied = best_rule.get("cap") is not None


    return {

        "reward_amount": round(final_reward, 2),

        "reward_unit": reward_unit,

        "effective_rate": round(effective_rate, 4),

        "cap_applied": cap_applied,

        "explanation": f"{best_rule['category']} reward applied"

    }
