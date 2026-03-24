import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLATFORM_DIR = os.path.join(BASE_DIR, "data", "platforms")


def load_platform(platform_id: str) -> dict:
    path = os.path.join(PLATFORM_DIR, f"{platform_id}.json")
    if not os.path.exists(path):
        raise ValueError(f"Unknown platform: {platform_id}")

    with open(path, "r") as f:
        return json.load(f)


def calculate_platform_reward(platform_id: str, amount: float, category: str) -> dict:
    platform = load_platform(platform_id)

    if category in platform.get("excluded_categories", []):
        return {
            "reward": 0,
            "unit": platform["unit"],
            "eligible": False,
            "warning": f"No platform rewards for {category.replace('_', ' ')}"
        }

    reward = amount * platform["reward_rate"]

    return {
        "reward": round(reward, 2),
        "unit": platform["unit"],
        "eligible": True,
        "warning": None
    }
