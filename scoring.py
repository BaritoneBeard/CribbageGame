import requests
import json
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

def main():
    r = requests.post(url + deckname)
    try:
        r = requests.get(url + deckname + '/cards/4')
       # print(r.content)
        dict = json.loads(r.text)       # list of dictionaries
        # print(dict)
        # print(dict[0]['rank'])
        # print(dict[0]['suit'])
        calc_score(dict)
    except HTTPError as e:              # eventually, make this log
        print("Doesn't work as intended yet")
    finally:
        r = requests.delete(url+deckname)
        print("\ndeleted, program finished")

main()

