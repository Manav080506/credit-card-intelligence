"""Change history worker.

Tracks changes in card attributes over time and appends immutable history events.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


HISTORY_DIR = Path(__file__).resolve().parent.parent / "data" / "history"


def _history_file(card_id: str) -> Path:
    return HISTORY_DIR / f"{card_id}.json"


def detect_card_changes(old_card: Dict[str, Any], new_card: Dict[str, Any]) -> List[Dict[str, Any]]:
    changes: List[Dict[str, Any]] = []

    fields_to_check = [
        "annual_fee",
        "joining_fee",
        "reward_rates",
        "milestone_bonus",
        "lounge_access",
        "network",
    ]

    for field in fields_to_check:
        old_value = old_card.get(field)
        new_value = new_card.get(field)
        if old_value != new_value:
            changes.append(
                {
                    "field": field,
                    "old_value": old_value,
                    "new_value": new_value,
                }
            )

    return changes


def log_change(card_id: str, old_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    changes = detect_card_changes(old_data, new_data)

    entry = {
        "card": new_data.get("card_name") or card_id,
        "card_id": card_id,
        "change_date": datetime.utcnow().date().isoformat(),
        "timestamp": datetime.utcnow().isoformat(),
        "changes": changes,
    }

    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    path = _history_file(card_id)

    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    history.append(entry)

    with path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    return entry


def track_change(old_card: Dict[str, Any], new_card: Dict[str, Any]) -> List[Dict[str, Any]]:
    card_id = str(new_card.get("card_id") or new_card.get("id") or "unknown_card")
    event = log_change(card_id, old_card, new_card)
    return event.get("changes", [])
