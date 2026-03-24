"""
Card Template Generator
Ensures schema-compliant card JSON every time
"""

import json
import sys
from datetime import date


def generate_card(
    card_id: str,
    card_name: str,
    issuer: str,
    tier: str,
    reward_type: str,
    networks=None
):
    networks = networks or ["Visa"]

    card = {
        "card_id": card_id,
        "card_name": card_name,
        "issuer": issuer,
        "network": networks,
        "tier": tier,
        "reward_type": reward_type,
        "fees": {
            "joining_fee": 0,
            "annual_fee": 0
        },
        "earn_rules": [],
        "constraints": {},
        "meta": {
            "last_verified": str(date.today()),
            "source": "manual_entry"
        }
    }

    return card


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python card_template.py <card_id> <card_name> <issuer> <tier> <reward_type>")
        sys.exit(1)

    card = generate_card(
        card_id=sys.argv[1],
        card_name=sys.argv[2],
        issuer=sys.argv[3],
        tier=sys.argv[4],
        reward_type=sys.argv[5] if len(sys.argv) > 5 else "cashback"
    )

    print(json.dumps(card, indent=2))
