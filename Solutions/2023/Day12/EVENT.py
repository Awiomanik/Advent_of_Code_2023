# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 12

from multiprocessing import Pool
import os
from tqdm import tqdm
import time
import shutil

# PARAMETERS
data_path = "DATA.txt"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')


# UTILITY FUNCTIONS
# data
def data2list_key(char):
    if char == '#': return -1
    if char == '.': return 1
    return 0

def data2lists():
    '''
    Returns list of tuples with two lists, list of springs as -1, 0, 1 
    and list of sequences of operational springs as intigers
    '''
    #print("Data2list")
    return [([data2list_key(spring) for spring in springs_numbers.split(' ')[0]], \
             [int(number) for number in springs_numbers.split(' ')[1].split(',')]) \
                for springs_numbers in data]

def unfold_records(records, times=5):
    #print("Unfold records")
    #print(records)
    if times == 1: return records 
    return [(((record[0]+[0])*times)[:-1], record[1]*times) for record in records] 

def sequence_record(record):
    sequence = []
    sequences = []
    flag = False
    #print("sequence record in:")
    #print(record)

    # iterate over springs
    for s in record[0]:
        # if spring is 1 and previously was -1 or 0, start a new sequence
        if s == 1 and flag:
            sequences.append(sequence)
            sequence = []
            flag = False

        sequence.append(s)

        # if spring is -1 or 0, set flag to True
        if s == -1 or s == 0:
            flag = True

    # append remaining springs
    if sequence:
        sequences.append(sequence)

    #print("sequence record out:")
    #print((sequences, record[1]))
    #print()
    return sequences, record[1]


# basic version
def check_validity(springs, valid):
    '''Return True if springs valid else False'''
    # set variables
    current_counter = 0
    counter = []

    # create list of operational springs
    for spring in springs:
        # count subsequent operational springs
        if spring == -1:
            current_counter += 1
        # if non operational spring encountered
        elif spring == 1:
            # if current not subsequent non operational
            if current_counter != 0:
                counter.append(current_counter)
                current_counter = 0
    # if any remainning operational springs
    if current_counter != 0:
        counter.append(current_counter)

    return counter == valid

def count_valid_arrangments(current_arrangment, valid, index=0):
    '''Counts valid arrangments'''

    # recursion escape condition
    if not 0 in current_arrangment:
        return 1 if check_validity(current_arrangment, valid) else 0

    # generate arrangments recrsively
    counter = 0
    if current_arrangment[index] == 0:
        for spring in [1, -1]:
            current_arrangment[index] = spring
            counter += count_valid_arrangments(current_arrangment, valid, index+1)
            # return current_arrangment to previous state
            current_arrangment[index] = 0
    else:
        counter += count_valid_arrangments(current_arrangment, valid, index+1)

    return counter

def pruning_check(springs, valid):
    '''Return True if springs valid till first 0 else False'''
    current_counter = 0
    valid_index = 0

    for spring in springs:
        if spring == -1:
            current_counter += 1
        elif spring == 1:
            if current_counter != 0:
                if valid_index >= len(valid) \
                or current_counter > valid[valid_index]:
                    return True
                valid_index += 1
                current_counter = 0
        elif spring == 0:
            break

    if current_counter != 0:
        if valid_index >= len(valid) \
        or current_counter > valid[valid_index]:
            return True

    return False

def count_valid_arrangments_with_pruning(current_arrangment, valid, index=0):
    '''Counts valid arrangments, prunes invalid branches ahead'''

    # prunning
    if pruning_check(current_arrangment, valid):
        #print("\nPRUNNING", current_arrangment, valid)
        return 0

    # Recursion escape condition
    if not 0 in current_arrangment:
        return 1 if check_validity(current_arrangment, valid) else 0

    # generate arrangments recrsively
    counter = 0
    if current_arrangment[index] == 0:
        for spring in [1, -1]:
            current_arrangment[index] = spring
            counter += count_valid_arrangments_with_pruning(current_arrangment, valid, index+1)
            # return current_arrangment to previous state
            current_arrangment[index] = 0
    else:
        counter += count_valid_arrangments_with_pruning(current_arrangment, valid, index+1)

    return counter

# bitwise version
def count_valid_arrangments_bitwise(operational, damaged, valid, length, index=0):
    '''Counts valid arrangments, prunes invalid branches ahead, uses bitwise representation'''

    # prunning
    if pruning_check_bitwise(operational, damaged, valid, length):
        return 0

    # Recursion escape condition
    if index == length:
        #print(bin(operational), length)
        return 1 if check_validity_bitwise(damaged, valid, length) else 0

    # generate arrangments recrsively
    counter = 0
    bit_mask = 1 << index
    # if current spring's status is known
    if operational & bit_mask or damaged & bit_mask:
        # move to next bit
        counter += count_valid_arrangments_bitwise(operational, damaged, valid, length, index+1)
    else:
        # set to operational and recurse
        counter += count_valid_arrangments_bitwise(operational | bit_mask, damaged, valid, length, index+1)
        # set to damaged and recurse
        counter += count_valid_arrangments_bitwise(operational, damaged | bit_mask, valid, length, index+1)

    return counter

