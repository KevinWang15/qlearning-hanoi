from utils import final_state


def calc_reward_from_action(state_from, state_to):
    # if it solves the game, give reward 1000
    # otherwise, give punishment -1 (to prevent loop)
    if state_to == final_state:
        return 1000
    else:
        return -1
