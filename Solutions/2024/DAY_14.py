"""
Advent of Code 2024 - Day 14

This script contains my solution for **Advent of Code 2024, Day 14**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_14_input.txt` located in the same directory as this script.
- Example: `python DAY_14.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from functools import reduce
from operator import mul

# Get data
data: list[dict[str,tuple[int, int]]] = [{
            'p': tuple(int(x) for x in robot.split(' ')[0][2:].split(',')), 
            'v': tuple(int(x) for x in robot.split(' ')[1][2:].split(','))} 
                for robot in open("day_14_input.dat").read().split('\n')]

WIDTH: int = 101
HEIGHT: int = 103
TIME: int = 100

def move_robot(pos: tuple[int, int], vel: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + vel[0]) % WIDTH, (pos[1] + vel[1]) % HEIGHT

# < --- 1'st STAR --- >
mid_w: int = WIDTH // 2
mid_h: int = HEIGHT // 2

quadrants = [0, 0, 0, 0]

new_state = []
for robot in data:
    pos: tuple[int, int] = robot['p']
    vel: tuple[int, int] = robot['v']

    for sec in range(TIME):
        pos = move_robot(pos, vel)

    x, y = pos
    if x < mid_w:
        if y < mid_h: quadrants[0] += 1
        elif y > mid_h: quadrants[1] += 1
    elif x > mid_w:
        if y < mid_h: quadrants[2] += 1
        elif y > mid_h: quadrants[3] += 1           

print("\n1'st star solution:\n")
print(reduce(mul, quadrants))


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print("Computing...", end='\r')

headquarters: list[bool] = [False] * (WIDTH * HEIGHT)

j: int = 0
searching_for_the_easter_egg: bool = True
while searching_for_the_easter_egg:

    headquarters[:] = [False] * (WIDTH * HEIGHT)

    for robot in data:
        x, y = robot['p']
        robot['p'] = move_robot(robot['p'], robot['v'])
        headquarters[y * WIDTH + x] = True


    for x in range(3, WIDTH - 3):
        for y in range(HEIGHT - 3):
            i: int = y * WIDTH + x

                # Tree tip          ->    ^
            if (headquarters[i] and
                # Tree - firs row   ->   /|\
                headquarters[i + WIDTH] and headquarters[i + WIDTH - 1] and headquarters[i + WIDTH + 1] and
                # tree - second row ->  /|||\
                sum(headquarters[i + 2 * WIDTH + dx] for dx in range(-2, 3)) == 5 and
                # tree - third row  -> /|||||\
                sum(headquarters[i + 3 * WIDTH + dx] for dx in range(-3, 4)) == 7):

                print('\b' * 12, j)
                searching_for_the_easter_egg = False
                break
        else: continue
        break
    
    j += 1