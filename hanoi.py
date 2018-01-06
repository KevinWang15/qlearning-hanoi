# coding=utf-8
# 总共有27种state，用SML表示盘子小、中、大，
# state表示为 S*3^0+M*3^1+L*3^2
# 其中S、M、L表示对应盘子所在柱子的位置，值为0、1或者2
# reward action矩阵中，用-1代表不连通
from init_reward_matrix import init_reward_matrix
from print_reward_matrix import print_reward_matrix

final_state = 26


def calc_reward_from_action(state_from, state_to):
    # if it solves the game, give reward 1000
    # otherwise, give punishment -1 (to prevent loop)
    if state_to == final_state:
        return 1000
    else:
        return -1


learning_rate = 0.2
discount_factor = 0.9

reward_matrix = init_reward_matrix()


def train():
    current_state = 0

    while current_state != final_state:
        possible_actions = reward_matrix[current_state]
        best_next_state_quality = -10000
        best_next_state = -1
        for i in range(0, len(possible_actions)):
            if possible_actions[i] > best_next_state_quality:
                best_next_state_quality = possible_actions[i]
                best_next_state = i
        reward = calc_reward_from_action(current_state, best_next_state)

        # update reward matrix
        reward_matrix[current_state][best_next_state] = (1 - learning_rate) * reward_matrix[current_state][
            best_next_state] + learning_rate * (reward + discount_factor * max(reward_matrix[best_next_state]))

        current_state = best_next_state


for i in range(0, 10000):
    train()


def print_state(state):
    pos_s = state % 3
    pos_m = (state / 3) % 3
    pos_l = (state / 9) % 3
    print "s:" + str(pos_s) + " m:" + str(pos_m) + " l:" + str(pos_l)


def print_solution():
    current_state = 0

    while current_state != final_state:
        print_state(current_state)
        possible_actions = reward_matrix[current_state]
        best_next_state_quality = -10000
        best_next_state = -1
        for i in range(0, len(possible_actions)):
            if possible_actions[i] > best_next_state_quality:
                best_next_state_quality = possible_actions[i]
                best_next_state = i
        current_state = best_next_state

    print_state(current_state)


print_solution()
