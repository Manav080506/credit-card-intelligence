# === AUTHORITATIVE CARD SCHEMA ===

REQUIRED_CARD_FIELDS = {
    "card_id": str,
    "card_name": str,
    "issuer": str,
    "network": list,
    "tier": str,
    "reward_type": str,
    "fees": dict,
    "earn_rules": list,
    "constraints": dict,
    "meta": dict
}

REQUIRED_FEES_FIELDS = {
    "joining_fee": (int, float),
    "annual_fee": (int, float)
}

REQUIRED_EARN_RULE_FIELDS = {
    "category": str,
    "reward_rate": (int, float),
    "reward_unit": str
}

OPTIONAL_CARD_FIELDS = {
    "redemption_rules": list
}
