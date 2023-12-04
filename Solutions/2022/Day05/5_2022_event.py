# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 5

import re
import numpy as np
import copy
from functools import reduce


# PARAMETERS
data_path = "5_2022_data.txt"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    split_element = data.index('')
    data_crates, data_procedure = data[:split_element], data[split_element+1:]
    # list of dict keyed by amount, from and to 
    procedure = [{"amount": int(a), "from": int(f)-1, "to": int(t)-1} for a, f, t in \
                [re.match(r"^move ([0-9]*) from ([0-9]*) to ([0-9]*)", dp).groups() \
                for dp in data_procedure]]
    # list of lists of letters marking crates
    stacks = [list(s) for s in \
              list(np.transpose(np.array([[dc[pos] for pos in range(1, len(dc), 4)] \
                                          for dc in data_crates[:-1]])))]
    # delete empty elements
    crates = [[element for element in stack if element != ' '][::-1] for stack in stacks]


# UTILITY FUNCTIONS
def perform_step_CrateMover_9000(step, crates_state):
    a, f, t = step['amount'], step['from'], step['to']

    for _ in range(a):
        crates_state[t].append(crates_state[f].pop())

    return crates_state

def perform_step_CrateMover_9001(step, crates_state):
    a, f, t = step['amount'], step['from'], step['to']

    crates2move = []
    for _ in range(a):
        crates2move.append(crates_state[f].pop())

    crates_state[t] += crates2move[::-1]

    return crates_state


def star1():
    # nested list needs deep copy so not only outer shell will be copied
    state = copy.deepcopy(crates)

    for step in procedure:
        state = perform_step_CrateMover_9000(step, state)
    
    print(reduce(lambda x, y: x+y, [c[-1] for c in state]))

def star2():
    state2 = copy.deepcopy(crates)

    for step in procedure:
        state2 = perform_step_CrateMover_9001(step, state2)

    print(reduce(lambda x, y: x+y, [c[-1] for c in state2]))


star1()
star2()