import json
from pathlib import Path
from typing import Dict, List, Tuple


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

CATEGORIES = (
    "online_shopping",
    "dining",
    "travel",
    "utilities",
    "groceries",
    "fuel",
)


def _normalize_spend(spend_profile: Dict[str, float]) -> Dict[str, float]:
    return {key: float(spend_profile.get(key, 0) or 0) for key in CATEGORIES}


def _humanize_category(category: str) -> str:
    return category.replace("_", " ")


def _get_reward_rate(card: Dict, category: str) -> float:
    direct_rate = card.get(category)
    if direct_rate is not None:
        return float(direct_rate or 0)

    reward_rates = card.get("reward_rates", {})
    if isinstance(reward_rates, dict):
        return float(reward_rates.get(category, 0) or 0)

    return 0.0


def _milestone_bonus(card: Dict, metadata: Dict, yearly_spend: float) -> Tuple[float, bool]:
    milestone = metadata.get("milestone_bonus", card.get("milestone_bonus", {}))

    if isinstance(milestone, dict):
        threshold = float(milestone.get("threshold", milestone.get("spend_threshold", 0)) or 0)
        bonus = float(milestone.get("bonus", milestone.get("amount", 0)) or 0)
    elif isinstance(milestone, (int, float)):
        threshold = float(metadata.get("milestone_threshold", 120000) or 120000)
        bonus = float(milestone or 0)
    else:
        threshold = 0.0
        bonus = 0.0

    if threshold > 0 and yearly_spend >= threshold and bonus > 0:
        return bonus, True

    return 0.0, False


def _confidence(
    spend_profile: Dict[str, float],
    card: Dict,
    category_breakdown: Dict[str, float],
    all_cards: List[Dict],
    data_quality: float,
) -> Tuple[float, str]:
    total_categories = len(CATEGORIES)
    active_categories = [key for key in CATEGORIES if spend_profile.get(key, 0) > 0]

    coverage_score = len(active_categories) / total_categories if total_categories else 0.0

    if active_categories:
        category_match_values = []
        for key in active_categories:
            max_rate = max(_get_reward_rate(c, key) for c in all_cards) if all_cards else 0.0
            current_rate = _get_reward_rate(card, key)
            category_match_values.append(current_rate / max(max_rate, 1e-9))
        category_match = sum(category_match_values) / len(category_match_values)
    else:
        category_match = 0.0

    contributions = [float(category_breakdown.get(key, 0) or 0) for key in active_categories]
    total_contribution = sum(contributions)
    if total_contribution > 0 and len(contributions) > 1:
        shares = [value / total_contribution for value in contributions]
        concentration = sum(share * share for share in shares)
        min_concentration = 1 / len(shares)
        reward_stability = 1 - ((concentration - min_concentration) / max(1 - min_concentration, 1e-9))
        reward_stability = max(0.0, min(1.0, reward_stability))
    elif total_contribution > 0:
        reward_stability = 0.6
    else:
        reward_stability = 0.0

    confidence = (
        0.35 * coverage_score
        + 0.25 * data_quality
        + 0.25 * category_match
        + 0.15 * reward_stability
    )
    confidence = round(max(0.0, min(1.0, confidence)), 2)

    if confidence > 0.85:
        label = "high"
    elif confidence >= 0.65:
        label = "good"
    else:
        label = "low"

    return confidence, label


def generate_card_reason(card, reward_breakdown, yearly_reward) -> str:
    sorted_categories = sorted(reward_breakdown.items(), key=lambda item: item[1], reverse=True)
    top_categories = [name for name, amount in sorted_categories if amount > 0][:2]
    if len(top_categories) < 2:
        top_categories = (top_categories + ["balanced spending", "everyday spend"])[:2]

    annual_fee = float(card.get("annual_fee", 0) or 0)
    fee_phrase = "Low fee edge." if annual_fee <= 1000 else "High fee drag."

    milestone_applied = bool(card.get("milestone_applied", False))
    milestone_phrase = "Milestone bonus applied." if milestone_applied else "No milestone bonus."

    reason = (
        f"Best for {_humanize_category(top_categories[0])} and {_humanize_category(top_categories[1])}. "
        f"{fee_phrase} {milestone_phrase}"
    )

    words = reason.split()
    if len(words) > 25:
        reason = " ".join(words[:25])
    return reason


