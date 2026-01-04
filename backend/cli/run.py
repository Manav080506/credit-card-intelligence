#!/usr/bin/env python3

from backend.engine.earn_calculator import calculate_reward
from backend.engine.redeem_calculator import calculate_redemption


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

    print("=== BEST REDEMPTION OPTION ===")
    best = result["best_option"]
    print(f"{best['type'].upper()} → {best['partner']}")
    print(f"Value: ₹{best['value']} ({best['value_per_point']} / point)")
    print(f"Note: {best['notes']}")

    print("\n--- Other Options ---")
    for opt in result["all_options"][1:]:
        print(f"{opt['type']} → {opt['partner']} : ₹{opt['value']}")


def main():
    print("=== Credit Card Intelligence Engine ===\n")
    print("Choose an option:")
    print("1) Earn rewards")
    print("2) Redeem points")
    print("3) Exit\n")

    choice = prompt("Enter choice (1/2/3): ")

    if choice == "1":
        earn_flow()
    elif choice == "2":
        redeem_flow()
    else:
        print("Goodbye 👋")


if __name__ == "__main__":
    main()
