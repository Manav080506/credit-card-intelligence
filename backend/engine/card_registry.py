from backend.engine.bootstrap import CARDS, CARD_ERRORS


def list_cards():
    return [
        {
            "card_id": card["card_id"],
            "card_name": card["card_name"],
            "issuer": card["issuer"],
            "reward_type": card.get("reward_type", "unknown")
        }
        for card in CARDS.values()
    ]


def registry_health():
    return {
        "loaded_cards": len(CARDS),
        "errors": CARD_ERRORS
    }
