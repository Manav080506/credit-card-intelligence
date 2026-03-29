import json
import os
from typing import Dict, List


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "data", "cards")
CATEGORIES_FILE = os.path.join(BASE_DIR, "data", "categories.json")
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "category_gap_detector_latest.json")


class CategoryGapDetectorWorker:
    """Detect missing reward categories and compute category coverage stats."""

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def _load_category_ids(self) -> List[str]:
        if not os.path.exists(CATEGORIES_FILE):
            return []

        with open(CATEGORIES_FILE, "r") as f:
            data = json.load(f)

        return [entry.get("id") for entry in data.get("categories", []) if entry.get("id")]

    def _load_cards(self) -> List[Dict]:
        cards: List[Dict] = []

        if not os.path.exists(CARDS_DIR):
            return cards

        for root, _, files in os.walk(CARDS_DIR):
            for filename in files:
                if not filename.endswith(".json"):
                    continue

                path = os.path.join(root, filename)
                try:
                    with open(path, "r") as f:
                        card = json.load(f)
                    cards.append(card)
                except (json.JSONDecodeError, OSError):
                    continue

        return cards

    def calculate_category_coverage(self) -> Dict[str, Dict]:
        """Calculate how many cards support each category and coverage ratio."""
        category_ids = self._load_category_ids()
        cards = self._load_cards()

        coverage = {category_id: 0 for category_id in category_ids}
        total_cards = len(cards)

        for card in cards:
            seen = set()
            for rule in card.get("earn_rules", []):
                category = rule.get("category")
                if category in coverage and category not in seen:
                    coverage[category] += 1
                    seen.add(category)

        result = {}
        for category_id, count in coverage.items():
            ratio = (count / total_cards) if total_cards else 0.0
            result[category_id] = {
                "cards_supporting": count,
                "coverage_ratio": round(ratio, 4),
            }

        return result

    def detect_missing_categories(self) -> List[str]:
        """Return categories that no current card rewards explicitly."""
        coverage = self.calculate_category_coverage()
        return [category for category, stats in coverage.items() if stats["cards_supporting"] == 0]

    def run(self):
        """Run gap detection and persist a combined summary."""
        coverage = self.calculate_category_coverage()
        missing_categories = self.detect_missing_categories()

        output = {
            "missing_categories": missing_categories,
            "coverage": coverage,
        }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(output, f, indent=2)

        return output


def calculate_category_coverage():
    return CategoryGapDetectorWorker().calculate_category_coverage()


def detect_missing_categories():
    return CategoryGapDetectorWorker().detect_missing_categories()


if __name__ == "__main__":
    worker = CategoryGapDetectorWorker()
    print(json.dumps(worker.run(), indent=2))
