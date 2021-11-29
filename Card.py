import requests
import json
from urllib.error import HTTPError

url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/tdn'

rank_list = {1: 'ace', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
             8: '8', 9: '9', 10: '10', 11: 'Jack', 12: 'Queen', 13: 'King'}

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        # self.name = name

    def print_card(self):
        print(rank_list[self.rank], "of", self.suit)


def make_card(card_dict: dict):
    card = Card(card_dict['rank'], card_dict['suit'])
    return card
