from backend.engine.reward_value_map import REWARD_VALUE_MAP


def convert_reward_to_value(reward_amount, reward_unit):

    conversion_rate = REWARD_VALUE_MAP.get(
        reward_unit,
        0.25
    )

    return round(
        reward_amount * conversion_rate,
        2
    )
