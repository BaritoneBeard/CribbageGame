import json
import random
import requests


# should Player_BE also have the methods that Player has in frontend? or just attributes?
class Player_BE():
    def __init__(self, player_hand, crib_turn, turn, name, score):
        # player_hand is a Hand with its own id, so in a way, it is attached to a specific player
        self.hand = player_hand
        self.score = score  # 0 for a player just starting out.
        self.crib_turn = crib_turn
        self.turn = turn
        self.name = name
