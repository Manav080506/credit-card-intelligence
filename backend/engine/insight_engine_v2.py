from typing import Dict, List

from backend.workers.orchestrator import InsightOrchestratorV2


def get_best_card_for_transactions(transactions: List[Dict]) -> Dict:
    """Run the v2 orchestrator and return a compact best-card recommendation view."""
    orchestrator = InsightOrchestratorV2()
    pipeline_result = orchestrator.run_full_pipeline(transactions)

    user_pipeline = pipeline_result.get("user_pipeline", {})
    details = pipeline_result.get("details", {})
    user_details = details.get("user", {})

    reward_prediction = (
        user_details
        .get("steps", {})
        .get("reward_prediction", {})
        .get("result", {})
    )

    best_card = user_pipeline.get("best_card") or reward_prediction.get("best_card_id")
    expected_reward = reward_prediction.get("best_reward", 0)
    estimates = reward_prediction.get("estimates", {})
    category_breakdown = estimates.get(best_card, {}).get("category_breakdown", {})

    return {
        "best_card": best_card,
        "expected_reward": expected_reward,
        "confidence": user_pipeline.get("confidence", 0),
        "category_breakdown": category_breakdown,
    }
