from backend.engine.card_registry import CARDS
from backend.engine.earn_calculator import calculate_reward
from backend.engine.reward_value_converter import convert_reward_to_value


def best_card_for_transaction(
    card_ids: list[str],
    amount: float,
    category: str
):

    best_card = None
    best_value = 0
    best_reward = None

    for card_id in card_ids:

        card = CARDS.get(card_id)

        if not card:
            continue

        reward_result = calculate_reward(
            card_id=card_id,
            amount=amount,
            category=category
        )

        reward_value = convert_reward_to_value(
            reward_result,
            card
        )

        if reward_value > best_value:

            best_value = reward_value

            best_card = card_id

            best_reward = reward_result


    return {

        "recommended_card": best_card,

        "expected_reward_value": round(best_value, 2),

        "reward_details": best_reward

    }
