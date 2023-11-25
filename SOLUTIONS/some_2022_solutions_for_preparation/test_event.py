# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: (test event from 2022)

# PARAMETERS
data_path = "test_data.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')

def l2p(l):
    '''Change letters into priority values'''
    n = ord(l)
    return n - 38 if n < 91 else n -96

def star1():
    sack = []
    item_list = []
    # Make list of sacks
    for s in data:
        s_len = len(s)//2
        sack.append([s[:s_len], s[s_len:]])
    
    # Make list of repeting items
    for i, _ in  enumerate(sack):
        for item in sack[i][0]:
            if item in sack[i][1]:
                item_list.append(l2p(item))
                break
    
    print(sum(item_list))

def star2():
    badge = []
    # Make list of gropus
    group = [data[3*i:3*i+3] for i in range(len(data)//3)]
    # Make list of repeting items
    for g in group:
            for item in g[0]:
                if item in g[1] and item in g[2]:
                    badge.append(l2p(item))
                    break

    #print("Data:\n", data)
    #print("GROUP:\n", group)
    #print("BADGE:\n", badge)
    print(sum(badge))


star1()
star2()