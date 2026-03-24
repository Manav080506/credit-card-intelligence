from backend.engine.wallet_optimizer import optimize_wallet
from backend.engine.gap_recommender import recommend_card_for_gaps
from backend.engine.insight_engine import generate_insights


def analyze_wallet(
    card_ids,
    monthly_spend
):

    wallet = optimize_wallet(
        card_ids,
        monthly_spend
    )

    recommendation = recommend_card_for_gaps(
        current_cards=card_ids,
        monthly_spend=monthly_spend
    )

    return {

        "wallet_score":
            wallet["wallet_score"],

        "net_yearly_value":
            wallet["net_yearly_value"],

        "coverage_analysis":
            wallet["coverage_analysis"],

        "recommended_card_to_add":
            recommendation,

        "insights":
            generate_insights(wallet)

    }
