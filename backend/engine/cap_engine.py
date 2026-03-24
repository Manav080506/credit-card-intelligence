def apply_cap(reward, cap):

    if cap is None:
        return reward, False

    if reward > cap:
        return cap, True

    return reward, False
