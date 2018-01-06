final_state = 26


def print_state(state):
    pos_s = state % 3
    pos_m = (state / 3) % 3
    pos_l = (state / 9) % 3
    print "s:" + str(pos_s) + " m:" + str(pos_m) + " l:" + str(pos_l)


def print_solution(reward_matrix):
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


def print_reward_matrix(reward):
    for i in range(0, len(reward)):
        print reward[i]
