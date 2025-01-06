"""
Advent of Code 2024 - Day 17

This script contains my solution for **Advent of Code 2024, Day 17**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_17_input.txt` located in the same directory as this script.
- Example: `python DAY_17.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from typing import Callable

# Get data
data = open("day_17_input.dat").read().split('\n\n')
register: dict[str, int] = {reg.split(' ')[1][0]: int(reg.split(' ')[2]) for reg in data[0].split('\n')}
original_registers: dict[str, int] = register
program: list[int] = [int(x) for x in data[1].split(' ')[1].split(',')]
output_list: list[int] = []

# Operands
operands: dict[int, Callable] = {0: lambda: 0, 1: lambda: 1, 2: lambda: 2, 3: lambda: 3, 
        4: lambda: register.get('A'), 5: lambda: register.get('B'), 6: lambda: register.get('C')}

# Instructions
instruction_pointer = 0
def adv(x: int): 
    register['A'] = int(register['A'] / (2 ** operands[x]()))
def bxl(x: int): 
    register['B'] = register['B'] ^ x
def bst(x: int): 
    register['B'] = operands[x]() % 8
def jzn(x: int): 
    global instruction_pointer
    instruction_pointer = x - 2 if register['A'] != 0 else instruction_pointer
def bxc(x: int): 
    register['B'] = register['B'] ^ register['C']
def out(x: int): 
    output_list.append(operands[x]() % 8)
def bdv(x: int): 
    register['B'] = int(register['A'] / (2 ** operands[x]()))
def cdv(x: int): 
    register['C'] = int(register['A'] / (2 ** operands[x]()))

opcodes: dict[int, Callable] = {0: adv, 1: bxl, 2: bst, 3: jzn, 4: bxc, 5: out, 6: bdv, 7:cdv}

# Run program
def run_program():
    """Runs the program and returns the output list."""
    global instruction_pointer, register, output_list

    # Execute program
    while instruction_pointer < len(program):
        opcodes[program[instruction_pointer]](program[instruction_pointer + 1])
        instruction_pointer += 2

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
run_program()
print(','.join(str(x) for x in output_list))

# < --- 2'nd STAR --- >
print("\n2'st star solution:\n")
print("Calculating...", end='\r')

# Step 1: Finding the initial search range
candidate = 1
step = 1
lower_bound = None
upper_bound = None
search_range = None
while True:
    # Reset values
    instruction_pointer = 0
    output_list = []
    register = original_registers
    register['A'] = candidate

    # Get program output
    run_program()

    # Check output length
    if lower_bound is None and len(output_list) == len(program):
        lower_bound = candidate

    if len(output_list) > len(program):
        upper_bound = candidate - step
        search_range = upper_bound - lower_bound
        break

    candidate *= 2

# Step 2: Finding solution
candidate = lower_bound
step = search_range // 32  # Initial step
best = 0
while True:
    candidate += step
    # Reset values
    instruction_pointer = 0
    output_list = []
    register = original_registers
    register['A'] = candidate

    # Get program output
    run_program()

    if program == output_list:
        break

    # Count matching values
    current_matched = 0
    for o, p in zip(output_list[::-1], program[::-1]):
        if o == p:
            current_matched += 1
        else:
            break

    # Reduce step
    if current_matched > best:
        best = current_matched
        step = max(step // 8, 1)

print(candidate)