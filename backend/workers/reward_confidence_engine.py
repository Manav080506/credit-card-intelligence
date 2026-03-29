import json
import os
from typing import Dict


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "reward_confidence_engine_latest.json")


class RewardConfidenceEngineWorker:
    """Compute confidence scores for reward rules and reward predictions."""

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def calculate_confidence(self, rule: Dict) -> float:
        """Calculate confidence score (0..1) for a single reward rule."""
        score = 0.2

        if rule.get("reward_rate") is not None:
            score += 0.3

        if rule.get("category") and rule.get("category") != "others":
            score += 0.2

        cap_known = rule.get("cap") is not None or rule.get("cap_amount") is not None
        if cap_known:
            if rule.get("cap_period"):
                score += 0.2
            else:
                score += 0.1
        else:
            # No cap can still be predictable when explicitly unbounded.
            if rule.get("no_cap") is True:
                score += 0.15

        if rule.get("reward_unit") in {"cashback", "points_per_150", "miles"}:
            score += 0.1

        return round(min(1.0, max(0.0, score)), 4)

    def calculate_prediction_confidence(self, prediction: Dict) -> float:
        """Calculate confidence score (0..1) for a card reward prediction."""
        estimates = prediction.get("estimates", {})
        best_card_id = prediction.get("best_card_id")

        if not estimates or not best_card_id or best_card_id not in estimates:
            return 0.0

        best_reward = float(estimates[best_card_id].get("total_estimated_reward", 0) or 0)
        rewards = sorted(
            [float(v.get("total_estimated_reward", 0) or 0) for v in estimates.values()],
            reverse=True,
        )

        if not rewards:
            return 0.0

        second_best = rewards[1] if len(rewards) > 1 else 0.0
        margin = max(0.0, best_reward - second_best)

        # Confidence rises when the top recommendation is clearly separated.
        margin_score = min(0.5, margin / max(1.0, best_reward))
        base_score = 0.4 if best_reward > 0 else 0.1
        score = base_score + margin_score

        return round(min(1.0, max(0.0, score)), 4)

    def run(self):
        """Run a minimal standalone confidence demo."""
        sample_rule = {
            "category": "online_shopping",
            "reward_rate": 5,
            "reward_unit": "cashback",
            "cap_amount": 1000,
            "cap_period": "monthly",
        }
        sample_prediction = {
            "best_card_id": "sample_card",
            "estimates": {
                "sample_card": {"total_estimated_reward": 1200},
                "other_card": {"total_estimated_reward": 900},
            },
        }

        output = {
            "rule_confidence": self.calculate_confidence(sample_rule),
            "prediction_confidence": self.calculate_prediction_confidence(sample_prediction),
        }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(output, f, indent=2)

        return output


def calculate_confidence(rule: Dict):
    return RewardConfidenceEngineWorker().calculate_confidence(rule)


def calculate_prediction_confidence(prediction: Dict):
    return RewardConfidenceEngineWorker().calculate_prediction_confidence(prediction)


if __name__ == "__main__":
    worker = RewardConfidenceEngineWorker()
    print(json.dumps(worker.run(), indent=2))
