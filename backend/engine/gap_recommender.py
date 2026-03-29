from backend.engine.card_registry import CARDS


def recommend_card_for_gap(

    wallet_analysis,

    monthly_spend

):

    coverage = wallet_analysis.get(

        "coverage_analysis",

        {}

    )

    missing_categories = coverage.get(

        "missing_categories",

        []

    )


    if not missing_categories:

        return {

            "message":

            "Your wallet already has strong coverage."

        }


    target_category = missing_categories[0]


    best_card = None

    best_rate = 0


    for card_id, card in CARDS.items():

        rules = card.get(

            "earn_rules",

            []

        )


        for rule in rules:

            if rule.get(

                "category"

            ) == target_category:


                rate = rule.get(

                    "reward_rate",

                    0

                )


                if rate > best_rate:

                    best_rate = rate


                    best_card = {

                        "card_id": card_id,

                        "reason":

                        f"Strong rewards for {target_category}",

                        "reward_rate": rate

                    }


    if not best_card:

        return {

            "message":

            f"No optimized card found for {target_category}"

        }


    return best_card



# backward compatibility for old routes

def recommend_card_for_gaps(

    wallet_analysis,

    monthly_spend

):

    return recommend_card_for_gap(

        wallet_analysis,

        monthly_spend

    )
