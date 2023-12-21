# personal loading bar
# by Wojciech Kośnik-Kowalczuk

# check how importing works in a context of modules and exchanging information
# build it as a class 

import shutil

def loading_bar_init():
    pass

def loading_bar_update(start, i, total, additional_info=None):
    '''
    Updates loading bar
    Input:
    start           starting time in seconds (int)
    i               current iteration (indexing from 1!) (int)
    total           number of all calculations (int)
    additional_info additional info about current state (string)
    '''
    # initialize nmerical variables
    current_time = time.time()
    percentage = int(i/total * 100)

    # initialize strings
    percent_string = f"| {percentage}% |"
    info_string = f"| {i}/{total} | " + \
                  ((additional_info + " | ") if additional_info else '') + \
                  f"Average time = {(current_time - start)/i:.2f}s |"
        # make time show min or nanosec if necessary
        ############################################

    # initialize size
    loading_bar_size = shutil.get_terminal_size()[0] - len(percent_string) - len(info_string) - 2

    # print
    print("\r" + percent_string + \
            '\u25B0' * (int(percentage / 100 * loading_bar_size)) + \
            '\u2550' * (int((100 - percentage) / 100 * loading_bar_size)) + \
            info_string, end='')
    
def loading_bar_close():
    pass