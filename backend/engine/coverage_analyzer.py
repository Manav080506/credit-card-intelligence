IMPORTANT_CATEGORIES = [
    "online_shopping",
    "travel",
    "dining",
    "groceries",
    "fuel",
    "others"
]


STRONG_THRESHOLD = 0.03
WEAK_THRESHOLD = 0.01


def analyze_coverage(best_card_per_category):

    strong = []
    weak = []
    missing = []


    for category in IMPORTANT_CATEGORIES:

        if category not in best_card_per_category:

            missing.append(category)
            continue


        reward = best_card_per_category[category]["monthly_reward"]


        if reward >= STRONG_THRESHOLD * 10000:

            strong.append(category)

        elif reward >= WEAK_THRESHOLD * 10000:

            weak.append(category)

        else:

            missing.append(category)


    coverage_score = (
        len(strong) / len(IMPORTANT_CATEGORIES)
    ) * 100


    return {

        "strong_categories": strong,

        "weak_categories": weak,

        "missing_categories": missing,

        "coverage_score": round(coverage_score, 1)

    }
