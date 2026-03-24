def generate_reasons(card: dict, monthly_spend: dict) -> list[str]:
    reasons = []

    # High spend categories
    for category, amount in monthly_spend.items():
        if amount >= 15000:
            reasons.append(
                f"High {category.replace('_', ' ')} spend (₹{amount}/month)"
            )

    # Annual fee logic
    annual_fee = card.get("annual_fee", 0)
    net_gain = card.get("net_monthly_gain", 0)

    if annual_fee > 0:
        months_to_recover = round(annual_fee / max(net_gain, 1), 1)
        reasons.append(
            f"Annual fee of ₹{annual_fee} recovered in ~{months_to_recover} month(s)"
        )
    else:
        reasons.append("No annual fee")

    # Reward type reasoning
    if "cashback" in card.get("card_name", "").lower():
        reasons.append("Cashback gives predictable monthly savings")
    else:
        reasons.append("Reward structure evaluated for maximum value")

    return reasons
