import json
import random

import requests

deck_and_card_url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/bgame'
localhost_url = 'http://127.0.0.1:5000/'  # Will change once we upload to Dave's server.


# Assume 2 players in game for now.
class BE_Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_deck = requests.post(deck_and_card_url+deckname)  # Need game_id so you can create the game
        self.player_1 = self.create_player()  # Need to create player class to create player objects like with Card.py?
        self.player_2 = self.create_player()
        #self.dealer = self.assign_initial_dealer()  # need players before we can assign dealer



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

        create_hand_player_1 = requests.post(
            url=localhost_url + 'games/' + str(10101) + '/hands/' + str(hand_dict["hand_id"]),
            data={'hand_info': cards_json_string})

        player_1_hand_info = requests.get(
            url=localhost_url + 'games/' + str(10101) + '/hands/' + str(hand_dict["hand_id"])).text

        print("Hand: ", json.loads(player_1_hand_info))


    def create_player(self):
        # Create the Player using the Hand created above.
        # TODO: assign crib_turn, turn based on dealer attribute.
        player_dict = {"hand": self.create_hand(), "crib_turn": False, "turn": True, "score": 0, "name": "tyler"}
        player_json_string = json.dumps(player_dict)
        create_player_1 = requests.post(url=localhost_url + 'games/' + str(10101) + '/players/' + player_dict["name"],
                                        data={'player_info': player_json_string})

        get_player = requests.get(url=localhost_url + 'games/' + str(10101) + '/players/' + player_dict["name"])
        print()
        print("Player: ", json.loads(get_player.text))
        print()




    # Choose a random number between 1 and 13, whichever player gets a LOWER number will be auto assigned to be the dealer -ACE IS 1
    # Crib belongs to the dealer, so assign dealer, then set crib-turn = True
    # Non-dealer picks starting card and goes first with the pegging round.
    def assign_initial_dealer(self):
        num1 = random.randint(1,13)
        num2 = random.randint(1,13)
        if num1 <= num2:
            self.dealer = self.player_1
        else:
            self.dealer = self.player_2
        print("dealer is: ", self.dealer)
        return self.dealer

    # Don't think we need this - this happens when we call to get cards from PCMS server
    def get_player_cards(self):
        pass

    # Don't think we need this - this happens when we call to get cards from PCMS server
    def deal_cards(self):
        pass

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
    return random.randint(1, 10000)

# Same as hand_id except with game_id's
def create_random_game_id():
    return random.randint(1, 10000)


new_game = BE_Game(create_random_game_id())
requests.delete(deck_and_card_url+deckname)

