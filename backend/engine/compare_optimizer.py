import json
from pathlib import Path
from typing import Dict, List

from backend.engine.card_comparison_evaluator import compare_cards as deterministic_compare_cards
from backend.engine.response_formatter import format_top_cards


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OPTIMIZER_LAYER_FILE = DATA_DIR / "cards_optimizer_layer.json"
METADATA_LAYER_FILE = DATA_DIR / "cards_metadata_layer.json"


def _load_json_or_default(file_path: Path, default_value):
    if not file_path.exists():
        return default_value
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


OPTIMIZER_CARDS = _load_json_or_default(OPTIMIZER_LAYER_FILE, [])
METADATA_CARDS = _load_json_or_default(METADATA_LAYER_FILE, [])
METADATA_BY_ID = {card.get("id"): card for card in METADATA_CARDS if card.get("id")}


def _estimate_optimizer_confidence(sample_spend: Dict[str, float], top_cards: List[Dict]) -> float:
    if not top_cards:
        return 0.0

    active_categories = [k for k, v in (sample_spend or {}).items() if float(v or 0) > 0]
    if not active_categories:
        return 0.6

    winner_breakdown = top_cards[0].get("reward_breakdown", {})
    covered = sum(1 for category in active_categories if float(winner_breakdown.get(category, 0) or 0) > 0)
    coverage_score = covered / len(active_categories)
    return round(0.6 + (coverage_score * 0.4), 3)


def get_top_ranked_cards(sample_spend: Dict[str, float], limit: int = 3, card_ids: List[str] | None = None) -> List[Dict]:
    cards = OPTIMIZER_CARDS
    if card_ids:
        allowed = set(card_ids)
        cards = [card for card in OPTIMIZER_CARDS if card.get("id") in allowed]

    return deterministic_compare_cards(cards=cards, monthly_spend=sample_spend, limit=limit)


def compare_cards(card_ids, sample_spend):
    top_cards = get_top_ranked_cards(sample_spend=sample_spend, limit=max(3, len(card_ids or [])), card_ids=card_ids)
    optimizer_confidence = _estimate_optimizer_confidence(sample_spend, top_cards)
    return format_top_cards(top_cards, optimizer_confidence=optimizer_confidence)
