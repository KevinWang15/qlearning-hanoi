# coding=utf-8
# 总共有27种state，用SML表示盘子小、中、大，
# state表示为 S*3^0+M*3^1+L*3^2
# 其中S、M、L表示对应盘子所在柱子的位置，值为0、1或者2
# reward action矩阵中，用-1代表不连通

from common import reward_matrix
from train import train
from random import randint
from utils import print_solution, get_state

for i in range(0, 100000):
    train(randint(0, 26))

for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            print_solution(reward_matrix, get_state(i, j, k))
