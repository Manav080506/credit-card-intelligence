from backend.engine.wallet_optimizer import optimize_wallet
from backend.engine.combo_optimizer_v2 import find_best_combo
from backend.engine.statement_analyzer import analyze_statement
from backend.engine.spend_simulator import simulate_spend_change
from backend.engine.wallet_advisor import analyze_wallet


def run_full_analysis(payload):

    results = {}

    if "wallet" in payload:

        results["wallet"] = optimize_wallet(
            payload["wallet"]["card_ids"],
            payload["wallet"]["monthly_spend"]
        )

    if "combo" in payload:

        results["combo"] = find_best_combo(
            payload["combo"]["monthly_spend"]
        )

    if "statement" in payload:

        results["statement"] = analyze_statement(
            payload["statement"]["card_ids"],
            payload["statement"]["transactions"]
        )

    if "simulation" in payload:

        results["simulation"] = simulate_spend_change(
            payload["simulation"]["card_ids"],
            payload["simulation"]["current_spend"],
            payload["simulation"]["new_spend"]
        )

    if "advisor" in payload:

        results["advisor"] = analyze_wallet(
            payload["advisor"]["card_ids"],
            payload["advisor"]["monthly_spend"]
        )

    return results
