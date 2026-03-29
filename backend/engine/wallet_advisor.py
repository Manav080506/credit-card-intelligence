from backend.engine.wallet_optimizer import optimize_wallet
from backend.engine.gap_recommender import recommend_card_for_gap
from backend.engine.insight_engine import generate_insights


def analyze_wallet(

    card_ids,

    monthly_spend

):

    wallet_analysis = optimize_wallet(

        card_ids,

        monthly_spend

    )


    recommendation = recommend_card_for_gap(

        wallet_analysis,

        monthly_spend

    )


    insights = generate_insights(

        wallet_analysis

    )


    return {

        "wallet_score": wallet_analysis["wallet_score"],

        "net_yearly_value": wallet_analysis["net_yearly_value"],

        "coverage_analysis": wallet_analysis["coverage_analysis"],

        "recommended_card_to_add": recommendation,

        "insights": insights

    }
