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
        self.game_deck = None  # Will change
        self.player_1 = self.create_player()
        self.player_2 = self.create_player()
        self.dealer = None  # Will change
        self.starter_card = json.loads(requests.get(deck_and_card_url+deckname+'/cards/1').text)[0]


    # Come back to
    def create_hand(self):
        player_hand = requests.get(deck_and_card_url + deckname + '/cards/6')  # list of card dictionaries.

        # hand_dict = {"hand_id": create_random_hand_id(), "card_list": player_hand, "cards_on_table": []}
        # cards_json_string = json.dumps(hand_dict)  # makes the dictionary of cards into a json string that we pass to the server.
        #
        # return hand_dict


    # Come back to - not accurate
    def create_player(self):
        # Create the Player using the Hand created above.
        player_dict = {"hand": self.create_hand(), "crib_turn": False, "turn": False, "score": 0, "name": "tyler"}
        player_json_string = json.dumps(player_dict)

        new_player = Player_BE(player_dict["hand"], player_dict["crib_turn"], player_dict["turn"], player_dict["name"])

        return new_player


    # Need to be able to call send_cards_to_crib method from player - how?
    def get_crib_cards(self):
        pass

    # I don't really know how this one is going to work
    # We need to be checking every 1 second whether someone tried to connect to our game.
    def player_joined(self):
        pass


# Selects a random number from 1 to 10000, adds it to a global list of hand_id's
# checks to make sure we haven't used it yet and returns it
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

