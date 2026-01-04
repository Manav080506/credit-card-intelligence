import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLATFORM_DATA_DIR = os.path.join(BASE_DIR, "data", "platforms")


def load_platform(platform_id: str) -> dict:
    path = os.path.join(PLATFORM_DATA_DIR, f"{platform_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Platform data not found: {platform_id}")

    with open(path, "r") as f:
        return json.load(f)


def calculate_platform_reward(platform_id: str, amount: float, category: str) -> dict:
    platform = load_platform(platform_id)

    if category in platform.get("excluded_categories", []):
        return {
            "platform_reward": 0,
            "unit": platform["reward_type"],
            "eligible": False,
            "warning": f"No platform rewards for {category.replace('_', ' ')} payments"
        }

    if category not in platform.get("eligible_categories", []):
        return {
            "platform_reward": 0,
            "unit": platform["reward_type"],
            "eligible": False,
            "warning": "Category not eligible for platform rewards"
        }

    reward = amount * platform["reward_rate"]

    return {
        "platform_reward": round(reward, 2),
        "unit": platform["reward_type"],
        "eligible": True,
        "warning": None
    }
