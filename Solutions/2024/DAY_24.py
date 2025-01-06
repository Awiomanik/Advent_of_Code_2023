"""
Advent of Code 2024 - Day 24

This script contains my solution for **Advent of Code 2024, Day 24**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_24_input.txt` located in the same directory as this script.
- Example: `python DAY_24.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from time import time
from itertools import combinations
from copy import deepcopy

# Get data
data = open("day_24_input.dat").read()
values, gates = data.split('\n\n')
values: dict[str, bool] = {line.split(': ')[0]: line.split(': ')[1] == '1' for line in values.split('\n')}
gates: dict[tuple[str, str, int], tuple[str, str]] = {
    (gate.split(' ')[0], gate.split(' ')[2], i): 
    (gate.split(' ')[1], gate.split(' ')[4]) 
        for i, gate in enumerate(gates.split('\n'))}

def calculate_sum(gates: dict[tuple[str, str, int], tuple[str, str]], values: dict[str, bool]) -> int:
    calculating = True
    while calculating:

        calculating = False
        for (in1, in2, _), (operator, out) in gates.items():
            if (in1 in values) and (in2 in values) and (out not in values):
                if operator == 'AND':
                    values[out] = values[in1] and values[in2]
                if operator == 'OR':
                    values[out] = values[in1] or values[in2]
                if operator == 'XOR':
                    values[out] = values[in1] != values[in2]
                
                calculating = True

    bits: str = ''
    for wire, val in sorted(values.items())[::-1]:
        if wire.startswith('z'):
            bits += str(int(val))

    return int(bits, 2)

def create_indexed_dict(x: int, y: int, x_len: int, y_len: int) -> dict[str, bool]:
    """
    Creates a dictionary with keys as x01, x02, ..., y01, y02, ...
    and values as the bits of x and y, respectively.

    Args:
    - x (int): Integer whose bits are mapped to x-prefixed keys.
    - y (int): Integer whose bits are mapped to y-prefixed keys.
    - x_len (int): Number of x-prefixed keys to generate.
    - y_len (int): Number of y-prefixed keys to generate.

    Returns:
    - dict[str, bool]: A dictionary mapping keys to bit values.
    """
    values = {}

    # Convert x and y into binary strings with leading zeros
    x_bin = f"{x:0{x_len}b}"[-x_len:][::-1]  # Ensure exactly x_len bits
    y_bin = f"{y:0{y_len}b}"[-y_len:][::-1]  # Ensure exactly y_len bits

    # Map x bits to x-prefixed keys
    for i, bit in enumerate(x_bin, start=1):
        values[f"x{i:02d}"] = bit == "1"  # True for '1', False for '0'

    # Map y bits to y-prefixed keys
    for i, bit in enumerate(y_bin, start=1):
        values[f"y{i:02d}"] = bit == "1"  # True for '1', False for '0'

    return values


# < --- 1'st STAR --- >
start = time()

print("\n1'st star solution:\n")
print(calculate_sum(gates, values))
print(f"Solution found in {time() - start:.2f}s")


# < --- 2'nd STAR --- >
start = time()
x_len = len([val for val in values if val.startswith('x')])
y_len = len([val for val in values if val.startswith('y')])

gates_listed = list(gates.items())
print(gates)
print("Number:", len(tuple(combinations(combinations(range(len(gates)), 2), 2))))
for (index1, index2), (index3, index4) in combinations(combinations(range(len(gates)), 2), 2):
    gates_temp = deepcopy(gates)
    gates_temp[gates_listed[index1][0]] = (gates_listed[index1][1][0], gates_listed[index2][1][1])
    gates_temp[gates_listed[index2][0]] = (gates_listed[index2][1][0], gates_listed[index2][1][1])
    gates_temp[gates_listed[index3][0]] = (gates_listed[index4][1][0], gates_listed[index2][1][0])
    gates_temp[gates_listed[index4][0]] = (gates_listed[index4][1][0], gates_listed[index3][1][1])
    
    found = True
    for x, y in [(11, 13), (12, 73), (0, 0), (9999, 0), (2, 4), (84, 293748), (38724, 3439847)]:
        values = create_indexed_dict(x, y, x_len, y_len)
        if (gates_listed[index2][1][1], gates_listed[index1][1][1]) == ('z02', 'z05'):
            print(gates_temp)
            print()
            print(values)
            print()
        if x + y != calculate_sum(gates_temp, values):
            print("NOT FOUND!")
            print(x, y, calculate_sum(gates_temp, values))
            print(gates_listed[index2][1][1], gates_listed[index1][1][1])
            print(gates_listed[index4][1][1], gates_listed[index3][1][1])
            print()
            found = False
            break
        else:
            print("\nFOUND:\nx, y =", x, y)
            print(gates)
            print(values)


print("\n2'nd star solution:\n")
print()
print(f"Solution found in {time() - start:.2f}s")