"""Canonical card schema contract for stable engine and data pipeline usage."""

CARD_SCHEMA = {
    "card_id": str,
    "card_name": str,
    "bank": str,
    "annual_fee": float,
    "reward_rates": dict,
    "benefits": dict,
    "milestone_bonus": list,
    "confidence": float,
}

# Backward-compatible schema constants used by legacy validators.
# Keep these until all validation paths are migrated to CARD_SCHEMA.
REQUIRED_CARD_FIELDS = {
    "card_id": str,
    "card_name": str,
    "bank": str,
    "fees": dict,
    "earn_rules": list,
}

REQUIRED_FEES_FIELDS = {
    "joining_fee": (int, float),
    "annual_fee": (int, float),
}

REQUIRED_EARN_RULE_FIELDS = {
    "category": str,
    "rate": (int, float),
}

OPTIONAL_CARD_FIELDS = {
    "benefits": dict,
    "milestone_bonus": list,
    "confidence": (int, float),
}
