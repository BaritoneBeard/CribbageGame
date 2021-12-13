import json
import random
from Player_BE import Player_BE
import requests

deck_and_card_url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/bgame'
localhost_url = 'http://127.0.0.1:5000/'  # Will change once we upload to Dave's server.
game_id_list = []
hand_id_list = []

# Other BE classes like scoring and pegging can call to BE_Game and access its players for scores, turns, etc.

# Assume 2 players in game for now.
class BE_Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_deck = requests.post(deck_and_card_url+deckname)  # Remains null until Game POST is called.
        self.player_1 = None  # Remains null until a player is asked to be created.
        self.player_2 = None
        self.starter_card = json.loads(requests.get(deck_and_card_url+deckname+'/cards/1').text)[0]
        self.crib_list = []

    # Calls the PCMS server and returns a list of card dictionaries.
    def create_hand(self):
        player_hand = requests.get(deck_and_card_url + deckname + '/cards/6')  # returns a response obj of list of card_dicts
        player_hand_dict = json.loads(player_hand.text)  # returns as list of card_dicts

        return player_hand_dict  # Not a response object.

    # Determines which players are not active and creates a backend player object (Ex. if p1 is None, create p1)
    def create_player(self, player_name):
        if self.player_1 is None:
            self.player_1 = Player_BE(self.create_hand(), player_name, 0)
        elif self.player_2 is None:
            self.player_2 = Player_BE(self.create_hand(), player_name, 0)

    # Don't need this - here just in case.
    def get_crib_cards(self):
        pass

    # I don't really know how this one is going to work
    # We need to be checking every 1 second whether someone tried to connect to our game.
    def player_joined(self):
        pass


# Selects a random number from 1 to 10000, adds it to a global list of hand_id's
# checks to make sure we haven't used it yet and returns it
# Maybe join specific URL endpoint based on game_id ('games/<int:game_id/join')
def create_random_hand_id():
    id = random.randint(1,10000)
    while True:
        if id in hand_id_list:
            id = random.randint(1,10000)
        else:
            return id


# Same as hand_id except with game_id's
def create_random_game_id():
    id = random.randint(1,10000)
    while True:
        if id in game_id_list:
            id = random.randint(1,10000)
        else:
            return id


def main():
    pass
    # game_id = create_random_game_id()
    # new_game = BE_Game(game_id)  # Create a new game with a random game_id
    # requests.delete(deck_and_card_url+deckname)

if __name__ == '__main__':
    main()