def check_validity_bitwise(damaged, valid, length):
    current_counter = 0
    counter = []
    bit_mask = 1

    # loop through springs and populate counter
    for _ in range(length):
        if damaged & bit_mask:
            current_counter += 1
        elif current_counter != 0:
            counter.append(current_counter)
            current_counter = 0
        bit_mask <<= 1

    # Check for any remaining operational springs
    if current_counter != 0:
        counter.append(current_counter)

    return counter == valid

def pruning_check_bitwise(operational, damaged, valid, length):
    ''''''
    # set variables
    current_counter = 0
    valid_index = 0
    bit_mask = 1

    # iterate over springs
    for _ in range(length):
        # encountered dameged spring
        if damaged & bit_mask:
            current_counter += 1
        # encountered operational spring
        elif operational & bit_mask:
            if current_counter != 0:
                # check for pruning 
                if valid_index >= len(valid) \
                or current_counter > valid[valid_index]:
                    return True
                valid_index += 1
                current_counter = 0
        # encountered unset spring
        else: 
            break
        bit_mask <<= 1

    # add remainning springs
    if current_counter != 0:
        # check for pruning
        if valid_index >= len(valid) \
        or current_counter > valid[valid_index]:
            return True

    return False

def list2bit(springs):
    '''
    Returns bitwise representation of springs
    (operational (int), damaged (int), valid (list), length (int))
    '''
    operational = 0
    damaged = 0
    length = len(springs[0])-1
    valid = springs[1]

    for i, s in enumerate(springs[0]):
        if s == 1:
            operational |= (1 << i)
        elif s == -1:
            damaged |= (1 << i)

    return operational, damaged, valid, length

#sequenced version
def check_validity_sequenced(damaged, valid, length):
    current_counter = 0
    counter = []
    bit_mask = 1
    #print("to check (damaged, valid)", bin(damaged), valid)

    # loop through springs and populate counter
    for _ in range(length+1):
        #print("index", _)
        if damaged & bit_mask:
            #print("got in")
            current_counter += 1
        elif current_counter != 0:
            counter.append(current_counter)
            current_counter = 0
        bit_mask <<= 1

    # Check for any remaining operational springs
    if current_counter != 0:
        counter.append(current_counter)

    #print(counter)
    #print(valid)
    #print(valid[:len(counter)])
    #print("Validity:", counter == valid[:len(counter)] and len(counter) != 0)
    counter_length = len(counter)
    return counter == valid[:counter_length] and counter_length != 0, len(counter)

def count_valid_arrangments_sequenced(operational, damaged, valid, length, index=0):
    '''
    Counts valid arrangments in subsequence,
    prunes invalid branches ahead,
    uses bitwise representation

    Returns:
    if sequence is valid:       dictionary keyed by remainning valid list
                                with values representing ombinations per remainning valid
    '''
    print(f"\nEntering count_valid_arrangments_sequenced: Index: {index}, Operational: {bin(operational)}, Damaged: {bin(damaged)}, Valid: {valid}, Length: {length}")

    # Pruning
    if pruning_check_bitwise(operational, damaged, valid, length):
        print("Pruning condition met, returning empty dictionary.")
        return {}

    # Recursion escape condition
    if index == length + 1:
        is_valid, count = check_validity_sequenced(damaged, valid, length)
        print(f"Recursion escape condition met. Is valid: {is_valid}, Count: {count}")
        if is_valid:
            print(f"Returning valid arrangement: {tuple(valid[count:])}")
            return {tuple(valid[count:]): 1}
        else:
            print("Returning empty dictionary as sequence is not valid.")
            return {}

    # Generate arrangements recursively
    bit_mask = 1 << index
    result = {}

    # If current spring's status is known
    if operational & bit_mask or damaged & bit_mask:
        print(f"Known status at index {index}, moving to next bit.")
        result = count_valid_arrangments_sequenced(operational, damaged, valid, length, index + 1)
    else:
        # Set to operational and recurse
        print(f"Setting bit {index} to operational and recursing.")
        result_operational = count_valid_arrangments_sequenced(operational | bit_mask, damaged, valid, length, index + 1)
        
        # Set to damaged and recurse
        print(f"Setting bit {index} to damaged and recursing.")
        result_damaged = count_valid_arrangments_sequenced(operational, damaged | bit_mask, valid, length, index + 1)
        
        # Merge dictionaries
        result = {key: result_damaged.get(key, 0) + result_operational.get(key, 0) for key in set(result_operational) | set(result_damaged)}

    print(f"Returning from count_valid_arrangments_sequenced: {result}")
    return result

