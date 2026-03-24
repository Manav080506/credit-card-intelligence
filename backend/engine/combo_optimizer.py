from itertools import combinations

from backend.engine.wallet_optimizer import optimize_wallet


def find_best_2_card_combo(all_card_ids, monthly_spend):

    results = []

    for combo in combinations(all_card_ids, 2):

        optimization = optimize_wallet(
            card_ids=list(combo),
            monthly_spend=monthly_spend
        )

        results.append({

            "combo": combo,

            "net_yearly_value": optimization["net_yearly_value"],

            "details": optimization
        })


    results.sort(
        key=lambda x: x["net_yearly_value"],
        reverse=True
    )

    return {

        "best_combo": results[0],

        "top_5_combos": results[:5]

    }
