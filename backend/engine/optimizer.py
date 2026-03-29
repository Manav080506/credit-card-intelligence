import json
import hashlib
from pathlib import Path
from typing import Dict, List

from backend.core.config import CACHE_TTL_SECONDS
from backend.core.cache import cache_get, cache_set
from backend.engine.compare_optimizer import compare_cards as compare_cards_for_response
from backend.engine.card_comparison_evaluator import compare_cards as deterministic_compare_cards
from backend.engine.response_formatter import format_top_cards


DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
SOURCE_DATA_FILE = DATA_DIR / 'credit_cards_india_50.json'
OPTIMIZER_LAYER_FILE = DATA_DIR / 'cards_optimizer_layer.json'
METADATA_LAYER_FILE = DATA_DIR / 'cards_metadata_layer.json'


def _load_json_or_default(file_path: Path, default_value):
    if not file_path.exists():
        return default_value
    with file_path.open('r', encoding='utf-8') as file:
        return json.load(file)


SOURCE_CARDS = _load_json_or_default(SOURCE_DATA_FILE, [])
OPTIMIZER_CARDS = _load_json_or_default(OPTIMIZER_LAYER_FILE, SOURCE_CARDS)
METADATA_CARDS = _load_json_or_default(METADATA_LAYER_FILE, [])

METADATA_BY_ID = {card.get('id'): card for card in METADATA_CARDS if card.get('id')}

SPEND_CATEGORIES = [
    'online_shopping',
    'dining',
    'travel',
    'groceries',
    'fuel',
    'utilities',
]


def _normalize_spend(spend: Dict[str, float]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for category in SPEND_CATEGORIES:
        normalized[category] = float(spend.get(category, 0) or 0)
    return normalized


def compare_cards(spend: Dict[str, float], cards: List[Dict] | None = None) -> List[Dict]:
    normalized_spend = _normalize_spend(spend)
    card_list = cards if cards is not None else OPTIMIZER_CARDS
    return deterministic_compare_cards(card_list, normalized_spend, limit=3)


def generate_ai_insight(spend: Dict[str, float]) -> List[str]:
    normalized_spend = _normalize_spend(spend)
    insights: List[str] = []

    if normalized_spend['utilities'] > 8000:
        insights.append('Utility heavy user detected')

    if normalized_spend['travel'] > 15000:
        insights.append('Travel reward optimization recommended')

    if normalized_spend['online_shopping'] > 10000:
        insights.append('High ecommerce usage pattern')

    if not insights:
        insights.append('Balanced spending profile detected')

    return insights


def _spend_cache_key(spend: Dict[str, float]) -> str:
    ordered_payload = {category: spend.get(category, 0) for category in SPEND_CATEGORIES}
    raw = json.dumps(ordered_payload, sort_keys=True)
    spend_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]
    return f'opt:{spend_hash}'


def optimize_spend(spend: Dict[str, float]) -> Dict:
    normalized_spend = _normalize_spend(spend)
    cache_key = _spend_cache_key(normalized_spend)

    try:
        cached = cache_get(cache_key)
        if cached:
            return cached
    except Exception:
        # Fail open if cache is unavailable.
        pass

    response = compare_cards_for_response(card_ids=None, sample_spend=normalized_spend)

    if 'top_cards' not in response:
        response = format_top_cards(compare_cards(normalized_spend, OPTIMIZER_CARDS))

    try:
        cache_set(cache_key, response, ttl=CACHE_TTL_SECONDS)
    except Exception:
        # Fail open if cache is unavailable.
        pass

    return response
