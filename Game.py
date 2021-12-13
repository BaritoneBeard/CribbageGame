import json

import requests
import random

import Card
from Player import Player
from Hand import Hand
from Crib import Crib

base_url = 'http://127.0.0.1:5000/'
deck_and_card_url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/bgame'



class Game:
    def __init__(self):
        # On the backend, you can call to the PCMS server to get your actual hand, then pass back
        self.game_id = None
        self.player_1 = Player(Hand(), False, False, '', 0)
        self.player_2 = Player(Hand(), False, False, '', 0)
        self.dealer = self.assign_initial_dealer()
        self.starter_card = None

        self.crib = Crib(Hand())
        self.table = []

    # Player's GET needs to be called when we do a make_move(). Pegging points get updated as the round goes.
    # But, a player's hand (and crib) gets displayed at the end of the round. So, call GET again once the round is
    # over.

    def start_game(self):

        # Create the game initially, return game_id
        create_game = requests.post(url=base_url+'games')
        game_info = json.loads(create_game.text)
        self.game_id = game_info["game_id"]
        # only need the starter_card because we want to display it to the user - calculations are on backend.
        self.starter_card = game_info["starter_card"]


        # Create the players on the backend and return their hands.
        self.player_1.get_player_name()
        self.player_2.get_player_name()

        create_player_1 = requests.post(url=base_url+'games/'+str(self.game_id)+'/'+self.player_1.name)
        player_1_hand = json.loads(create_player_1.text)  # Supposed to convert json string to dictionary.
        create_player_2 = requests.post(url=base_url+'games/'+str(self.game_id)+'/'+self.player_2.name)
        player_2_hand = json.loads(create_player_2.text)

        get_player_1_score = requests.get(url=base_url+'games/'+str(self.game_id)+'/'+self.player_1.name)
        print("Player 1 score: ", int(get_player_1_score.content))

        # Convert players hands into Card objects and add their cards to their own list.
        p1_list = []
        p2_list = []
        for i in range(len(player_1_hand)):
            p1_new_card = Card.make_card(player_1_hand[i])  # Makes Card object from dictionary received from backend
            p1_list.append(p1_new_card)

            p2_new_card = Card.make_card(player_2_hand[i])
            p2_list.append(p2_new_card)

        # I now have a list of Card objects rather than a list of dictionaries of card attributes.
        # We need players' cards as Card objects to work with Hand and Crib class.

        self.player_1.hand.card_list = p1_list
        self.player_2.hand.card_list = p2_list

        # TODO: how to show hands to individual players?

        # Display the cards to the user - TODO: need to modify Player a bit, so there are no double prints.
        self.player_1.get_letter_options()
        print("Player 1's hand\n")
        self.player_1.display_hand()
        print()
        self.player_2.get_letter_options()
        print("Player 2's hand\n")
        self.player_2.display_hand()
        print()


        # Ask both players to send cards to the crib - the crib is saved into our crib attribute here in Game.
        self.crib.hand.card_list = []  # Do this because crib's hand.card_list is initially None.
        self.player_1.send_cards_to_crib(self.crib)  # Pass in our crib which is empty and fill it.
        self.player_2.send_cards_to_crib(self.crib)

        # Test that the crib prints.
        print("--------Crib List--------: ")
        for i in range(len(self.crib.hand.card_list)):
            self.crib.hand.card_list[i].print_card()
        # ---------------------------


        # Convert the crib back into a list of card dictionaries (rank, suit) to pass over to backend for scoring.
        # We do this because we cannot send Card objects (or any objects) over the API (HTTP)
        crib_list_to_send = []

        for i in range(len(self.crib.hand.card_list)):
            card_dict = {"rank": self.crib.hand.card_list[i].rank, "suit": self.crib.hand.card_list[i].suit}
            crib_list_to_send.append(card_dict)

        crib_json = json.dumps(crib_list_to_send)

        # Send crib info to the backend and return the crib_id so the frontend has access to it.
        create_crib = requests.post(url=base_url+'games/'+str(self.game_id)+'/cribs', data={'crib_card_list': crib_json})
        self.crib.crib_id = int(create_crib.content)

        # Need to convert player's hand to list of dictionaries (not Card objects) to send over the server.
        updated_player_hand = []
        for i in range(len(self.player_1.hand.card_list)):
            card_dict = {"rank": self.player_1.hand.card_list[i].rank, "suit": self.player_1.hand.card_list[i].suit}
            updated_player_hand.append(card_dict)

        json_updated_hand = json.dumps(updated_player_hand)

        # Right now, both players have 4 cards, so call PUT to update and score the player's hands.
        put_req = requests.put(url=base_url+'games/'+str(self.game_id)+'/'+self.player_1.name,
                               data={'updated_player_hand': json_updated_hand})
        print("Player's updated score: ", int(put_req.content))
        self.player_1.score += int(put_req.content)  # Adds on the score that we retrieved from BE calculations.



        delete_game = requests.delete(url=deck_and_card_url+deckname)

    # Have user pass in a specific game_id so they can join a game - then go to that specific game address?
    def join_game(self):
        pass

    def assign_initial_dealer(self):
        num1 = random.randint(1,13)
        num2 = random.randint(1,13)
        if num1 <= num2:
            return self.player_1
        else:
            return self.player_2

    def assign_crib_and_turn(self):
        if self.dealer is self.player_1:
            self.player_1.crib_turn = True
            self.player_1.turn = False
            self.player_2.crib_turn = False
            self.player_2.turn = True
        else:
            self.player_1.crib_turn = False
            self.player_1.turn = True
            self.player_2.crib_turn = True
            self.player_2.turn = False


def main():
    new_game = Game()
    new_game.start_game()


if __name__ == '__main__':
    main()
