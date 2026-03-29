"""Shared response formatter for optimizer/compare endpoints."""

from __future__ import annotations

from typing import Any, Dict, List


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def format_top_cards(cards: List[Dict[str, Any]], optimizer_confidence: float | None = None) -> Dict[str, Any]:
    formatted: List[Dict[str, Any]] = []

    for c in cards:
        formatted.append(
            {
                "card_id": c.get("card_id"),
                "card_name": c.get("card_name"),
                "monthly_reward": round(_to_float(c.get("monthly_reward", 0.0), 0.0), 2),
                "yearly_reward": round(_to_float(c.get("yearly_reward", 0.0), 0.0), 2),
                "confidence": round(_to_float(c.get("confidence", c.get("confidence_score", 0.8)), 0.8), 3),
                "reason": c.get("reason", ""),
                "benefit_score": round(_to_float(c.get("benefit_score", 0.0), 0.0), 2),
                "reward_breakdown": c.get("reward_breakdown", {}),
            }
        )

    if optimizer_confidence is None:
        if formatted:
            optimizer_confidence = sum(card["confidence"] for card in formatted) / len(formatted)
        else:
            optimizer_confidence = 0.0

    return {
        "top_cards": formatted,
        "optimizer_confidence": round(max(0.0, min(1.0, _to_float(optimizer_confidence, 0.0))), 3),
    }
