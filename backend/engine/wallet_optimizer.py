from backend.engine.card_registry import CARDS
from backend.engine.earn_calculator import calculate_reward
from backend.engine.reward_value_converter import convert_reward_to_value
from backend.engine.coverage_analyzer import analyze_coverage
from backend.engine.wallet_scorer import score_wallet
from backend.engine.milestone_engine import apply_milestone_bonus


def optimize_wallet(
    card_ids: list[str],
    monthly_spend: dict[str, float]
):

    best_per_category = {}

    total_monthly_reward_value = 0
    yearly_fee_total = 0


    # --- find best card per category ---
    for category, spend in monthly_spend.items():

        best_card = None
        best_value = 0

        for card_id in card_ids:

            card = CARDS.get(card_id)

            if not card:
                continue

            reward_result = calculate_reward(
                card_id=card_id,
                amount=spend,
                category=category
            )

            reward_value = convert_reward_to_value(
                reward_result,
                card
            )

            if reward_value > best_value:
                best_value = reward_value
                best_card = card_id

        best_per_category[category] = {
            "card_id": best_card,
            "monthly_reward": round(best_value, 2)
        }

        total_monthly_reward_value += best_value


    # --- yearly reward ---
    yearly_reward = total_monthly_reward_value * 12


    # --- yearly fees ---
    for card_id in card_ids:

        card = CARDS.get(card_id)

        if not card:
            continue

        yearly_fee_total += card.get(
            "fees",
            {}
        ).get(
            "annual_fee",
            0
        )


    # --- milestone bonuses ---
    yearly_spend_total = sum(
        monthly_spend.values()
    ) * 12


    for card_id in card_ids:

        card = CARDS.get(card_id)

        if not card:
            continue

        milestone_bonus = apply_milestone_bonus(

            yearly_spend_total,

            card.get("milestones")

        )

        yearly_reward += milestone_bonus


    # --- net value ---
    net_yearly_value = yearly_reward - yearly_fee_total


    # --- coverage analysis ---
    coverage = analyze_coverage(
        best_per_category
    )


    # --- wallet score ---
    wallet_score_result = score_wallet(

        best_per_category,

        yearly_fee_total,

        net_yearly_value

    )


    return {

        "best_card_per_category": best_per_category,

        "total_monthly_reward": round(
            total_monthly_reward_value,
            2
        ),

        "estimated_yearly_reward": round(
            yearly_reward,
            2
        ),

        "estimated_annual_fees": yearly_fee_total,

        "net_yearly_value": round(
            net_yearly_value,
            2
        ),

        "wallet_score": wallet_score_result[
            "wallet_score"
        ],

        "score_breakdown": wallet_score_result[
            "score_breakdown"
        ],

        "coverage_analysis": coverage

    }
