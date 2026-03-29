"""
Worker: Merchant Learning Engine

Goal:
Learn merchant category automatically from transactions.

Input:
- merchant_name
- category

Store mapping inside:
- backend/data/categories.json

Functions:
- learn_mapping(merchant, category)
- get_category(merchant)

The worker updates JSON without overwriting existing mappings.
"""

import json
import os
from typing import Any, Dict, Optional


class MerchantLearningWorker:
    """Learns and retrieves merchant to category mappings."""

    def __init__(self, categories_file: str = "backend/data/categories.json") -> None:
        self.categories_file = categories_file

    def learn_mapping(self, merchant: str, category: str) -> Dict[str, str]:
        """
        Learn or update a merchant to category mapping.

        Existing category definitions and previously learned mappings are preserved.
        """
        merchant_key = self._normalize_merchant(merchant)
        category_value = str(category).strip()

        if not merchant_key:
            raise ValueError("merchant must be a non-empty string")
        if not category_value:
            raise ValueError("category must be a non-empty string")

        data = self._load_categories_data()
        mappings = data.get("merchant_mappings")

        if not isinstance(mappings, dict):
            mappings = {}

        mappings[merchant_key] = category_value
        data["merchant_mappings"] = mappings

        self._save_categories_data(data)

        return {"merchant": merchant_key, "category": category_value}

    def get_category(self, merchant: str) -> Optional[str]:
        """Get learned category for a merchant, if available."""
        merchant_key = self._normalize_merchant(merchant)
        if not merchant_key:
            return None

        data = self._load_categories_data()
        mappings = data.get("merchant_mappings", {})

        if not isinstance(mappings, dict):
            return None

        return mappings.get(merchant_key)

    def _load_categories_data(self) -> Dict[str, Any]:
        if not os.path.exists(self.categories_file):
            raise FileNotFoundError(
                f"categories file not found: {self.categories_file}"
            )

        with open(self.categories_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_categories_data(self, data: Dict[str, Any]) -> None:
        with open(self.categories_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def _normalize_merchant(merchant: str) -> str:
        return str(merchant).strip().lower()


worker = MerchantLearningWorker()


def learn_mapping(merchant: str, category: str) -> Dict[str, str]:
    """Convenience function: learn merchant->category mapping."""
    return worker.learn_mapping(merchant, category)


def get_category(merchant: str) -> Optional[str]:
    """Convenience function: fetch learned category for merchant."""
    return worker.get_category(merchant)
