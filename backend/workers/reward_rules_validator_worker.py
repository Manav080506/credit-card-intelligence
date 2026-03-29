import json
import os
from typing import Dict, List


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CATEGORIES_FILE = os.path.join(BASE_DIR, "data", "categories.json")
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "reward_rules_validator_latest.json")


class RewardRulesValidatorWorker:
    """Validate reward rules and detect conflicts before card data persistence."""

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def _load_categories(self) -> set[str]:
        if not os.path.exists(CATEGORIES_FILE):
            return set()

        with open(CATEGORIES_FILE, "r") as f:
            data = json.load(f)

        categories = data.get("categories", [])
        return {entry.get("id") for entry in categories if entry.get("id")}

    def detect_conflict(self, rule_a: Dict, rule_b: Dict) -> bool:
        """Detect conflict when same category has incompatible reward definitions."""
        same_category = rule_a.get("category") == rule_b.get("category")
        same_period = (rule_a.get("cap_period") or "") == (rule_b.get("cap_period") or "")

        if not same_category or not same_period:
            return False

        rate_a = rule_a.get("reward_rate")
        rate_b = rule_b.get("reward_rate")

        unit_a = rule_a.get("reward_unit") or rule_a.get("reward_type")
        unit_b = rule_b.get("reward_unit") or rule_b.get("reward_type")

        # Different rates for the same category/period without distinct conditions are conflicting.
        if rate_a != rate_b and unit_a == unit_b:
            cond_a = rule_a.get("condition")
            cond_b = rule_b.get("condition")
            if not cond_a and not cond_b:
                return True

        return False

    def validate_reward_rule(self, rule: Dict) -> Dict:
        """Run base validation checks for a single reward rule."""
        errors: List[str] = []
        categories = self._load_categories()

        reward_rate = rule.get("reward_rate")
        if reward_rate is None or reward_rate < 0 or reward_rate > 100:
            errors.append("reward_rate must be between 0 and 100")

        cap_amount = rule.get("cap")
        if cap_amount is None:
            cap_amount = rule.get("cap_amount")

        if cap_amount is not None and cap_amount < 0:
            errors.append("cap must not be negative")

        category = rule.get("category")
        if category not in categories:
            errors.append("category must exist in categories.json")

        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "rule": rule,
        }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(result, f, indent=2)

        return result

    def run(self):
        """Run a minimal standalone validator demo."""
        sample_rule = {
            "category": "online_shopping",
            "reward_rate": 5,
            "reward_unit": "cashback",
            "cap_amount": 1000,
            "cap_period": "monthly",
        }
        return self.validate_reward_rule(sample_rule)


def validate_reward_rule(rule: Dict):
    return RewardRulesValidatorWorker().validate_reward_rule(rule)


def detect_conflict(rule_a: Dict, rule_b: Dict):
    return RewardRulesValidatorWorker().detect_conflict(rule_a, rule_b)


if __name__ == "__main__":
    worker = RewardRulesValidatorWorker()
    print(json.dumps(worker.run(), indent=2))
