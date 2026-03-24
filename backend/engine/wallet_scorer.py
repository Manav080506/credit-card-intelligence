IMPORTANT_CATEGORIES = [
    "online_shopping",
    "travel",
    "dining",
    "groceries",
    "fuel",
    "others"
]


def score_wallet(
    best_per_category: dict,
    yearly_fee_total: float,
    net_yearly_value: float
):

    # --- reward score (40 max) ---
    reward_score = min(net_yearly_value / 20000, 1) * 40


    # --- coverage score (25 max) ---
    covered_categories = len([
        c for c in best_per_category.values()
        if c["card_id"] is not None
    ])

    coverage_score = (
        covered_categories / len(IMPORTANT_CATEGORIES)
    ) * 25


    # --- diversification score (15 max) ---
    unique_cards = len(set([
        c["card_id"]
        for c in best_per_category.values()
        if c["card_id"]
    ]))

    diversification_score = min(unique_cards / 3, 1) * 15


    # --- fee efficiency score (20 max) ---
    if yearly_fee_total == 0:
        fee_score = 20

    elif yearly_fee_total < 2000:
        fee_score = 15

    elif yearly_fee_total < 5000:
        fee_score = 8

    else:
        fee_score = 3


    total_score = (
        reward_score
        + coverage_score
        + diversification_score
        + fee_score
    )


    return {

        "wallet_score": round(total_score, 1),

        "score_breakdown": {

            "reward_score": round(reward_score, 1),

            "coverage_score": round(coverage_score, 1),

            "diversification_score": round(diversification_score, 1),

            "fee_score": round(fee_score, 1)

        }

    }
