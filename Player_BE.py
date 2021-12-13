import json
import random
import requests


# crib_turn and turn will be taken care of on the frontend. Might need that info though for scoring
class Player_BE():
    def __init__(self, player_hand, name, score):
        self.hand = player_hand  # a list of card dictionaries.
        self.score = score  # 0 for a player just starting out.
        self.name = name
        # self.crib_turn = crib_turn
        # self.turn = turn
