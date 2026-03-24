import csv

from backend.engine.transaction_optimizer import best_card_for_transaction

from backend.engine.merchant_classifier import classify_merchant

def analyze_statement(
    card_ids,
    transactions
):

    results = []

    total_possible_reward = 0


    for txn in transactions:

        recommendation = best_card_for_transaction(

            card_ids=card_ids,

            amount=txn["amount"],

            category=txn["category"]

        )


        results.append({

            "merchant": txn["merchant"],

            "amount": txn["amount"],

            "category": txn["category"],

            "recommended_card": recommendation["recommended_card"],

            "expected_reward": recommendation["expected_reward_value"]

        })


        total_possible_reward += recommendation["expected_reward_value"]


    return {

        "transactions_analyzed": len(results),

        "total_possible_reward": round(total_possible_reward, 2),

        "recommendations": results

    }
