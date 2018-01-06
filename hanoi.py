# coding=utf-8
# 总共有27种state，用SML表示盘子小、中、大，
# state表示为 S*3^0+M*3^1+L*3^2
# 其中S、M、L表示对应盘子所在柱子的位置，值为0、1或者2
# reward action矩阵中，用-1代表不连通
from init_reward_matrix import init_reward_matrix

reward = init_reward_matrix()

for i in range(0, len(reward)):
    print reward[i]
