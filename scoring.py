import requests
import json
import itertools
import Card
from urllib.error import HTTPError

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'

'''
    Rules referenced:
    15 	2 points 	Each combination that adds up to 15 is worth 2 points (no matter how many cards are involved).
    Pair 	2 points 	Each pair is worth 2 points
    Pair Royal 	6 points 	Three of a kind
    Double Pair Royal 	12 points 	Four of a kind
    Run 	1 point per card 	Cards in consecutive order (i.e. – 5-6-7-8)
    Four Card Flush 	4 points 	All four cards in your hand are of the same suit 
    Five Card Flush 	5 points 	All five cards in your hand (and using the starter) are the same suit
    Go 	1 point 	The last player to lay a card
    Nobs 	1 point 	Jack of the same suit as the starter. Referred to as “One for his nobs/nob” in the United Kingdom.
'''


'''
    Helper functions for stripping lists of cards into lists of ranks or suits depending on the needs of the function
'''


def extract_ranks(card_list):
    for i in range(len(card_list)):
        if type(card_list[i]) == Card.Card:
            card_list[i] = card_list[i].rank
    return card_list


def extract_suits(card_list):
    for i in range(len(card_list)):
        if type(card_list[i]) == Card.Card:
            card_list[i] = card_list[i].suit
    return card_list


'''
    Checks each combination of cards and adds 2 to total for each combination found that equals exactly 15 or 31.
    Starts with two card combos, then goes to 3, 4, 5...
    Ensures no duplicates, for example, a hand with cards 4,5,6 could have 4,5,6 , 5,4,6 , 6,5,4 ... etc.
'''


def calc_15(card_list: list):    # this is a list of RANKS
    card_list = extract_ranks(card_list)
    card_list.sort()
    score = 0
    repeats = []
    for i in range(2, len(card_list)):
        for combo in itertools.combinations(card_list, i):  # built in python tool to check each combination of cards
            total = 0
            cards_combined = []  # tracks the combos for this iteration only.
            for card in combo:
                if card >= 10:
                    card = 10
                total += card
                cards_combined.append(card)
                if total == 15 and cards_combined not in repeats:
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
    card_list = extract_ranks(card_list)
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
    Calculate how many cards are in a run. If two card ranks are sequential, adds both to a list. 
    Knowing this will cause duplicates, rather than putting more conditional statements I just 
    let the duplicates accrue and then removes them at the end. 
    The actual cards and their ranks don't matter, only how many are in a run. So the program returns the length
    of the list of cards in the run minus all duplicates.
'''


def calc_run(card_list: list):
    card_list = extract_ranks(card_list)
    cards_in_run = []
    card_list.sort()
    current = -1  # If aces are low, aces = 1, so we don't want to give free points just for having an ace.
    for i in card_list:
        if i == current + 1:
            cards_in_run.append(i)
            cards_in_run.append(current)
        else:
            run = len(set(cards_in_run))
            if run < 3:
                cards_in_run.clear()
        current = i
    run = len(set(cards_in_run))    # set() function removes all duplicates
    if run >= 3:
        return run
    else:
        return 0


'''
    Calculates if every suit is the same. The easiest way to do this is remove all duplicates and check if the 
    resulting length of the list is exactly 1.
    In the event that the suit is the same as te flipped card's, adds an extra point.
'''


def calc_flush(card_list: list, flipped_suit: Card = None):
    card_list = extract_suits(card_list)
    if len(set(card_list)) == 1 and len(card_list) == 4:            # flush of 4
        if flipped_suit.suit == card_list[0]:    # flush of 5
            return 5
        else:
            return 4
    else:                                   # no flush
        return 0


'''
    One for this nob: check if jack exists in hand at all, then if it does, check the suit of the flipped card,
    if those match, congrats, you've earned a single point.
    
    if this starts being wonky, we'll have to make a class for cards, which is something I want to avoid only
    because I haven't needed one thus far, so it seems like it would be a waste.
'''


def nob(rank_list: list, suit_list: list, flipped_suit:str):
    if 11 in rank_list:
        if suit_list[rank_list.index(11)] == flipped_suit:
            return 1
        else:
            return 0
    else:
        return 0


'''
    Trivial, but included for the sake of completion.
'''


def go():
    return 1

'''
    Calculates score, calls other calc methods.
    Separates data retrieved from the mock into a list of card ranks and suits.
    This will be what gets called from other files.
'''


def calc_score(list_of_cards:list, flipped_card: Card.Card = None):
    score = 0
    rank_list = []
    suit_list = []
    flipped_suit = None
    if flipped_card:
        flipped_suit = flipped_card.suit
    for i in range(len(list_of_cards)):
        rank_list.append(list_of_cards[i].rank)
        suit_list.append(list_of_cards[i].suit)

    # print(rank_list)
    # print(suit_list, "\n")

    score += calc_15(rank_list)
    score += calc_pairs(rank_list)
    score += calc_run(rank_list)
    score += calc_flush(suit_list, flipped_suit)
    score += nob(rank_list, suit_list, flipped_suit)

    return score
