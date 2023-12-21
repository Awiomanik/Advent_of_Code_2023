# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 4

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    data = [d.split(':')[1].strip() for d in data]


# UTILITY FUNCTIONS
def count_matches(card):
    '''For a given card string returns number of matches'''
    part1, part2 = card.split(" | ")

    winning_nums = set(map(int, part1.split()))
    scrached_nums = set(map(int, part2.split()))
    
    return len(winning_nums.intersection(scrached_nums))

def cards_total(cards):
    '''Loops through cards and adds won copies, returns total number of cards'''
    
    card_counts = [1] * len(cards)
    # new wins for given iteration
    new_cards = [0] * len(cards)  

    for i, card in enumerate(cards):
        matches = count_matches(card)

        # add won cards
        for j in range(i + 1, min(i + 1 + matches, len(cards))):
            new_cards[j] += card_counts[i]

        # Update card counts with new wins and reset new_wins for next iteration
        for j in range(len(cards)):
            card_counts[j] += new_cards[j]
            new_cards[j] = 0

    return sum(card_counts)


def star1():
    print(sum([2**(p-1) if p != 0 else 0 for p in [count_matches(d) for d in data]]), "points won.")

def star2():
    print("Total scrachcard number is", cards_total(data))


star1()
star2()
