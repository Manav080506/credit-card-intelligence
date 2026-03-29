import json
import os
from typing import Dict

from backend.engine.bootstrap import CARDS
from backend.engine.earn_calculator import calculate_reward
from backend.engine.reward_stacker import calculate_stacked_rewards


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "dynamic_reward_predictor_latest.json")

# Guardrail caps to keep forecasted monthly rewards realistic.
CATEGORY_CAPS = {
    "online_shopping": 20000,
    "dining": 10000,
    "travel": 30000,
    "utilities": 15000,
}

# Upper bound for unknown categories to avoid pathological inputs.
DEFAULT_CATEGORY_CAP = 50000


class DynamicRewardPredictorWorker:
    """Predict the best card for a future spend pattern."""

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def _normalize_spend_pattern(self, spend_pattern: Dict[str, float]) -> Dict[str, float]:
        """Normalize spend inputs with category caps before running card reward estimates."""
        normalized = {}

        for category, amount in spend_pattern.items():
            safe_amount = max(0.0, float(amount or 0))
            cap = CATEGORY_CAPS.get(category, DEFAULT_CATEGORY_CAP)
            normalized[category] = min(safe_amount, cap)

        return normalized

    def estimate_future_rewards(self, spend_pattern: Dict[str, float]) -> Dict[str, Dict]:
        """Estimate total rewards for each card across category-wise spend."""
        normalized_pattern = self._normalize_spend_pattern(spend_pattern)
        card_estimates: Dict[str, Dict] = {}

        for card_id in CARDS:
            total_reward = 0.0
            per_category = {}

            for category, amount in normalized_pattern.items():
                base = calculate_reward(card_id, amount, category)
                stacked = calculate_stacked_rewards(card_id, amount, category)

                base_reward = float(base.get("reward_amount", 0) or 0)
                stack_card_reward = float(
                    stacked.get("card_reward", {}).get("reward_amount", 0) or 0
                )

                reward_amount = max(base_reward, stack_card_reward)
                total_reward += reward_amount

                per_category[category] = {
                    "estimated_reward": round(reward_amount, 2),
                    "explanation": base.get("explanation", "computed"),
                    "input_amount": round(float(spend_pattern.get(category, 0) or 0), 2),
                    "normalized_amount": round(float(amount), 2),
                }

            card_estimates[card_id] = {
                "total_estimated_reward": round(total_reward, 2),
                "category_breakdown": per_category,
            }

        return card_estimates

    def predict_best_card(self, spend_pattern: Dict[str, float]) -> Dict:
        """Predict best card by maximum estimated future reward."""
        estimates = self.estimate_future_rewards(spend_pattern)

        if not estimates:
            result = {
                "best_card_id": None,
                "best_reward": 0,
                "estimates": {},
            }
        else:
            best_card_id = max(
                estimates,
                key=lambda card_id: estimates[card_id]["total_estimated_reward"],
            )

            result = {
                "best_card_id": best_card_id,
                "best_reward": estimates[best_card_id]["total_estimated_reward"],
                "estimates": estimates,
            }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(result, f, indent=2)

        return result

    def run(self):
        """Run a minimal standalone prediction demo."""
        sample_spend_pattern = {
            "online_shopping": 4000,
            "dining": 2000,
            "fuel": 1500,
            "others": 2500,
        }
        return self.predict_best_card(sample_spend_pattern)


def estimate_future_rewards(spend_pattern: Dict[str, float]):
    return DynamicRewardPredictorWorker().estimate_future_rewards(spend_pattern)


def predict_best_card(spend_pattern: Dict[str, float]):
    return DynamicRewardPredictorWorker().predict_best_card(spend_pattern)


if __name__ == "__main__":
    worker = DynamicRewardPredictorWorker()
    print(json.dumps(worker.run(), indent=2))