def process_sequences_recursively(sequences, valid, index=0, result=None):
    ''''''
    print("\nEntering process_sequences_recursively")
    print("Index:", index, "Sequences:", sequences, "Valid:", valid)

    if not result:
        result = {}
        valid = tuple(valid)

    if index == len(sequences):
        print("Recursion escape with result:", result)
        if valid:
            return result

    current = (sequences[index], list(valid))
    subsequences = count_valid_arrangments_sequenced(*list2bit(current))

    for subvalid in subsequences.keys():
        if subvalid:
            print("Processing subvalid:", subvalid, "with count:", subsequences[subvalid])
            x = process_sequences_recursively(sequences, subvalid, index+1, result)
            x = next(iter(x), 0)
            print("Returned from recursion with x =", x, "for subvalid =", subvalid)
            subsequences[subvalid] *= x

    print("Final subsequences before returning:", subsequences)
    return subsequences.values()

# multiprocessing:
def subprocess_bitwise(spring):
    return count_valid_arrangments_bitwise(*list2bit(spring))

def subprocess_pruning(spring):
    return count_valid_arrangments_with_pruning(spring[0], spring[1])

def subprocess_sequenced(spring):
    ''''didn't work out, to look into later'''
    # memoization do it later ####
    print("subprocess_sequenced")
    print(spring)

    result = []
    for s in spring:
        for r in process_sequences_recursively(*sequence_record(s)):
            result.append(r)
            print("subproces_sequence", result, r)
            print()
        
    return result
            

def star1():
    print("Part 1:")
    print()

    # preapre data
    springs = data2lists()
    counter = 0
    l = len(springs)

    # calculate sum
    for i, s in enumerate(springs):
        percentage = i//10
        print(f"\033[A\r{percentage}% ({i}/{l}), counter =", counter, f"\n[{'#'*(percentage//2)}{' '*(50-(percentage//2))}]", end='')
        counter += count_valid_arrangments_with_pruning(s[0], s[1])
    
    print("\033[A\rDONE", ' '*100,)
    print("Resoult:", counter, ' '*100)
    print()

def star2(loading="bar_counter", algorithm="pruning"):
    '''
    Brute force baby
    loading =   "bar"       |   "counter"   |   "bar_counter"
    algorithm = "bitwise"   |   "pruning"   |   "sequenced" (sequenced still in development)
    '''
    start = time.time()
    print("Part 2:")

    # get number of processors to split the task
    cores = os.cpu_count()
    cores -= 2

    # preapre data
    springs = unfold_records(data2lists(), times=3)
    all_springs=len(springs)

    # choose algorithm
    if algorithm == "bitwise":
        subprocess = subprocess_bitwise
    elif algorithm == "pruning":
        subprocess = subprocess_pruning
    elif algorithm == "sequenced":
        subprocess = subprocess_sequenced

    # display info
    print(f"Available cores: {cores+2}, splitting task into {cores} subprocesses")
    print(f"Using {algorithm} algorithm and {loading} display option") 

    # calculate the sum by calculating parts of initial value range as seperate processes
    counter = 0
    with Pool(processes=cores) as pool:
        # tqdm loading bar
        if loading == 'bar':
            with tqdm(total=all_springs) as bar:
                for c in pool.imap_unordered(subprocess, springs):
                    counter += c
                    bar.update()      
        else:
            i = 0
            for c in pool.imap_unordered(subprocess, springs):
                counter += c
                i += 1
                # counter
                if loading == "counter":
                    print(f"{i}:\tcounter = {counter},\tc = {c}")
                # personal loading bar
                else:
                    current_time = time.time()
                    percentage = int(i/all_springs * 100)
                    percent_string = f"| {percentage}%" + (' ' if percentage < 10 else '') + " |"
                    info_string = \
                    f"| {i}/{all_springs} | Current counter = {counter} | Average time = {(current_time - start)/i:.2f}s |"
                    loading_bar_size = shutil.get_terminal_size()[0] - len(percent_string) - len(info_string) - 2
                    print("\r" + percent_string + \
                          '\u25B0' * (int(percentage / 100 * loading_bar_size)) + \
                          '\u2550' * (int((100 - percentage) / 100 * loading_bar_size)) + \
                            info_string, end='')

    # time display
    end = time.time()
    time_passed = end - start
    if time_passed > 60:
        min = time_passed//60
        sec = time_passed%60
        time_passed = f"{min:.0f}min {sec:.0f}s"
    else:
        time_passed = f"{time_passed:.2f}" + 's'

    print("\nDone in", time_passed)
    print("Final counter =", counter)

# main
if __name__ == "__main__":
    star1()
    star2() # worst calculation time of all of solutions, 
            # but lucky for me I had access to pretty powerfull machine today,
            # and so I utilized it to the fullest.
            # If you have any ideas how to improve it, please let me know


# Times measured on my machine on other data (testing different approaches) 
# time                              25s
# time with prunning                6 s
# time with memization and pruning  7 s buuuu (I doesn't go the same path twise, so this is just useless additional calculations, it can be improved though)
# time with pruning and pooling     8 s (longer but it takes some time to set it up so I'll give it a chance)
# time bitwise with pruning         7 s
