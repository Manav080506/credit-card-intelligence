def generate_insights(

    wallet_analysis,

    simulation_result=None

):

    insights = []

    coverage = wallet_analysis.get(

        "coverage_analysis",

        {}

    )

    score = wallet_analysis.get(

        "wallet_score",

        0

    )

    net_value = wallet_analysis.get(

        "net_yearly_value",

        0

    )

    weak_categories = coverage.get(

        "weak_categories",

        []

    )

    missing_categories = coverage.get(

        "missing_categories",

        []

    )


    # overall score insight

    if score >= 80:

        insights.append(

            "Your wallet is highly optimized for your spending pattern."

        )

    elif score >= 60:

        insights.append(

            "Your wallet is moderately optimized but can be improved."

        )

    else:

        insights.append(

            "Your wallet is under-optimized. You may be losing significant rewards."

        )


    # coverage insights

    if weak_categories:

        insights.append(

            f"Weak reward coverage detected in: {', '.join(weak_categories)}."

        )


    if missing_categories:

        insights.append(

            f"No strong card detected for: {', '.join(missing_categories)}."

        )


    # value insight

    insights.append(

        f"Estimated yearly reward value: ₹{round(net_value)}."

    )


    # simulation insights

    if simulation_result:

        reward_change = simulation_result.get(

            "reward_change",

            0

        )

        score_change = simulation_result.get(

            "wallet_score_change",

            0

        )


        if reward_change > 0:

            insights.append(

                f"Optimizing spending could increase yearly rewards by ₹{round(reward_change)}."

            )


        if score_change > 5:

            insights.append(

                "Spending optimization significantly improves wallet efficiency."

            )


    return insights
