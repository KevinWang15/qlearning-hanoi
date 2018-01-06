from utils import get_state


def init_reward_matrix():
    reward = []

    # set the reward of unconnected area to -1000
    for i in range(0, 27):
        row = []
        for j in range(0, 27):
            row.append(-1000)
        reward.append(row)

    # set the reward of connected states to 0
    for state in range(0, 27):  # enumerate state
        pos_s = state % 3
        pos_m = (state / 3) % 3
        pos_l = (state / 9) % 3

        for i in range(0, 3):  # small can move freely
            reward[state][get_state(i, pos_m, pos_l)] = 0

        if pos_m != pos_s:  # if middle can move
            for i in range(0, 3):
                if pos_s != i:
                    reward[state][get_state(pos_s, i, pos_l)] = 0

        if pos_l != pos_m and pos_l != pos_s:  # if large can move
            for i in range(0, 3):
                if pos_m != i and pos_s != i:
                    reward[state][get_state(pos_s, pos_m, i)] = 0

        reward[state][state] = -1000  # prevent loop

    # set the reward of completing the puzzle to 1000
    # for i in range(24, 26):
    #     reward[i][26] = 1000

    return reward
