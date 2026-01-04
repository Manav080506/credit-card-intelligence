#!/usr/bin/env python3

from backend.engine.earn_calculator import calculate_reward
from backend.engine.redeem_calculator import calculate_redemption
from backend.engine.card_recommender import recommend_cards


def prompt(label: str) -> str:
    value = input(label).strip()
    print(f"→ {value}\n")
    return value


def earn_flow():
    card_id = prompt("Enter card id (example: hdfc_millennia): ")
    category = prompt("Enter spend category (example: online_shopping): ")
    amount = float(prompt("Enter spend amount: "))

    result = calculate_reward(
        card_id=card_id,
        amount=amount,
        category=category
    )

    print("--- Reward Result ---")
    print(f"Reward Earned : {result['reward_amount']} {result['reward_unit']}")
    print(f"Cap Applied   : {'Yes' if result['cap_applied'] else 'No'}")
    print(f"Explanation  : {result['explanation']}")


def redeem_flow():
    card_id = prompt("Enter card id (example: hdfc_regalia_gold): ")
    points = int(prompt("Enter available points: "))

    result = calculate_redemption(card_id=card_id, points=points)

    if "error" in result:
        print(f"⚠️ {result['error']}")
        return

    best = result["best_option"]

    print("=== BEST REDEMPTION OPTION ===")
    print(f"{best['type'].upper()} → {best['partner']}")
    print(f"Value: ₹{best['value']} ({best['value_per_point']} / point)")
    print(f"Note: {best['notes']}")

    print("\n--- Other Options ---")
    for opt in result["all_options"][1:]:
        print(f"{opt['type']} → {opt['partner']} : ₹{opt['value']}")


def recommend_flow():
    print("Enter your average MONTHLY spend\n")

    monthly_spend = {
        "online_shopping": float(prompt("Online shopping spend (₹): ")),
        "food_dining": float(prompt("Food & dining spend (₹): ")),
        "travel": float(prompt("Travel spend (₹): ")),
        "utilities": float(prompt("Utilities spend (₹): "))
    }

    result = recommend_cards(monthly_spend=monthly_spend)

    best = result["best_card"]

    print("\n=== BEST CARD FOR YOU ===")
    print(f"Card: {best['card_name']}")
    print(f"Net Monthly Gain: ₹{best['net_monthly_gain']}")
    print("Reasons:")
    for r in best["reasons"]:
        print(f"• {r}")

    if result["alternatives"]:
        print("\n--- Alternatives ---")
        for alt in result["alternatives"]:
            print(f"{alt['card_name']} (₹{alt['net_monthly_gain']}/month)")


def main():
    print("=== Credit Card Intelligence Engine ===\n")
    print("Choose an option:")
    print("1) Earn rewards")
    print("2) Redeem points")
    print("3) Recommend a card")
    print("4) Exit\n")

    choice = prompt("Enter choice (1/2/3/4): ")

    if choice == "1":
        earn_flow()
    elif choice == "2":
        redeem_flow()
    elif choice == "3":
        recommend_flow()
    else:
        print("Goodbye 👋")


if __name__ == "__main__":
    main()
