from backend.engine.earn_calculator import calculate_reward
from backend.engine.platform_reward_engine import calculate_platform_reward


def calculate_stacked_rewards(card_id: str, platform_id: str, amount: float, category: str) -> dict:
    card_result = calculate_reward(card_id, amount, category)
    platform_result = calculate_platform_reward(platform_id, amount, category)

    warnings = []
    if platform_result.get("warning"):
        warnings.append(platform_result["warning"])

    return {
        "card_reward": card_result,
        "platform_reward": platform_result,
        "warnings": warnings
    }
