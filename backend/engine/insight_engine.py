def generate_insights(wallet_result):

    insights = []

    coverage = wallet_result.get(
        "coverage_analysis",
        {}
    )

    missing = coverage.get(
        "missing_categories",
        []
    )

    weak = coverage.get(
        "weak_categories",
        []
    )

    if missing:

        insights.append(

            f"Missing categories: {', '.join(missing)}"

        )

    if weak:

        insights.append(

            f"Weak reward coverage in: {', '.join(weak)}"

        )

    value = wallet_result.get(
        "net_yearly_value",
        0
    )

    if value < 5000:

        insights.append(

            "Low yearly reward potential"

        )

    if value > 30000:

        insights.append(

            "Strong reward optimization achieved"

        )

    return insights
