from backend.engine.reward_value_map import REWARD_VALUE_MAP


def convert_reward_to_value(
    reward_result: dict,
    card: dict
):

    reward_amount = reward_result.get(
        "reward_amount",
        0
    )

    reward_unit = reward_result.get(
        "reward_unit"
    )


    # safety fix
    if isinstance(reward_unit, dict):

        reward_unit = reward_unit.get(
            "type",
            "cashback"
        )


    conversion_rate = REWARD_VALUE_MAP.get(

        reward_unit,

        1   # cashback default

    )


    value = reward_amount * conversion_rate


    return round(value, 2)
