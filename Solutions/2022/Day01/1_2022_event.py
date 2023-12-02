# ADVENT OF CODE 2022
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 1

# PARAMETERS
data_path = "1_2022_data.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')


def star1():
    calories_list = [0]

    i = 0
    for d in data:
        if d != "":
            calories_list[i] += int(d)
        else:
            i += 1
            calories_list.append(0)

    print(max(calories_list))

    return(calories_list)


def star2():

    elfs = star1()
    resoult = [0, 0, 0]

    for i in range(3):
         resoult[i] = elfs.pop(elfs.index(max(elfs)))

    print(sum(resoult))


star1()
star2()