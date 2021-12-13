import json
from Player_BE import Player_BE
import requests

deck_and_card_url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/bgame'
localhost_url = 'http://127.0.0.1:5000/'
game_id_list = []
hand_id_list = []

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


def main():
    pass
    # game_id = create_random_game_id()
    # new_game = BE_Game(game_id)  # Create a new game with a random game_id
    # requests.delete(deck_and_card_url+deckname)

if __name__ == '__main__':
    main()

