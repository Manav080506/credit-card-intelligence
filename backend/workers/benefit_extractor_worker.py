import json
import os
import re
from typing import Dict, Optional


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
OUTPUT_FILE = os.path.join(HISTORY_DIR, "benefit_extractor_latest.json")


class BenefitExtractorWorker:
    """Extract structured reward benefit fields from raw credit-card text."""

    CATEGORY_KEYWORDS = {
        "online_shopping": ["amazon", "flipkart", "myntra", "online", "e-commerce", "ecommerce"],
        "dining": ["swiggy", "zomato", "restaurant", "dining", "food"],
        "travel": ["flight", "hotel", "travel", "uber", "ola", "irctc"],
        "fuel": ["fuel", "petrol", "diesel", "pump"],
        "utilities": ["utility", "electricity", "mobile", "broadband", "bill"],
    }

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def normalize_reward_rate(self, text: str) -> float:
        """Extract reward rate and normalize into a percentage value (0..100)."""
        text_lower = text.lower()

        pct_match = re.search(r"(\d+(?:\.\d+)?)\s*%", text_lower)
        if pct_match:
            return float(pct_match.group(1))

        decimal_match = re.search(r"(?:cashback|reward|points?)\s*(?:at|of)?\s*(0\.\d+)", text_lower)
        if decimal_match:
            return round(float(decimal_match.group(1)) * 100, 4)

        return 0.0

    def detect_cap(self, text: str) -> Dict[str, Optional[float | str]]:
        """Detect cap amount and cap period from free text."""
        text_lower = text.lower()

        cap_amount: Optional[float] = None
        cap_period: Optional[str] = None

        amount_patterns = [
            r"up to\s*([0-9][0-9,]*(?:\.\d+)?)",
            r"capped at\s*([0-9][0-9,]*(?:\.\d+)?)",
            r"max(?:imum)?\s*([0-9][0-9,]*(?:\.\d+)?)",
        ]

        for pattern in amount_patterns:
            match = re.search(pattern, text_lower)
            if match:
                cap_amount = float(match.group(1).replace(",", ""))
                break

        if "per month" in text_lower or "monthly" in text_lower:
            cap_period = "monthly"
        elif "per year" in text_lower or "annual" in text_lower or "yearly" in text_lower:
            cap_period = "yearly"
        elif "per quarter" in text_lower or "quarterly" in text_lower:
            cap_period = "quarterly"

        return {
            "cap_amount": cap_amount,
            "cap_period": cap_period,
        }

    def extract_benefits(self, text: str) -> Dict[str, Optional[float | str]]:
        """Extract category, reward type, reward rate, and cap details from text."""
        text_lower = text.lower()

        category = "others"
        for candidate, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                category = candidate
                break

        reward_type = "points"
        if "cashback" in text_lower:
            reward_type = "cashback"
        elif "miles" in text_lower:
            reward_type = "miles"

        cap_data = self.detect_cap(text)
        result = {
            "category": category,
            "reward_type": reward_type,
            "reward_rate": self.normalize_reward_rate(text),
            "cap_amount": cap_data["cap_amount"],
            "cap_period": cap_data["cap_period"],
        }

        with open(OUTPUT_FILE, "w") as f:
            json.dump(result, f, indent=2)

        return result

    def run(self):
        """Run a minimal standalone extraction demo."""
        sample = "5% cashback on Amazon up to 1000 per month"
        return self.extract_benefits(sample)


def extract_benefits(text: str):
    return BenefitExtractorWorker().extract_benefits(text)


def normalize_reward_rate(text: str):
    return BenefitExtractorWorker().normalize_reward_rate(text)


def detect_cap(text: str):
    return BenefitExtractorWorker().detect_cap(text)


if __name__ == "__main__":
    worker = BenefitExtractorWorker()
    print(json.dumps(worker.run(), indent=2))
