def apply_milestone_bonus(
    yearly_spend: float,
    milestones: list | None
):
    if not milestones:
        return 0

    bonus_value = 0

    for milestone in milestones:
        threshold = milestone["spend_threshold"]

        if yearly_spend >= threshold:
            bonus_value += milestone["reward_value"]

    return bonus_value
