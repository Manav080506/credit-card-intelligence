from backend.engine.wallet_optimizer import optimize_wallet

from backend.engine.combo_optimizer_v2 import find_best_combo

from backend.engine.statement_analyzer import analyze_statement

from backend.engine.spend_simulator import simulate_spend_change

from backend.engine.wallet_advisor import analyze_wallet

from backend.engine.insight_engine import generate_insights

from backend.workers.card_discovery_worker import discover_cards
from backend.workers.card_update_worker import update_all_cards
from backend.workers.duplicate_card_detector import find_duplicates

from backend.workers.benefit_extractor_worker import BenefitExtractorWorker
from backend.workers.reward_rules_validator_worker import RewardRulesValidatorWorker
from backend.workers.category_gap_detector_worker import CategoryGapDetectorWorker

from backend.workers.user_spend_pattern_worker import UserSpendPatternWorker
from backend.workers.dynamic_reward_predictor import DynamicRewardPredictorWorker
from backend.workers.reward_confidence_engine import RewardConfidenceEngineWorker



def run_full_analysis(payload):

    results = {}


    # wallet optimization

    if "wallet" in payload:

        results["wallet"] = optimize_wallet(

            payload["wallet"]["card_ids"],

            payload["wallet"]["monthly_spend"]

        )


    # combo optimizer

    if "combo" in payload:

        results["combo"] = find_best_combo(

            payload["combo"]["monthly_spend"]

        )


    # statement analyzer

    if "statement" in payload:

        results["statement"] = analyze_statement(

            payload["statement"]["card_ids"],

            payload["statement"]["transactions"]

        )


    # spend simulation

    if "simulation" in payload:

        results["simulation"] = simulate_spend_change(

            payload["simulation"]["card_ids"],

            payload["simulation"]["current_spend"],

            payload["simulation"]["new_spend"]

        )


    # wallet advisor

    if "advisor" in payload:

        results["advisor"] = analyze_wallet(

            payload["advisor"]["card_ids"],

            payload["advisor"]["monthly_spend"]

        )


    # generate insights

    if "wallet" in results:

        results["insights"] = generate_insights(

            results["wallet"],

            results.get("simulation")

        )


    return results


class InsightOrchestratorV2:
    """Simple orchestrator for card, reward, and user intelligence pipelines."""

    def __init__(self):
        # Layer 1 workers (function-style modules)
        self.card_discovery_worker = discover_cards
        self.card_update_worker = update_all_cards
        self.duplicate_detector_worker = find_duplicates

        # Layer 2 workers (class-style workers)
        self.benefit_extractor_worker = BenefitExtractorWorker()
        self.reward_rules_validator_worker = RewardRulesValidatorWorker()
        self.category_gap_detector_worker = CategoryGapDetectorWorker()

        # Layer 3 workers (class-style workers)
        self.user_spend_pattern_worker = UserSpendPatternWorker()
        self.dynamic_reward_predictor_worker = DynamicRewardPredictorWorker()
        self.reward_confidence_engine_worker = RewardConfidenceEngineWorker()

    def _safe_run(self, label, fn, *args, **kwargs):
        """Run one worker step without interrupting the full pipeline on failure."""
        print(f"[orchestrator-v2] running {label}")
        try:
            result = fn(*args, **kwargs)
            print(f"[orchestrator-v2] success {label}")
            return {
                "status": "success",
                "result": result,
            }
        except Exception as e:
            print(f"[orchestrator-v2] failed {label}: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "result": None,
            }

    def _pipeline_status(self, steps):
        statuses = [step.get("status") for step in steps.values()]

        if all(status == "success" for status in statuses):
            return "success"

        if any(status == "success" for status in statuses):
            return "partial_success"

        return "failed"

    def run_data_pipeline(self):
        """Run card maintenance workers: discovery, updates, duplicate detection."""
        steps = {
            "card_discovery": self._safe_run(
                "data.card_discovery",
                self.card_discovery_worker,
            ),
            "card_updates": self._safe_run(
                "data.card_updates",
                self.card_update_worker,
                {},
            ),
            "duplicate_detection": self._safe_run(
                "data.duplicate_detection",
                self.duplicate_detector_worker,
            ),
        }

        return {
            "status": self._pipeline_status(steps),
            "steps": steps,
        }

    def run_reward_pipeline(self):
        """Run reward intelligence workers: extraction, validation, gap detection."""
        extraction_step = self._safe_run(
            "reward.benefit_extraction",
            self.benefit_extractor_worker.extract_benefits,
            "5% cashback on Amazon up to 1000 per month",
        )

        extracted = extraction_step.get("result") or {}
        validation_input = {
            "category": extracted.get("category", "others"),
            "reward_rate": extracted.get("reward_rate", 0),
            "reward_unit": extracted.get("reward_type", "cashback"),
            "cap_amount": extracted.get("cap_amount"),
            "cap_period": extracted.get("cap_period"),
        }

        steps = {
            "benefit_extraction": extraction_step,
            "reward_validation": self._safe_run(
                "reward.rules_validation",
                self.reward_rules_validator_worker.validate_reward_rule,
                validation_input,
            ),
            "category_gap_detection": self._safe_run(
                "reward.category_gap_detection",
                self.category_gap_detector_worker.run,
            ),
        }

        return {
            "status": self._pipeline_status(steps),
            "steps": steps,
        }

    def run_user_pipeline(self, transactions):
        """Run user intelligence workers: spend pattern, prediction, confidence."""
        transactions = transactions or []

        spend_step = self._safe_run(
            "user.spend_pattern",
            self.user_spend_pattern_worker.analyze_transactions,
            transactions,
        )

        spend_pattern = spend_step.get("result") or {}

        prediction_step = self._safe_run(
            "user.reward_prediction",
            self.dynamic_reward_predictor_worker.predict_best_card,
            spend_pattern,
        )

        prediction = prediction_step.get("result") or {}

        confidence_step = self._safe_run(
            "user.prediction_confidence",
            self.reward_confidence_engine_worker.calculate_prediction_confidence,
            prediction,
        )

        steps = {
            "spend_pattern": spend_step,
            "reward_prediction": prediction_step,
            "prediction_confidence": confidence_step,
        }

        return {
            "status": self._pipeline_status(steps),
            "best_card": prediction.get("best_card_id"),
            "confidence": confidence_step.get("result", 0),
            "steps": steps,
        }

    def run_full_pipeline(self, transactions=None):
        """Run data, reward, and user pipelines in order."""
        data_result = self.run_data_pipeline()
        reward_result = self.run_reward_pipeline()
        user_result = self.run_user_pipeline(transactions or [])

        return {
            "data_pipeline": data_result.get("status"),
            "reward_pipeline": reward_result,
            "user_pipeline": {
                "status": user_result.get("status"),
                "best_card": user_result.get("best_card"),
                "confidence": user_result.get("confidence"),
            },
            "details": {
                "data": data_result,
                "reward": reward_result,
                "user": user_result,
            },
        }


def run_data_pipeline():
    return InsightOrchestratorV2().run_data_pipeline()


def run_reward_pipeline():
    return InsightOrchestratorV2().run_reward_pipeline()


def run_user_pipeline(transactions):
    return InsightOrchestratorV2().run_user_pipeline(transactions)


def run_full_pipeline(transactions=None):
    return InsightOrchestratorV2().run_full_pipeline(transactions)


if __name__ == "__main__":
    orchestrator = InsightOrchestratorV2()

    sample_transactions = [
        {"merchant": "Amazon", "amount": 4000},
        {"merchant": "Swiggy", "amount": 1200},
    ]

    print(orchestrator.run_full_pipeline(sample_transactions))
