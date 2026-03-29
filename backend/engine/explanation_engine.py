from typing import Dict, List


def explain_recommendation(best_card: Dict, features: Dict[str, float]) -> Dict:
    reasons: List[str] = []
    codes: List[str] = []

    if features.get('online_ratio', 0) > 0.4:
        reasons.append('High online spend detected')
        codes.append('HIGH_ONLINE_RATIO')

    if features.get('travel_heavy'):
        reasons.append('Travel-heavy profile')
        codes.append('HIGH_TRAVEL_RATIO')

    travel_rate = (
        best_card.get('reward_model', {}).get('travel')
        if best_card.get('reward_model')
        else best_card.get('travel', 0)
    )
    if float(travel_rate or 0) > 0.04:
        reasons.append('Strong travel reward rate')
        codes.append('STRONG_TRAVEL_RATE')

    if not reasons:
        reasons.append('Balanced spending profile, optimized for blended rewards')
        codes.append('BALANCED_PROFILE')

    summary = ', '.join(reasons[:2])

    return {
        'insight_summary': summary,
        'reason_codes': codes,
        'reasons': reasons,
    }
