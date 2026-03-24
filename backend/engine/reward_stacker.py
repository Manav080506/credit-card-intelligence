from backend.engine.earn_calculator import calculate_reward
from backend.engine.platform_reward_engine import calculate_platform_reward


def calculate_stacked_rewards(
    card_id: str,
    amount: float,
    category: str,
    platform_id: str | None = None
):
    card_reward = calculate_reward(card_id, amount, category)

    result = {
        "card_reward": card_reward,
        "platform_reward": None,
        "warnings": []
    }

    if platform_id:
        platform_result = calculate_platform_reward(platform_id, amount, category)
        result["platform_reward"] = platform_result

        if platform_result.get("warning"):
            result["warnings"].append(platform_result["warning"])

    return result
