"""Trusted seed loader for initial stable card set.

Loads curated cards from cards_25_real.json and writes a small, reliable
5-card dataset to backend/data/cards/*.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SEED_SOURCE_FILE = DATA_DIR / "cards_25_real.json"
CARD_OUTPUT_DIR = DATA_DIR / "cards"

TRUSTED_CARD_IDS = [
    "hdfc_millennia",
    "axis_ace",
    "sbi_cashback",
    "icici_amazon_pay",
    "amex_mrcc",
]


def load_seed_cards() -> List[Dict]:
    with SEED_SOURCE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_trusted_seed_files() -> Dict[str, List[str]]:
    cards = load_seed_cards()
    card_map = {card.get("card_id"): card for card in cards if card.get("card_id")}

    CARD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    written_files: List[str] = []
    missing_ids: List[str] = []

    for card_id in TRUSTED_CARD_IDS:
        card = card_map.get(card_id)
        if not card:
            missing_ids.append(card_id)
            continue

        output_file = CARD_OUTPUT_DIR / f"{card_id}.json"
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(card, file, indent=2)
        written_files.append(str(output_file))

    return {
        "written_files": written_files,
        "missing_ids": missing_ids,
    }
