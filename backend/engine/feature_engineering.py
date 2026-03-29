import math
from typing import Dict

from backend.engine.normalizer import normalize_spend


def calculate_entropy(spend: Dict[str, float]) -> float:
    total = sum(spend.values())
    if total <= 0:
        return 0.0

    entropy = 0.0
    for amount in spend.values():
        if amount <= 0:
            continue
        probability = amount / total
        entropy -= probability * math.log(probability)

    return round(entropy, 4)


def build_features(spend: Dict[str, float]) -> Dict[str, float]:
    normalized = normalize_spend(spend)
    total = max(1.0, sum(normalized.values()))

    return {
        'online_ratio': normalized['online_shopping'] / total,
        'dining_ratio': normalized['dining'] / total,
        'travel_ratio': normalized['travel'] / total,
        'utility_ratio': normalized['utilities'] / total,
        'spend_entropy': calculate_entropy(normalized),
        'premium_affinity': 1 if total > 50000 else 0,
        'travel_heavy': 1 if normalized['travel'] > 15000 else 0,
        'total_spend': total,
    }
