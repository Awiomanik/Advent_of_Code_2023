# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: (solution from 02.12.2022)

# PARAMETERS
data_path = "2_2022_data.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')

def data2list(data):
    opp = [s[0] for s in data]
    you = [s[2] for s in data]

    return you, opp

def translate(a):
    if a == 'A': return 0
    if a == 'B': return 1
    if a == 'C': return 2

def tactic1(a, x):
    if x == 'X': return 0
    if x == 'Y': return 1
    if x == 'Z': return 2

def tactic2(a, x):
    if x == 'X': return (a-1)%3
    if x == 'Y': return a
    if x == 'Z': return (a+1)%3

def calculate_score(opp, you):
    resoult = 0

    for y, o in zip(you, opp):
        resoult += round_score(y, o)
        #print(o, y, round_score(y, o))
    
    return resoult

def round_score(you, opp):
    return (you - opp + 1)%3 * 3 + you + 1


def star1():
    you, opp = data2list(data)
    
    opp = [translate(o) for o in opp]
    you = [tactic1(o, y) for o, y in zip(opp, you)]
    #print(you, opp)

    print(calculate_score(opp, you))

def star2():
    you, opp = data2list(data)

    opp = [translate(o) for o in opp]
    you = [tactic2(o, y) for o, y in zip(opp, you)]
    #print(you,opp)

    print(calculate_score(opp, you))

# A - ROCK
# B - PAPER
# C - SCISSORS

star1()
star2()