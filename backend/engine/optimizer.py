import json
import hashlib
from pathlib import Path
from typing import Dict, List

from backend.core.config import CACHE_TTL_SECONDS
from backend.core.cache import cache_get, cache_set
from backend.engine.recommendation_engine import rank_cards, recommend_with_explanation


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


def _normalize_spend(spend: Dict[str, float]) -> Dict[str, float]:
    return {
        'online_shopping': float(spend.get('online_shopping', 0) or 0),
        'dining': float(spend.get('dining', 0) or 0),
        'travel': float(spend.get('travel', 0) or 0),
        'utilities': float(spend.get('utilities', 0) or 0),
    }


def _card_reward(spend: Dict[str, float], card: Dict) -> float:
    return (
        spend['online_shopping'] * float(card.get('online_shopping', 0) or 0)
        + spend['dining'] * float(card.get('dining', 0) or 0)
        + spend['travel'] * float(card.get('travel', 0) or 0)
        + spend['utilities'] * float(card.get('utilities', 0) or 0)
    )


def compare_cards(spend: Dict[str, float], cards: List[Dict] | None = None) -> List[Dict]:
    normalized_spend = _normalize_spend(spend)
    card_set = cards if cards is not None else OPTIMIZER_CARDS
    return rank_cards(normalized_spend, card_set)


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


def _derive_optimization_score(spend: Dict[str, float], best_reward: float) -> float:
    total_spend = sum(spend.values())
    if total_spend <= 0:
        return 0.0
    baseline = total_spend * 0.01
    gain = max(0.0, best_reward - baseline)
    return round(max(0.0, min(0.99, gain / max(best_reward, 1e-9))), 2)


def _spend_cache_key(spend: Dict[str, float]) -> str:
    ordered_payload = {
        'online_shopping': spend.get('online_shopping', 0),
        'dining': spend.get('dining', 0),
        'travel': spend.get('travel', 0),
        'utilities': spend.get('utilities', 0),
    }
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

    recommendation = recommend_with_explanation(normalized_spend, OPTIMIZER_CARDS)

    best_card_id = recommendation.get('comparison', [{}])[0].get('card_id') if recommendation.get('comparison') else None
    best_card_metadata = METADATA_BY_ID.get(best_card_id, {})

    opportunities: List[str] = []
    ranked = recommendation.get('comparison', [])
    if len(ranked) > 1 and ranked[0]['monthly_reward'] > ranked[1]['monthly_reward']:
        yearly_diff = round((ranked[0]['monthly_reward'] - ranked[1]['monthly_reward']) * 12, 2)
        opportunities.append(f"Choosing {ranked[0]['card']} over {ranked[1]['card']} can add around INR {yearly_diff} yearly.")

    response = {
        'best_card': recommendation.get('best_card', 'No matching card'),
        'expected_monthly_reward': recommendation.get('expected_monthly_reward', 0),
        'expected_yearly_reward': recommendation.get('expected_yearly_reward', 0),
        'second_best_card': recommendation.get('second_best_card', ''),
        'confidence_score': recommendation.get('confidence_score', 0),
        'optimization_score': recommendation.get('optimization_score', 0),
        'insights': generate_ai_insight(normalized_spend),
        'opportunities': opportunities,
        'best_card_metadata': best_card_metadata,
        'comparison': recommendation.get('comparison', [])[:5],
        'explanation': recommendation.get('explanation', {}),
        'features': recommendation.get('features', {}),
    }

    try:
        cache_set(cache_key, response, ttl=CACHE_TTL_SECONDS)
    except Exception:
        # Fail open if cache is unavailable.
        pass

    return response
