"""
Advent of Code 2024 - Day 5

This script contains my solution for **Advent of Code 2024, Day 5**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_5_input.txt` located in the same directory as this script.
- Example: `python DAY_5.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

data = open("day_5_input.dat").read()
rules, updates = (x.split('\n') for x in data.split("\n\n"))
rules = [list(int(page) for page in rule.split('|')) for rule in rules]
updates = [list(int(page) for page in update.split(',')) for update in updates]
rule_set = {(rule[0], rule[1]): 1 for rule in rules} | {(rule[1], rule[0]): -1 for rule in rules}

# 1'st STAR
counter = 0
invalid_updates = []
for update in updates:
    wheter_update_not_valid = False

    for page_index, page in enumerate(update):
        for other_page_index, other_page in enumerate(update):
            if page_index == other_page_index:
                continue
            
            if (page, other_page) in rule_set and rule_set[(page, other_page)] * (page_index - other_page_index) > 0:
                wheter_update_not_valid = True
                break
                
        if wheter_update_not_valid: break
    
    if not wheter_update_not_valid:
        counter += update[len(update) // 2]
    else:
        invalid_updates.append(update)

print("\n1'st star solution:", counter)

# 2'nd STAR
counter = 0
for invalid_update in invalid_updates:
    valid_up = []

    for page in invalid_update:
        index = 0
        for val_page in valid_up:
            if (page, val_page) in rule_set:
                break
            index += 1
        
        valid_up.insert(index, page)

    counter += valid_up[len(valid_up) // 2]

print("\n2'nd star solution:", counter)