from backend.engine.wallet_optimizer import optimize_wallet
from backend.engine.bootstrap import CARDS


def recommend_card_for_gaps(current_cards, monthly_spend):

    baseline = optimize_wallet(

        card_ids=current_cards,

        monthly_spend=monthly_spend

    )


    baseline_score = baseline["wallet_score"]

    best_improvement = None


    for candidate in CARDS.keys():

        if candidate in current_cards:
            continue


        new_wallet = optimize_wallet(

            card_ids=current_cards + [candidate],

            monthly_spend=monthly_spend

        )


        score_gain = (

            new_wallet["wallet_score"]

            - baseline_score

        )


        yearly_gain = (

            new_wallet["net_yearly_value"]

            - baseline["net_yearly_value"]

        )


        if (

            best_improvement is None

            or score_gain > best_improvement["score_gain"]

        ):

            best_improvement = {

                "recommended_card": candidate,

                "score_gain": round(score_gain, 2),

                "yearly_value_gain": round(yearly_gain, 2),

                "new_wallet_score": new_wallet["wallet_score"],

                "new_net_yearly_value": new_wallet["net_yearly_value"]

            }


    return best_improvement
