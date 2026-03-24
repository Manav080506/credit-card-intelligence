from itertools import combinations

from backend.engine.card_registry import CARDS
from backend.engine.wallet_optimizer import optimize_wallet


def find_best_combo(
    monthly_spend: dict,
    max_cards: int = 3
):

    all_cards = list(CARDS.keys())

    best_combo = None
    best_value = 0
    best_result = None

    for r in range(1, max_cards + 1):

        for combo in combinations(all_cards, r):

            result = optimize_wallet(
                card_ids=list(combo),
                monthly_spend=monthly_spend
            )

            value = result["net_yearly_value"]

            if value > best_value:

                best_value = value

                best_combo = combo

                best_result = result


    return {

        "recommended_cards": list(best_combo),

        "expected_yearly_value": best_value,

        "wallet_score": best_result["wallet_score"],

        "details": best_result

    }
