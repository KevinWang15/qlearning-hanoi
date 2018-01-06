from common import reward_matrix, learning_rate, discount_factor
from reward_punishment import calc_reward_from_action
from utils import final_state


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