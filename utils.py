import sys

final_state = 26


def print_state(state):
    pos_s = state % 3
    pos_m = (state / 3) % 3
    pos_l = (state / 9) % 3

    def print_pos(pos):
        sys.stdout.write("[")
        if pos_s == pos:
            sys.stdout.write("S")
        if pos_m == pos:
            sys.stdout.write("M")
        if pos_l == pos:
            sys.stdout.write("L")
        sys.stdout.write("]")

    print_pos(0)
    print_pos(1)
    print_pos(2)
    sys.stdout.write("\n")


def get_state(s, m, l):
    return (s % 3) + (m % 3) * 3 + (l % 3) * 9


def print_solution(reward_matrix, current_state=0):
    print "START"
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
    print "END\n"


def print_reward_matrix(reward):
    for i in range(0, len(reward)):
        print reward[i]
