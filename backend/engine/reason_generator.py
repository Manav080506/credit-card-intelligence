def generate_reasons(card: dict, monthly_spend: dict) -> list[str]:
    """
    Generate intelligent, context-aware insights based on spend patterns and card profiles.
    Rules:
      - if online_ratio > 0.45: "High online spending detected"
      - if travel_ratio > 0.35: "Travel-heavy profile identified"
      - if balanced_spend: "Balanced spend pattern — general rewards card optimal"
    """
    reasons = []
    
    total_spend = sum(monthly_spend.values())
    if total_spend == 0:
        return reasons

    # Calculate spend ratios
    online_ratio = monthly_spend.get("online_shopping", 0) / total_spend if total_spend else 0
    dining_ratio = monthly_spend.get("dining", 0) / total_spend if total_spend else 0
    travel_ratio = monthly_spend.get("travel", 0) / total_spend if total_spend else 0
    utilities_ratio = monthly_spend.get("utilities", 0) / total_spend if total_spend else 0

    # Rule 1: High online spending pattern (>45%)
    if online_ratio > 0.45:
        amount = monthly_spend.get("online_shopping", 0)
        reasons.append(f"You spend heavily online (₹{int(amount)}/month) — cashback card recommended")

    # Rule 2: Travel-heavy profile (>35%)
    elif travel_ratio > 0.35:
        amount = monthly_spend.get("travel", 0)
        reasons.append(f"Travel-heavy profile detected ({int(travel_ratio * 100)}% of spend) — premium travel rewards ideal")

    # Rule 3: Dining-focused patterns (>30%)
    elif dining_ratio > 0.30:
        amount = monthly_spend.get("dining", 0)
        reasons.append(f"Dining-focused spending ({int(dining_ratio * 100)}% of transactions) — dining-premium card optimal")

    # Rule 4: Balanced spend pattern (no category > 40%)
    elif max(online_ratio, travel_ratio, dining_ratio, utilities_ratio) <= 0.40:
        reasons.append("Balanced spend pattern detected — general rewards card maximizes coverage")

    # High spend category alerts
    if online_ratio > 0.4:
        reasons.append(f"Online shopping rewards: {card.get('categories', {}).get('online_shopping', 1)}x points")
    
    if travel_ratio > 0.3:
        reasons.append(f"Travel bonus: {card.get('categories', {}).get('travel', 0)}x multiplier")

    if dining_ratio > 0.3:
        reasons.append(f"Dining cashback: {card.get('categories', {}).get('dining', 0)}x bonus")

    # Annual fee recovery logic
    annual_fee = card.get("annual_fee", 0)
    net_gain = card.get("net_monthly_gain", 0)

    if annual_fee > 0:
        if net_gain > 0:
            months_to_recover = round(annual_fee / net_gain, 1)
            reasons.append(f"Annual fee recovered in ~{months_to_recover} month(s)")
        else:
            reasons.append(f"Annual fee: ₹{annual_fee} (may not be beneficial)")
    else:
        reasons.append("Zero annual fee")

    # Card type reasoning
    card_name_lower = card.get("card_name", "").lower()
    if "cashback" in card_name_lower:
        reasons.append("Cashback provides predictable monthly savings")
    elif "travel" in card_name_lower:
        reasons.append("Specialized travel card — premium international benefits")
    elif "premium" in card_name_lower or "elite" in card_name_lower:
        reasons.append("Premium tier card — lifestyle and lounge benefits included")
    else:
        reasons.append("Smart card selection for maximum reward efficiency")

    return reasons[:4]  # Return top 4 reasons for clarity
