import requests
import json
import itertools
from urllib.error import HTTPError

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'
p1_score = 0
p2_score = 0

'''
    Rules referenced:
    15 	2 points 	Each combination that adds up to 15 is worth 2 points (no matter how many cards are involved).
    Pair 	2 points 	Each pair is worth 2 points
    Pair Royal 	6 points 	Three of a kind
    Double Pair Royal 	12 points 	Four of a kind
    Run 	1 point per card 	Cards in consecutive order (i.e. – 5-6-7-8)
    Four Card Flush 	4 points 	All four cards in your hand are of the same suit (sometimes the four-card flush does not count, see below)
    Five Card Flush 	5 points 	All five cards in your hand (and using the starter) are the same suit
    Go 	1 point 	The last player to lay a card
    Nobs 	1 point 	Jack of the same suit as the starter. Referred to as “One for his nobs/nob” in the United Kingdom.
'''


'''
    Checks each combination of cards and adds 2 to total for each combination found that equals exactly 15.
    Starts with two card combos, then goes to 3, 4, 5...
    Ensures no duplicates, for example, a hand with cards 4,5,6 could have 4,5,6 , 5,4,6 , 6,5,4 ... etc.
'''


def calc_15(nums: list):
    nums.sort()
    score = 0
    repeats = []
    for i in range(2, len(nums)):
        for combo in itertools.combinations(nums, i):  # built in python tool to check each combination of cards
            total = 0
            cards_combined = []  # tracks the combos for this iteration only.
            for card in combo:
                total += card
                cards_combined.append(card)
                if total == 15 and cards_combined not in repeats:  # Without checking for repeats the scores get wonky
                    repeats.append(cards_combined)  # ensures no duplicates
                    score += 2

    return score


'''
    Deletes all cards from incoming list and calculates how many were removed to award points.
    A pair is worth 2 points, 3 of a kind is worth 6, and 4 of a kind is worth 12.
    This relation turns out to be a sequence of n^2 + n.
    If n = 1 : 1^2 + 1 = 1 + 1 = 2
    If n = 2 : 2^2 + 2 = 4 + 2 = 6
    If n = 3 : 3^2 + 3 = 9 + 3 = 12
    Therefore, if n is the number of duplicate cards removed, we have our number of points awarded.
'''


def calc_pairs(card_list: list):
    score = 0
    while card_list:
        head = card_list[0]
        original_size = len(card_list)
        card_list = filter(lambda val: val != head, card_list)  # delete every element that matches head, including head
        card_list = list(card_list)
        n = (original_size - len(card_list)) - 1  # removes duplicates AND the card being compared, so we subtract 1
        score += (n ** 2 + n)  # again, 2, 6, 12
    return score


'''
    Will MOST LIKELY need refactoring when we move on past the mock.
    Calculates score, calls other calc methods.
    Separates data retrieved from the mock into a list of card ranks and suits.
'''


def calc_score(dictionary_list: list):
    score = 0
    rank_list = []
    suit_list = []
    for i in range(len(dictionary_list)):
        rank_list.append(dictionary_list[i]['rank'])
        suit_list.append(dictionary_list[i]['suit'])

    # rank_list.sort()
    # suit_list.sort()
    print(rank_list)
    print("\n", suit_list)
    # print(calc_15(rank_list))
    # print(calc_pairs(rank_list))
    score += calc_15(rank_list)
    score += calc_pairs(rank_list)


'''
    Main: tries to create a deck and collect cards from the top.
    I elected to have this draw 8 cards to get a good selection of cards to send to the functions.
'''


def main():
    r = requests.post(url + deckname)
    try:
        r = requests.get(url + deckname + '/cards/8')
        # print(r.content)
        dict = json.loads(r.text)  # list of dictionaries
        # print(dict)
        # print(dict[0]['rank'])
        # print(dict[0]['suit'])
        calc_score(dict[1:6])  # These cards are the only ones of the 8 drawn that have a 15, somehow.
    except HTTPError as e:  # eventually, make this log
        print("Doesn't work as intended yet")
    finally:
        r = requests.delete(url + deckname)
        print("\ndeleted, program finished")


if __name__ == '__main__':
    main()
