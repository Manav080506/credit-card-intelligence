import json
import os
from datetime import datetime


HISTORY_DIR = "backend/data/history"


def _ensure_history_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def detect_card_changes(old_card: dict, new_card: dict):
    changes = []

    # reward type
    if old_card.get("reward_type") != new_card.get("reward_type"):
        changes.append({
            "field": "reward_type",
            "old_value": old_card.get("reward_type"),
            "new_value": new_card.get("reward_type")
        })

    # annual fee
    old_fee = old_card.get("fees", {}).get("annual_fee")
    new_fee = new_card.get("fees", {}).get("annual_fee")

    if old_fee != new_fee:
        changes.append({
            "field": "fees.annual_fee",
            "old_value": old_fee,
            "new_value": new_fee
        })

    # reward rate
    old_rate = None
    new_rate = None

    if old_card.get("earn_rules"):
        old_rate = old_card["earn_rules"][0].get("reward_rate")

    if new_card.get("earn_rules"):
        new_rate = new_card["earn_rules"][0].get("reward_rate")

    if old_rate != new_rate:
        changes.append({
            "field": "earn_rules.reward_rate",
            "old_value": old_rate,
            "new_value": new_rate
        })

    return changes


def track_change(old_card, new_card):

    changes = detect_card_changes(old_card, new_card)

    if not changes:
        return []

    _ensure_history_dir()

    entry = {
        "card_id": new_card["card_id"],
        "timestamp": datetime.utcnow().isoformat(),
        "changes": changes
    }

    path = f"{HISTORY_DIR}/{new_card['card_id']}.json"

    if os.path.exists(path):

        with open(path, "r") as f:
            history = json.load(f)

    else:
        history = []

    history.append(entry)

    with open(path, "w") as f:
        json.dump(history, f, indent=2)

    return changes
