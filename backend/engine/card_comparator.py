from backend.engine.reward_stacker import calculate_stacked_rewards


def compare_cards(card_ids, spend_profile):

    output = []

    for card_id in card_ids:

        total = 0
        category_breakdown = {}

        for category, amount in spend_profile.items():

            result = calculate_stacked_rewards(
                card_id,
                amount,
                category
            )

            reward = result["card_reward"]["reward_amount"]

            total += reward

            category_breakdown[category] = reward

        output.append({
            "card_id": card_id,
            "monthly_value": round(total, 2),
            "breakdown": category_breakdown
        })

    return sorted(
        output,
        key=lambda x: x["monthly_value"],
        reverse=True
    )
