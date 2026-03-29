from typing import Dict


def normalize_spend(spend: Dict[str, float]) -> Dict[str, float]:
    return {
        'online_shopping': max(0.0, float(spend.get('online_shopping', 0) or 0)),
        'dining': max(0.0, float(spend.get('dining', 0) or 0)),
        'travel': max(0.0, float(spend.get('travel', 0) or 0)),
        'utilities': max(0.0, float(spend.get('utilities', 0) or 0)),
    }


def normalize_reward(card: Dict, spend: Dict[str, float]) -> float:
    reward_model = card.get('reward_model', {})

    online_rate = float(reward_model.get('online_base', card.get('online_shopping', 0)) or 0)
    dining_rate = float(reward_model.get('dining', card.get('dining', 0)) or 0)
    travel_rate = float(reward_model.get('travel', card.get('travel', 0)) or 0)
    utility_rate = float(reward_model.get('utilities', card.get('utilities', 0)) or 0)

    base_reward = (
        spend['online_shopping'] * online_rate
        + spend['dining'] * dining_rate
        + spend['travel'] * travel_rate
        + spend['utilities'] * utility_rate
    )

    conversion = card.get('reward_conversion', {}).get('value_per_point', 1)
    normalized = base_reward * float(conversion or 1)

    monthly_cap = card.get('caps', {}).get('monthly_cap')
    if monthly_cap is not None:
        normalized = min(normalized, float(monthly_cap))

    return round(normalized, 2)
