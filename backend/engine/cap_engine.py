def apply_reward_cap(
    spend: float,
    reward_rate: float,
    cap: dict | None,
    post_cap_rate: float | None = None
):
    if not cap:
        return spend * reward_rate

    cap_amount = cap["amount"]

    # max spend eligible for full reward rate
    max_spend_at_rate = cap_amount / reward_rate

    if spend <= max_spend_at_rate:
        return spend * reward_rate

    reward_before_cap = max_spend_at_rate * reward_rate

    remaining_spend = spend - max_spend_at_rate

    post_rate = post_cap_rate or 0

    reward_after_cap = remaining_spend * post_rate

    return reward_before_cap + reward_after_cap
