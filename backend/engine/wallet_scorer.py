from backend.engine.bootstrap import CARDS


IMPORTANT_CATEGORIES = [
    "online_shopping",
    "travel",
    "dining",
    "groceries",
    "fuel",
    "others"
]


def calculate_wallet_score(
    optimization_result
):

    monthly_value = optimization_result["total_monthly_reward"]

    yearly_value = optimization_result["net_yearly_value"]

    best_cards = optimization_result["best_card_per_category"]


    # --- reward score (40) ---
    reward_score = min(yearly_value / 20000, 1) * 40


    # --- coverage score (25) ---
    covered = len(best_cards)

    coverage_score = (
        covered / len(IMPORTANT_CATEGORIES)
    ) * 25


    # --- diversification score (15) ---
    unique_cards = len(
        set([
            c["card_id"]
            for c in best_cards.values()
        ])
    )

    diversification_score = min(
        unique_cards / 3,
        1
    ) * 15


    # --- fee efficiency (20) ---
    if yearly_value > 0:
        fee_score = 20
    else:
        fee_score = 5


    total_score = (
        reward_score
        + coverage_score
        + diversification_score
        + fee_score
    )


    return {

        "wallet_score": round(total_score, 1),

        "component_scores": {

            "reward_score": round(reward_score, 1),

            "coverage_score": round(coverage_score, 1),

            "diversification_score": round(diversification_score, 1),

            "fee_score": round(fee_score, 1)

        }

    }
