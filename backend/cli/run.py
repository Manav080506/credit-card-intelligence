#!/usr/bin/env python3

from backend.engine.earn_calculator import calculate_reward


def prompt(label: str) -> str:
    value = input(label).strip()
    print(f"→ {value}\n")
    return value


def main():
    print("=== Credit Card Intelligence Engine ===\n")

    card_id = prompt("Enter card id (example: hdfc_millennia): ")
    category = prompt("Enter spend category (example: online_shopping): ")
    amount = float(prompt("Enter spend amount: "))

    result = calculate_reward(
        card_id=card_id,
        amount=amount,
        category=category
    )

    print("--- Result ---")
    print(f"Reward Earned : {result['reward_amount']} {result['reward_unit']}")
    print(f"Cap Applied   : {'Yes' if result['cap_applied'] else 'No'}")
    print(f"Explanation  : {result['explanation']}")


if __name__ == "__main__":
    main()
