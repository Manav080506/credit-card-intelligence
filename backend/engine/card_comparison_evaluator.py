"""Deterministic card comparison evaluator.

Used by optimizer and dashboard modal to rank cards by yearly value.
"""

from __future__ import annotations

from typing import Dict, List, Any


SPEND_CATEGORIES = [
    "online_shopping",
    "dining",
    "travel",
    "groceries",
    "fuel",
    "utilities",
]

RATE_CATEGORIES = SPEND_CATEGORIES + [
    "general",
]


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_monthly_spend(monthly_spend: Dict[str, Any]) -> Dict[str, float]:
    spend = monthly_spend or {}
    normalized = {category: _to_float(spend.get(category, 0.0), 0.0) for category in SPEND_CATEGORIES}
    for category in normalized:
        if normalized[category] < 0:
            normalized[category] = 0.0
    return normalized


def _normalize_card(card: Dict[str, Any]) -> Dict[str, Any]:
    """Support both legacy optimizer cards and normalized reward schema cards."""
    reward_rates = card.get("reward_rates")
    if isinstance(reward_rates, dict):
        rates = {category: _to_float(reward_rates.get(category, 0.0), 0.0) for category in RATE_CATEGORIES}
    else:
        rates = {category: _to_float(card.get(category, 0.0), 0.0) for category in RATE_CATEGORIES}

    benefits = card.get("benefits", {}) if isinstance(card.get("benefits"), dict) else {}

    normalized = {
        "card_id": card.get("card_id") or card.get("id") or "unknown_card",
        "card_name": card.get("card_name") or card.get("name") or "Unknown Card",
        "annual_fee": _to_float(card.get("annual_fee", 0.0), 0.0),
        "reward_rates": rates,
        "milestone_bonus": card.get("milestone_bonus", []),
        "benefits": {
            "lounge_access": int(_to_float(benefits.get("lounge_access", 0), 0)),
            "fuel_surcharge_waiver": bool(benefits.get("fuel_surcharge_waiver", False)),
            "forex_markup": _to_float(benefits.get("forex_markup", 3.5), 3.5),
        },
        "confidence": _to_float(card.get("confidence", card.get("rating", 0.8)), 0.8),
    }
    return normalized


def _yearly_reward(spend: Dict[str, float], rates: Dict[str, float]) -> float:
    total = 0.0
    for category in SPEND_CATEGORIES:
        rate = _to_float(rates.get(category, rates.get("general", 0.0)), 0.0)
        total += spend[category] * rate * 12.0
    return total


def _reward_breakdown(spend: Dict[str, float], rates: Dict[str, float]) -> Dict[str, float]:
    breakdown: Dict[str, float] = {}
    for category in SPEND_CATEGORIES:
        rate = _to_float(rates.get(category, rates.get("general", 0.0)), 0.0)
        yearly_value = spend[category] * rate * 12.0
        if yearly_value > 0:
            breakdown[category] = round(yearly_value, 2)
    return breakdown


def _milestone_bonus(card: Dict[str, Any], yearly_spend: float) -> float:
    milestones = card.get("milestone_bonus", [])
    if not isinstance(milestones, list):
        return 0.0

    bonus = 0.0
    for milestone in milestones:
        if not isinstance(milestone, dict):
            continue
        threshold = _to_float(milestone.get("spend_threshold", 0.0), 0.0)
        value = _to_float(milestone.get("bonus_value", 0.0), 0.0)
        if yearly_spend >= threshold:
            bonus += value
    return bonus


def _benefit_score(card: Dict[str, Any]) -> float:
    benefits = card.get("benefits", {})
    lounge_score = int(_to_float(benefits.get("lounge_access", 0), 0)) * 120.0
    fuel_score = 150.0 if bool(benefits.get("fuel_surcharge_waiver", False)) else 0.0

    forex_markup = _to_float(benefits.get("forex_markup", 3.5), 3.5)
    if forex_markup <= 1.0:
        forex_score = 220.0
    elif forex_markup <= 2.0:
        forex_score = 120.0
    elif forex_markup <= 2.5:
        forex_score = 60.0
    else:
        forex_score = 0.0

    return lounge_score + fuel_score + forex_score