def rank_top_cards(
    spend_profile: Dict[str, float],
    cards: List[Dict],
    metadata_by_id: Dict[str, Dict] | None = None,
    limit: int = 3,
) -> List[Dict]:
    normalized = _normalize_spend(spend_profile)
    metadata = metadata_by_id or {}
    yearly_spend_total = sum(normalized.values()) * 12

    ranked: List[Dict] = []
    for card in cards:
        card_id = card.get("id") or card.get("card_id")
        if not card_id:
            continue

        category_breakdown = {}
        for category in CATEGORIES:
            category_breakdown[category] = round(normalized[category] * _get_reward_rate(card, category), 2)

        monthly_reward = round(sum(category_breakdown.values()), 2)
        yearly_reward_raw = monthly_reward * 12

        card_meta = metadata.get(card_id, {})
        annual_fee = float(card_meta.get("annual_fee", 0) or 0)
        data_quality = float(card_meta.get("data_reliability", card.get("data_reliability", 0)) or 0)
        if data_quality <= 0:
            data_quality = float(card.get("rating", 3.5) or 3.5) / 5
        data_quality = max(0.0, min(1.0, data_quality))

        milestone_bonus, milestone_applied = _milestone_bonus(card, card_meta, yearly_spend_total)

        yearly_reward = round(yearly_reward_raw - annual_fee + milestone_bonus, 2)
        confidence, confidence_label = _confidence(
            spend_profile=normalized,
            card=card,
            category_breakdown=category_breakdown,
            all_cards=cards,
            data_quality=data_quality,
        )

        reason_payload = {
            "annual_fee": annual_fee,
            "milestone_applied": milestone_applied,
        }
        reason = generate_card_reason(reason_payload, category_breakdown, yearly_reward)

        ranked.append(
            {
                "card_id": card_id,
                "card_name": card.get("name") or card.get("display_name") or card_id,
                "monthly_reward": monthly_reward,
                "yearly_reward": yearly_reward,
                "annual_fee": annual_fee,
                "milestone_bonus": milestone_bonus,
                "confidence": confidence,
                "confidence_label": confidence_label,
                "category_breakdown": category_breakdown,
                "reason": reason,
                "lounge_access": bool(card_meta.get("lounge_access", False)),
                "forex_markup": float(card_meta.get("forex_markup", 0) or 0),
                "data_quality": round(data_quality, 2),
            }
        )

    ranked.sort(key=lambda row: (row["yearly_reward"], row["card_id"]), reverse=True)
    return ranked[: max(1, limit)]


def compare_cards(card_ids=None, spend_profile=None, cards=None, metadata_by_id=None, monthly_spend=None):
    if spend_profile is None:
        spend_profile = monthly_spend or {}
    if card_ids is None:
        card_ids = cards or []

    provided_card_objects = None
    if isinstance(cards, list) and (len(cards) == 0 or isinstance(cards[0], dict)):
        provided_card_objects = cards

    card_set = provided_card_objects if provided_card_objects is not None else OPTIMIZER_CARDS
    metadata = metadata_by_id if metadata_by_id is not None else METADATA_BY_ID

    selected = [card for card in card_set if card.get("id") in set(card_ids)]
    ranked = rank_top_cards(spend_profile, selected, metadata_by_id=metadata, limit=len(selected) or 1)

    output = []
    for row in ranked:
        output.append(
            {
                "card_id": row["card_id"],
                "card_name": row["card_name"],
                "monthly_value": row["monthly_reward"],
                "breakdown": row["category_breakdown"],
                "yearly_value": row["yearly_reward"],
                "confidence": row["confidence"],
                "confidence_label": row["confidence_label"],
                "reason": row["reason"],
            }
        )

    return output
