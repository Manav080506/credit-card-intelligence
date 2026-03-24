from backend.engine.reward_stacker import calculate_stacked_rewards
from backend.engine.bootstrap import CARDS


def optimize_wallet(card_ids, monthly_spend):

    best_per_category = {}
    total_monthly_reward = 0

    for category, amount in monthly_spend.items():

        best_card = None
        best_value = 0

        for card_id in card_ids:

            result = calculate_stacked_rewards(
                card_id=card_id,
                amount=amount,
                category=category
            )

            reward_value = result["card_reward"]["reward_amount"]

            if reward_value > best_value:
                best_value = reward_value
                best_card = card_id

        best_per_category[category] = {
            "card_id": best_card,
            "monthly_reward": round(best_value, 2)
        }

        total_monthly_reward += best_value

    # yearly fee calculation
    yearly_fee_total = 0

    for card_id in set([v["card_id"] for v in best_per_category.values()]):

        card = CARDS.get(card_id, {})
        fee = card.get("fees", {}).get("annual_fee", 0)

        yearly_fee_total += fee

    yearly_reward = total_monthly_reward * 12
    net_yearly_value = yearly_reward - yearly_fee_total

    return {
        "best_card_per_category": best_per_category,
        "total_monthly_reward": round(total_monthly_reward, 2),
        "estimated_yearly_reward": round(yearly_reward, 2),
        "estimated_annual_fees": yearly_fee_total,
        "net_yearly_value": round(net_yearly_value, 2)
    }
