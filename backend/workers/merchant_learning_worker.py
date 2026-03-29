import json
import os
from typing import Dict, Optional


CATEGORIES_FILE = "backend/data/categories.json"


def _load_data():
    if not os.path.exists(CATEGORIES_FILE):
        return {"version": 1, "categories": {}, "merchant_mappings": {}}

    with open(CATEGORIES_FILE, "r") as f:
        return json.load(f)


def _save_data(data):
    with open(CATEGORIES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _normalize(name: str) -> str:
    return name.strip().lower()


def learn_mapping(merchant: str, category: str) -> Dict[str, str]:
    data = _load_data()

    if "merchant_mappings" not in data:
        data["merchant_mappings"] = {}

    merchant_key = _normalize(merchant)
    data["merchant_mappings"][merchant_key] = category

    _save_data(data)

    return {merchant_key: category}


def get_category(merchant: str) -> Optional[str]:
    data = _load_data()

    merchant_key = _normalize(merchant)

    return data.get("merchant_mappings", {}).get(merchant_key)
