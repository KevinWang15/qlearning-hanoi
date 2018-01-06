# 使用QLearning玩汉诺塔

本Project使用QLearning的方法（Reinforcement Learning）训练模型，玩汉诺塔游戏。

个人的感觉是，虽然汉诺塔这么简单的游戏没必要用机器学习，但是通过这个例子，学习QLearning的编写和使用，是非常有意思的！因为汉诺塔总共只有27个state，所以模型训练成本极小。可以手动实现QLearning的每个步骤，训练完之后，给任何一个初态都可以输出到终态的最短路径。我没有写任何传统的递归算法，汉诺塔却被成功解出，而且每次调用训练好的模型求解，都不用经过任何试探，直接找quality最大的路径就是解的路径，感觉非常神奇。

## State的定义

汉诺塔总共有27种state，我用以下规则进行编码：令S、M、L分别指小盘子、中盘子、大盘子，012分别指第1、2、3根柱子。p(X)指盘子的位置（值为0,1,2，X可以为S、M、L）

定义

> state = p(S) + p(M) * 3 + p(L) * 9

state的取值范围为0-26，可以覆盖所有可能的游戏状态。

## Reward和Punishment的定义

在```reward_punishment.py```中，我定义了增强学习所必须的reward和punishment，这个一般由外界环境给出，而在汉诺塔游戏中，可以直接定义为：如果成功解出了本游戏，则给1000的reward，否则，给-1的punishment。

```python
from utils import final_state


def calc_reward_from_action(state_from, state_to):
    # if it solves the game, give reward 1000
    # otherwise, give punishment -1 (to prevent loop)
    if state_to == final_state:
        return 1000
    else:
        return -1

```

为什么要给-1的punishment，我是希望程序可以以最小步数解出汉诺塔游戏。如果不给这个punishment，在训练的过程中，有可能会有loop的产生（几个state间产生环，兜来兜去陷在里面）。

## Reward Matrix的初始化

Reward Matrix有27行27列，行为State，列为Action。Action解读为：在当前这个State，转变到另一个State的Action。Matrix的值，就是做这个State转变到另一个State这个Action的Quality。由于不是所有的State都可以直接转变的（比如不能从{SML}{}{}直接转到{}{}{SML}），需要有一个算法去检查state之间的连通性，并把不连通的state的reward matrix值设置为-1000。

```python
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

    return reward

```

初始化后，这个矩阵是一个关于对角线对称的矩阵（因为所有action都是可逆的）

矩阵里大多数是-1000，分布着一些0。

## 模型的训练

训练就是通过多个episode，去更新reward matrix。

使用了wikipedia上给出的一个更加完整的公式，包含```learning rate```和```discount factor```

![qlearning-math](https://wikimedia.org/api/rest_v1/media/math/render/svg/1df368653bf2eb16081f8738486ef4c9d60e9d03)

这里我设置了

```
learning_rate = 0.2
discount_factor = 0.9
```

训练的代码长这样：

```python
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
```

大概就是找最好Quality的Action（由于没有随机性，直接用了贪心算法），并采取那个action，通过reward来更新reward matrix的值。

这里，我把reward作为了黑盒，用```calc_reward_from_action```获得。这个函数，输入的是你要采取的action（从```current_state```转移到```best_next_state```），输出的是这个action的reward和punishment。所以，可以认为这个reward或者punishment来自于环境，或者说，qlearning对汉诺塔游戏的规则是毫无任何了解的。

很少的迭代次数后，模型（reward matrix）值就固定下来了，我后来试了1000、10000、100000次训练，模型的值鲜有改动。

## 模型的使用

模型的使用更加简单，直接用贪心算法，每个state找到quality最大的action就行。没几步，就能输出答案。代码如下：

```python
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
```

其中```print_state```是为了让输出好看一点加上的

```python
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
```

输出结果：

```
START
[SML][][]
[ML][][S]
[L][M][S]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END
```

的确输出了最优解！

而且，我把```print_solution```的```current_state```参数改了个值（修改初态），发现这个模型也可以毫不费力地从另一个开局，找到完成游戏的最优解！

```
START
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END
```

## 遇到问题和解决

自然想到的是，我希望把27种开局的最优解都打印出来，于是我写了个循环。意外的却是：它死循环了。

通过调试，我最终发现问题出在{S}{ML}{}这种状态下。这种状态下，model会在两个reward都为0的action中跳来跳去。因为这个区域是模型没有训练到的区域（从{SML}{}{}开局，永远不会走到这两个状态）。

为了解决这个问题，我重新看了一下课件，看到了

>  –Select random initial state

于是，修改train方法，让它可以接受任何一个```initial_state```

```python
def train(initial_state=0):
    current_state = initial_state
```

使用时，

```python
for i in range(0, 100000):
    train(randint(0, 26))
```

这样训练出来的新模型，就没有死角了。

## 游戏胜利

最终，通过一个循环，本QLearning算法打印出了汉诺塔所有开局的最佳解。

```
START
[SML][][]
[ML][][S]
[L][M][S]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[SL][M][]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[S][ML][]
[][ML][S]
[M][L][S]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[S][M][L]
[S][][ML]
[][][SML]
END

START
[SL][][M]
[SL][M][]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[S][L][M]
[S][ML][]
[][ML][S]
[M][L][S]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[S][][ML]
[][][SML]
END

START
[ML][S][]
[L][S][M]
[SL][][M]
[SL][M][]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[M][SL][]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[M][S][L]
[][S][ML]
[][][SML]
END

START
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[][SML][]
[][ML][S]
[M][L][S]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[L][S][M]
[SL][][M]
[SL][M][]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[][SL][M]
[M][SL][]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[][S][ML]
[][][SML]
END

START
[ML][][S]
[L][M][S]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[M][L][S]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[L][M][S]
[L][SM][]
[][SM][L]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[][ML][S]
[M][L][S]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[][M][SL]
[S][M][L]
[S][][ML]
[][][SML]
END

START
[L][][SM]
[][L][SM]
[][SL][M]
[M][SL][]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[][L][SM]
[][SL][M]
[M][SL][]
[SM][L][]
[SM][][L]
[M][][SL]
[M][S][L]
[][S][ML]
[][][SML]
END

START
[][][SML]
END
```

