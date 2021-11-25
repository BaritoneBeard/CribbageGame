import requests
import json
import itertools
from urllib.error import HTTPError

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'
p1_score = 0
p2_score = 0

'''
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

def calc_15(nums:list):
    score = 0
    repeats = []
    for i in range(2, len(nums)):
        for combo in itertools.combinations(nums,i):    # built in python tool to check each combination of cards
            total = 0
            debug = []
            for card in combo:
                total += card
                debug.append(card)
                if total == 15 and debug not in repeats:    # Without checking for repeats the scores get wonky
                    repeats.append(debug)
                    # print(debug)
                    score += 2

    return score



def calc_score(dictionary_list:list):
    rank_list = []
    suit_list = []
    for i in range(len(dictionary_list)):
        rank_list.append(dictionary_list[i]['rank'])
        suit_list.append(dictionary_list[i]['suit'])
    rank_list.sort()
    suit_list.sort()
    print(rank_list)
    print("\n", suit_list)
    print(calc_15(rank_list))

def main():
    r = requests.post(url + deckname)
    try:
        r = requests.get(url + deckname + '/cards/8')
       # print(r.content)
        dict = json.loads(r.text)       # list of dictionaries
        # print(dict)
        # print(dict[0]['rank'])
        # print(dict[0]['suit'])
        calc_score(dict[1:6])           # These cards are the only ones of the 8 drawn that have a 15, somehow.
    except HTTPError as e:              # eventually, make this log
        print("Doesn't work as intended yet")
    finally:
        r = requests.delete(url+deckname)
        print("\ndeleted, program finished")

if __name__ == '__main__':
    main()

