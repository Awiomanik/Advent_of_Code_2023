"""
Advent of Code 2024 - Day 13

This script contains my solution for **Advent of Code 2024, Day 13**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_13_input.txt` located in the same directory as this script.
- Example: `python DAY_13.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

# Get data
data = open("day_13_input.dat").read().split('\n')
prizes: list[dict[str, tuple[int, int]]] = [
    {'A': (int(data[line    ].split('+')[1].split(',')[0]), int(data[line    ].split('+')[2])), 
     'B': (int(data[line + 1].split('+')[1].split(',')[0]), int(data[line + 1].split('+')[2])), 
     'P': (int(data[line + 2].split('=')[1].split(',')[0]), int(data[line + 2].split('=')[2]))} 
        for line in range(0, len(data), 4)]

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")

counter = 0
for prize in prizes:
    # Let's unpack some stuff
    x: int = prize['P'][0]
    Ax: int = prize['A'][0]
    Bx: int = prize['B'][0]
    Bm: int = 0

    y: int = prize['P'][1]
    Ay: int = prize['A'][1]
    By: int = prize['B'][1]

    candidates: list[tuple[int, int]] = []

    # Brute force time! Let's find all Bm values that satisfy the first equation.
    while Bm * Bx <= x:
        mA = (x - (Bm * Bx)) / Ax

        if mA // 1 == mA:
            candidates.append((int(mA), Bm))
            # print(f"{x} = {int(mA)}*{Ax} + {Bm}*{Bx} = {int(mA*Ax)} + {Bm*Bx}")

        Bm += 1

    # Time to sieve the candidates so only the worthy ones remain.
    nominees: list[tuple[int, int]] = [(Am, Bm) for Am, Bm in candidates if y != Am * Ay + Bm * By]

    # Now, let’s find the cheapest pair. Budget-friendly solution, please!
    sorted(nominees, key=lambda coords: coords[1])

    # And account for it in our grand total.
    if nominees: counter += nominees[0][0] * 3 + nominees[0][1]

print(counter)


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")

# Add 10000000000000 to prizes
increment: int = 10000000000000
for i in range(len(prizes)):
    prizes[i]['P'] = (prizes[i]['P'][0] + increment, prizes[i]['P'][1] + increment)

counter = 0
for prize in prizes:
    # Unfortunately, it's time to use linear algebra again.
    # Alright, here's what's given:
    x = prize['P'][0]
    Ax = prize['A'][0]
    Bx = prize['B'][0]
    # And:
    y = prize['P'][1]
    Ay = prize['A'][1]
    By = prize['B'][1]
    # We can write a system of equations:
    #
    # / x = Ax * Am + Bx * Bm
    # \ y = Ay * Am + By * Bm
    #
    # where Am and Bm are the unknowns.
    # We can rearrange the first equation to get:
    #
    # Ax * Am = x - Bx * Bm
    # Am = (x - Bx * Bm) / Ax
    # 
    # We can substitute the Am component into the second equation to get:
    # 
    # y = Ay * (x - Bx * Bm) / Ax + By * Bm
    # 
    # From that, we can obtain the Bm component:
    #
    # y * Ax = Ay * (x - Bx * Bm) + By * Bm * Ax
    # y * Ax = Ay * x - Bx * Bm * Ay + By * Bm * Ax
    # y * Ax - x * Ay = Bm * By - Bm * Bx * Ay = Bm * (By * Ax - Bx * Ay)
    Bm = (y * Ax - x * Ay) / (By * Ax - Bx * Ay)
    # 
    # Now we can substitute Bm into the second equation to obtain Am:
    #
    # y = Ay * Am + By * Bm
    # Ay * Am = y - By * Bm
    Am = (y - By * Bm) / Ay
    #
    # Finally, if our solution is Diophantine we can increment the counter
    if Am.is_integer() and Bm.is_integer(): counter += int(Am * 3 + Bm)

print(counter)