import json
import os
from typing import Dict, List

from backend.engine.merchant_classifier import classify_merchant
from backend.workers.merchant_learning_worker import get_category


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "user_spend_pattern_latest.json")


class UserSpendPatternWorker:
    """Analyze transactions and summarize spend by reward category."""

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def _resolve_category(self, merchant: str) -> str:
        mapped = get_category(merchant)
        if mapped:
            return mapped

        classified = classify_merchant(merchant)
        return classified.get("category", "others")

    def aggregate_category_spend(self, transactions: List[Dict]) -> Dict[str, float]:
        """Aggregate total spend per category for a list of transactions."""
        totals: Dict[str, float] = {}

        for tx in transactions:
            merchant = tx.get("merchant", "")
            amount = float(tx.get("amount", 0) or 0)
            category = self._resolve_category(merchant)

            totals[category] = round(totals.get(category, 0.0) + amount, 2)

        return totals

    def analyze_transactions(self, transactions: List[Dict]) -> Dict[str, float]:
        """Analyze transaction list and persist latest spend-pattern output."""
        result = self.aggregate_category_spend(transactions)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(result, f, indent=2)

        return result

    def run(self):
        """Run a minimal standalone spend pattern demo."""
        sample_transactions = [
            {"merchant": "Amazon", "amount": 2000},
            {"merchant": "Swiggy", "amount": 500},
        ]
        return self.analyze_transactions(sample_transactions)


def aggregate_category_spend(transactions: List[Dict]):
    return UserSpendPatternWorker().aggregate_category_spend(transactions)


def analyze_transactions(transactions: List[Dict]):
    return UserSpendPatternWorker().analyze_transactions(transactions)


if __name__ == "__main__":
    worker = UserSpendPatternWorker()
    print(json.dumps(worker.run(), indent=2))
