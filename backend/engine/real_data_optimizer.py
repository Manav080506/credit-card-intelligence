import json
from pathlib import Path
from typing import Dict, List, Tuple


DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'credit_cards_india.json'
CATEGORIES = ('online_shopping', 'dining', 'travel', 'utilities')


def _load_cards() -> List[Dict]:
    with DATA_PATH.open('r', encoding='utf-8') as file:
        return json.load(file)


def _normalize_spend(payload: Dict) -> Dict[str, float]:
    return {
        category: max(0.0, float(payload.get(category, 0) or 0))
        for category in CATEGORIES
    }


def _card_monthly_reward(card: Dict, spend: Dict[str, float]) -> float:
    rates = card.get('reward_rates', {})
    reward = 0.0
    for category in CATEGORIES:
        reward += spend[category] * float(rates.get(category, 0) or 0)

    cap = card.get('reward_cap')
    if cap is not None:
        reward = min(reward, float(cap))

    return round(reward, 2)


def _rank_cards(cards: List[Dict], spend: Dict[str, float]) -> List[Tuple[Dict, float]]:
    ranked = [(card, _card_monthly_reward(card, spend)) for card in cards]
    ranked.sort(key=lambda item: (item[1], float(item[0].get('rating', 0) or 0)), reverse=True)
    return ranked


def _build_category_breakdown(cards: List[Dict], spend: Dict[str, float]) -> Dict[str, Dict]:
    breakdown: Dict[str, Dict] = {}

    for category in CATEGORIES:
        best_card_name = ''
        best_reward = 0.0

        for card in cards:
            rate = float(card.get('reward_rates', {}).get(category, 0) or 0)
            reward = spend[category] * rate
            if reward > best_reward:
                best_reward = reward
                best_card_name = card.get('name', '')

        breakdown[category] = {
            'best_card': best_card_name,
            'estimated_reward': round(best_reward, 2),
            'spend': round(spend[category], 2),
        }

    return breakdown


def _confidence_score(spend: Dict[str, float], ranked: List[Tuple[Dict, float]]) -> float:
    filled = sum(1 for value in spend.values() if value > 0)
    base = min(0.95, 0.35 + 0.18 * filled)

    if len(ranked) >= 2 and ranked[0][1] > 0:
        margin = (ranked[0][1] - ranked[1][1]) / max(ranked[0][1], 1e-9)
        base += min(0.12, max(0.0, margin))

    return round(max(0.1, min(0.98, base)), 2)


def _optimization_score(spend: Dict[str, float], best_monthly_reward: float) -> float:
    total_spend = sum(spend.values())
    if total_spend <= 0:
        return 0.0

    baseline = total_spend * 0.01
    gain = max(0.0, best_monthly_reward - baseline)
    score = gain / max(best_monthly_reward, 1e-9)
    return round(max(0.0, min(0.99, score)), 2)


def optimize_spend_with_real_data(payload: Dict) -> Dict:
    spend = _normalize_spend(payload)
    cards = _load_cards()
    ranked = _rank_cards(cards, spend)

    if not ranked:
        return {
            'best_card': 'No cards available',
            'expected_monthly_reward': 0,
            'expected_yearly_reward': 0,
            'second_best_card': '',
            'confidence_score': 0,
            'optimization_score': 0,
            'insights': ['No cards loaded in dataset'],
            'opportunities': [],
            'category_breakdown': {},
        }

    best_card, best_monthly_reward = ranked[0]
    second_best_name = ranked[1][0].get('name', '') if len(ranked) > 1 else ''
    expected_yearly_reward = round(best_monthly_reward * 12, 2)
    confidence_score = _confidence_score(spend, ranked)
    optimization_score = _optimization_score(spend, best_monthly_reward)

    category_breakdown = _build_category_breakdown(cards, spend)

    utility_spend = spend.get('utilities', 0)
    online_spend = spend.get('online_shopping', 0)
    travel_spend = spend.get('travel', 0)

    insights: List[str] = []
    if utility_spend > 0:
        insights.append('Utilities under-optimized' if category_breakdown['utilities']['best_card'] != best_card.get('name') else 'Utilities optimized on current recommendation')
    if online_spend >= max(spend.values() or [0]):
        insights.append('High online shopping detected')
    if travel_spend > 0 and travel_spend >= (sum(spend.values()) * 0.25):
        insights.append('Travel heavy profile')
    if not insights:
        insights.append('Balanced spending profile detected')

    opportunities = [
        f"Switch utilities to {category_breakdown['utilities']['best_card']}" if category_breakdown['utilities']['best_card'] else 'Review utility category strategy',
        f"Use {category_breakdown['dining']['best_card']} for dining" if category_breakdown['dining']['best_card'] else 'Review dining category strategy',
    ]

    return {
        'best_card': best_card.get('name', ''),
        'expected_monthly_reward': round(best_monthly_reward, 2),
        'expected_yearly_reward': expected_yearly_reward,
        'second_best_card': second_best_name,
        'confidence_score': confidence_score,
        'optimization_score': optimization_score,
        'insights': insights,
        'opportunities': opportunities,
        'category_breakdown': category_breakdown,
    }
