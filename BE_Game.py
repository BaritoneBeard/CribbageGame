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
        self.game_deck = requests.post(deck_and_card_url+deckname)  # Need game_id so you can create the game
        self.player_1 = self.create_player()  # Player "object" we've created from info on json string from server.
        self.player_2 = self.create_player()
        self.player_3 = None
        self.player_4 = None
        self.dealer = self.assign_initial_dealer()  # need players before we can assign dealer
        self.assign_crib_and_turn()
        self.starter_card = json.loads(requests.get(deck_and_card_url+deckname+'/cards/1').text)[0]
        print("Starting card: ", self.starter_card)

    def create_hand(self):
        list_of_cards = []  # list of card dictionaries.

        # Makes a list of 6 initial cards
        for i in range(6):
            get_card = requests.get(deck_and_card_url + deckname + '/cards/1')
            card_dict = json.loads(get_card.text)
            new_card_dict = card_dict[0]  # For some reason json.loads is loading the card_dict into a single element list, I just want dict
            list_of_cards.append(new_card_dict)

        # Now create a hand_dict to pass in to create a Hand on server.
        # hand_id will be randomly generated here
        hand_dict = {"hand_id": create_random_hand_id(), "card_list": list_of_cards, "cards_on_table": []}
        cards_json_string = json.dumps(hand_dict)  # makes the dictionary of cards into a json string that we pass to the server.

        # TODO: Make BE Card objects using Card.py similar to Player_BE.py?

        create_hand_for_player = requests.post(
            url=localhost_url + 'games/' + str(10101) + '/hands/' + str(hand_dict["hand_id"]),
            data={'hand_info': cards_json_string})

        player_hand_info = requests.get(
            url=localhost_url + 'games/' + str(10101) + '/hands/' + str(hand_dict["hand_id"])).text

        print("Hand: ", json.loads(player_hand_info))
        return json.loads((player_hand_info))


    def create_player(self):
        # Create the Player using the Hand created above.
        # crib_turn and turn will get sorted out once assign_crib_and_turn is called in constructor
        player_dict = {"hand": self.create_hand(), "crib_turn": False, "turn": False, "score": 0, "name": "tyler"}
        player_json_string = json.dumps(player_dict)
        create_player_1 = requests.post(url=localhost_url + 'games/' + str(10101) + '/players/' + player_dict["name"],
                                        data={'player_info': player_json_string})

        # get_player = requests.get(url=localhost_url + 'games/' + str(10101) + '/players/' + player_dict["name"])

        # Got this player information from the server. Create a new player object (for backend only)
        new_player = Player_BE(player_dict["hand"], player_dict["crib_turn"], player_dict["turn"], player_dict["name"])

        return new_player




    # Choose a random number between 1 and 13, whichever player gets a LOWER number will be auto assigned to be the dealer -ACE IS 1
    # Crib belongs to the dealer, so assign dealer, then set crib-turn = True
    # Non-dealer picks starting card and goes first with the pegging round.
    def assign_initial_dealer(self):
        num1 = random.randint(1,13)
        num2 = random.randint(1,13)
        if num1 <= num2:
            return self.player_1
        else:
            return self.player_2

    def assign_crib_and_turn(self):
        if self.dealer is self.player_1: # new player class is all on backend, so creating objects like this is fine.
            self.player_1.crib_turn = True
            self.player_1.turn = False
            self.player_2.crib_turn = False
            self.player_2.turn = True
        else:
            self.player_1.crib_turn = False
            self.player_1.turn = True
            self.player_2.crib_turn = True
            self.player_2.turn = False

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
    game_id = create_random_game_id()
    new_game = BE_Game(game_id)  # Create a new game with a random game_id
    requests.delete(deck_and_card_url+deckname)

if __name__ == '__main__':
    main()

