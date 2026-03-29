from typing import Dict, List

from backend.engine.explanation_engine import explain_recommendation
from backend.engine.feature_engineering import build_features
from backend.engine.normalizer import normalize_reward, normalize_spend


def rank_cards(spend: Dict[str, float], cards: List[Dict]) -> List[Dict]:
    normalized_spend = normalize_spend(spend)
    results = []

    for card in cards:
        reward = normalize_reward(card, normalized_spend)
        results.append({
            'card_id': card.get('id'),
            'card': card.get('name') or card.get('display_name', 'Unknown Card'),
            'monthly_reward': reward,
            'yearly_reward': round(reward * 12, 2),
        })

    return sorted(results, key=lambda row: row['monthly_reward'], reverse=True)


def recommend_with_explanation(spend: Dict[str, float], cards: List[Dict]) -> Dict:
    features = build_features(spend)
    ranked = rank_cards(spend, cards)

    if not ranked:
        return {
            'best_card': 'No matching card',
            'expected_monthly_reward': 0,
            'expected_yearly_reward': 0,
            'comparison': [],
            'features': features,
            'explanation': {
                'insight_summary': 'No cards available for recommendation',
                'reason_codes': ['NO_DATA'],
                'reasons': ['No cards available for recommendation'],
            },
        }

    best = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None

    best_card_details = next((card for card in cards if card.get('id') == best.get('card_id')), {})
    explanation = explain_recommendation(best_card_details, features)

    confidence = 0.62
    filled = sum(1 for key in ('online_ratio', 'dining_ratio', 'travel_ratio', 'utility_ratio') if features.get(key, 0) > 0)
    if filled >= 3:
        confidence = 0.84
    elif filled == 2:
        confidence = 0.75

    baseline = features['total_spend'] * 0.01
    optimization = max(0.0, min(0.99, (best['monthly_reward'] - baseline) / max(best['monthly_reward'], 1e-9)))

    return {
        'best_card': best['card'],
        'expected_monthly_reward': best['monthly_reward'],
        'expected_yearly_reward': best['yearly_reward'],
        'second_best_card': second['card'] if second else '',
        'confidence_score': round(confidence, 2),
        'optimization_score': round(optimization, 2),
        'comparison': ranked[:10],
        'features': features,
        'explanation': explanation,
    }