def _confidence_score(card: Dict[str, Any], spend: Dict[str, float]) -> float:
    active_categories = [c for c in SPEND_CATEGORIES if spend[c] > 0]
    if not active_categories:
        return 0.0

    rates = card.get("reward_rates", {})
    covered = sum(1 for c in active_categories if _to_float(rates.get(c, 0.0), 0.0) > 0)
    coverage_score = covered / len(active_categories)

    confidence = _to_float(card.get("confidence", 0.8), 0.8)
    reward_stability = max(0.0, min(1.0, confidence))

    spend_total = sum(spend.values())
    weighted_match = 0.0
    if spend_total > 0:
        for category in active_categories:
            weighted_match += (spend[category] / spend_total) * _to_float(rates.get(category, 0.0), 0.0)
    category_match = min(1.0, weighted_match / 0.05)  # 5% is treated as excellent match

    score = (coverage_score * 0.4) + (reward_stability * 0.3) + (category_match * 0.3)
    return round(max(0.0, min(1.0, score)), 3)


def _reason(card: Dict[str, Any], spend: Dict[str, float]) -> str:
    rates = card.get("reward_rates", {})
    top_spend = sorted(SPEND_CATEGORIES, key=lambda c: spend[c], reverse=True)
    top_spend = [c for c in top_spend if spend[c] > 0][:2]

    if not top_spend:
        return "Balanced profile fit with steady rewards and simple fee structure"

    highlighted = sorted(top_spend, key=lambda c: _to_float(rates.get(c, 0.0), 0.0), reverse=True)
    parts = [f"Strong in {highlighted[0].replace('_', ' ')}"]
    if len(highlighted) > 1:
        parts.append(f"and {highlighted[1].replace('_', ' ')}")

    fee = _to_float(card.get("annual_fee", 0.0), 0.0)
    if fee <= 1000:
        parts.append("with manageable annual fee")
    else:
        parts.append("with premium benefits value")

    sentence = " ".join(parts)
    words = sentence.split()
    if len(words) <= 25:
        return sentence
    return " ".join(words[:25])


def compare_cards(
    cards: List[Dict[str, Any]],
    monthly_spend: Dict[str, Any],
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Compare cards and return top 3 by ranking score.

    Ranking formula:
    - yearly_reward = sum(monthly_spend[category] * reward_rate * 12) - annual_fee + milestone_bonus
    - benefit_score from lounge/fuel/forex benefits
    - confidence_score from coverage, stability, category match
    """
    normalized_spend = _normalize_monthly_spend(monthly_spend)
    yearly_spend_total = sum(normalized_spend.values()) * 12.0

    ranked: List[Dict[str, Any]] = []
    for raw_card in cards or []:
        card = _normalize_card(raw_card)

        gross_yearly_reward = _yearly_reward(normalized_spend, card["reward_rates"])
        milestone_bonus = _milestone_bonus(card, yearly_spend_total)
        yearly_reward = gross_yearly_reward - card["annual_fee"] + milestone_bonus
        monthly_reward = yearly_reward / 12.0
        reward_breakdown = _reward_breakdown(normalized_spend, card["reward_rates"])

        benefit_score = _benefit_score(card)
        confidence = _confidence_score(card, normalized_spend)

        ranking_score = yearly_reward + (0.15 * benefit_score) + (400.0 * confidence)

        ranked.append(
            {
                "card_id": card["card_id"],
                "card_name": card["card_name"],
                "yearly_reward": round(yearly_reward, 2),
                "monthly_reward": round(monthly_reward, 2),
                "confidence": confidence,
                "benefit_score": round(benefit_score, 2),
                "reason": _reason(card, normalized_spend),
                "reward_breakdown": reward_breakdown,
                "ranking_score": round(ranking_score, 2),
            }
        )

    ranked.sort(key=lambda row: row["ranking_score"], reverse=True)
    return ranked[: max(1, limit)]
