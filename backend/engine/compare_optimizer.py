from backend.engine.reward_stacker import calculate_stacked_rewards
from backend.engine.bootstrap import CARDS
from backend.engine.reward_value_converter import convert_reward_to_value

def compare_cards(card_ids, sample_spend):

    results = []

    for card_id in card_ids:

        total_reward = 0

        category_breakdown = {}

        for category, amount in sample_spend.items():

            r = calculate_stacked_rewards(
                card_id=card_id,
                amount=amount,
                category=category
            )

            raw = r["card_reward"]["reward_amount"]

            unit = r["card_reward"]["reward_unit"]

            value = convert_reward_to_value(raw, unit)

            category_breakdown[category] = value

            total_reward += value

        annual_fee = CARDS[card_id]["fees"]["annual_fee"]

        yearly_value = total_reward * 12

        effective_return_pct = (total_reward / sum(sample_spend.values())) * 100

        results.append({

            "card_id": card_id,

            "monthly_reward_value": round(total_reward, 2),

            "yearly_reward_value": round(yearly_value, 2),

            "annual_fee": annual_fee,

            "net_yearly_value": round(yearly_value - annual_fee, 2),

            "effective_return_pct": round(effective_return_pct, 2),

            "category_breakdown": category_breakdown

        })

    results.sort(key=lambda x: x["net_yearly_value"], reverse=True)

    return {

        "winner": results[0]["card_id"],

        "ranking": results

    }
