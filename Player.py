import json

import requests

from Hand import Hand
from Crib import Crib
#from Card import Card

url = 'http://pcms.game-host.org:8543/decks/'
letters = []

# Frontend Class
class Player:
    def __init__(self, player_hand, crib_turn, turn):
        self.hand = player_hand  # Since Hand is on FE with player, no need to call API
        self.score = 0  # 0 for a player just starting out.
        self.crib_turn = crib_turn
        self.turn = turn

    # returns a list of the cards in the player's hand in dictionary form (rank, suit and name)
    def get_hand(self):
        hand_list = []
        for i in range(len(self.hand.card_list)):
            hand_list[i] = {'rank': self.hand.card_list[i].rank, 'suit': self.hand.card_list[i].suit,
                            'name': self.hand.card_list[i].name}
        return hand_list

    # Don't think we need this - here just in case
    def get_player_score(self):
        return self.score

    def display_hand(self):
        print("Your hand is currently: ", end=" ")
        for i in range(len(self.hand.card_list)):
            if i == len(self.hand.card_list) - 1:
                print(self.hand.card_list[i].name, end=" ")
            else:
                print(self.hand.card_list[i].name + " // ", end=" ")

        print()

    # Append letters to a list for display to the user depending on how many cards they have in their hand.
    def get_letter_options(self):
        if len(self.hand.card_list) == 1:
            letters.append("a")
        elif len(self.hand.card_list) == 2:
            letters.append("a")
            letters.append("b")
        elif len(self.hand.card_list) == 3:
            letters.append("a")
            letters.append("b")
            letters.append("c")
        elif len(self.hand.card_list) == 4:
            letters.append("a")
            letters.append("b")
            letters.append("c")
            letters.append("d")
        elif len(self.hand.card_list) == 5:
            letters.append("a")
            letters.append("b")
            letters.append("c")
            letters.append("d")
            letters.append("e")
        elif len(self.hand.card_list) == 6:
            letters.append("a")
            letters.append("b")
            letters.append("c")
            letters.append("d")
            letters.append("e")
            letters.append("f")

    # TODO: Might need to call calc_score for player.
    # Asks a player for a single card, verifies it is in their hand, and adds the card's rank to the pegging total.
    def make_move(self):
        if not self.turn:
            return

        self.get_letter_options()  # Just gets the letters for display
        self.display_hand()  # Display the cards/options to the player

        while True:
            print("Please select the appropriate letter to play your card.")
            for k in range(len(self.hand.card_list)):
                print(letters[k] + ": " + self.hand.card_list[k].name)

            print()

            selection = str(input())
            if selection == "a":
                inputted_card = self.hand.card_list[0]
            elif selection == "b":
                inputted_card = self.hand.card_list[1]
            elif selection == "c":
                inputted_card = self.hand.card_list[2]
            elif selection == "d":
                inputted_card = self.hand.card_list[3]
            elif selection == "e":
                inputted_card = self.hand.card_list[4]
            elif selection == "f":
                inputted_card = self.hand.card_list[5]
            else:
                print("Not a valid selection.")
                continue

            peg.total += inputted_card.rank
            self.hand.remove_card(inputted_card)

            self.display_hand()
            print("Pegging total: ", peg.total)

            break


# TODO: send_cards_to_crib() needs to be modified to conform with the way make_move() is written.
    # Asks the user for two cards, verifies they are in their hand, removes them, and sends them to the crib
    def send_cards_to_crib(self):
        if not self.crib_turn:
            return

        # Display player's cards to them
        print("Your hand is currently: ", end=" ")
        for i in range(len(self.hand.card_list)):
            print(str(self.hand.card_list[i].rank) + self.hand.card_list[i].suit, end=" ")
        print()

        # Loop through until player has selected two valid cards
        while True:
            print("Please select two cards to send to the crib.")
            inputted_card_1, inputted_card_2 = str(input()).split()
            # inputted_card_1 = Card(int(inputted_card_1[0]), inputted_card_1[1])
            # inputted_card_2 = Card(int(inputted_card_2[0]), inputted_card_2[1])

            # For first card
            for i in range(len(self.hand.card_list)):

                # compare suit and rank of inputted card to see if it matches any card in the player's hand
                if inputted_card_1.rank == self.hand.card_list[i].rank and inputted_card_1.suit == self.hand.card_list[i].suit:
                    break  # Valid card - move to see if second card is valid

            else:
                print("Your first card is not currently in your hand. Please select your cards again.")
                continue

            # For second card.
            for j in range(len(self.hand.card_list)):
                if inputted_card_2.rank == self.hand.card_list[j].rank and inputted_card_2.suit == self.hand.card_list[j].suit:
                    break  # Valid card - can now remove cards from hand and add to crib
            else:
                print("Your second card is not currently in your hand. Please select your cards again.")
                continue

            self.hand.remove_card(inputted_card_1)
            self.hand.remove_card(inputted_card_2)
            crib.grab_cards(inputted_card_1, inputted_card_2)
            break


# The code below is for testing purposes only

deck_name = 'tm123'
req = requests.post(url+deck_name)
req2 = requests.get(url+deck_name+'/cards/6')
deck_info = json.loads(req2.text) # takes the json string and converts it into a python DS


# This is what a json_converter class will do when we get cards from the PCMS mock / real server. Will implement soon.
class FakeCard:
    def __init__(self, card_num):
        # Assigning appropriate rank, suit, and name for each card received from the API
        self.rank = deck_info[card_num]["rank"]
        self.suit = deck_info[card_num]["suit"]
        self.name = deck_info[card_num]["name"]


# Creating 6 cards that I got from the cardAPI running on Dave's server.
card_1 = FakeCard(0)
card_2 = FakeCard(1)
card_3 = FakeCard(2)
card_4 = FakeCard(3)
card_5 = FakeCard(4)
card_6 = FakeCard(5)

# Create a player hand using these cards.
player_hand = Hand(987, card_list=[card_1, card_2, card_3, card_4, card_5, card_6], cards_on_table=[])
my_player = Player(player_hand, True, True)


req3 = requests.delete(url+deck_name)

crib = Crib([])


# This would be a place where we'd call the FE/BE API to get the pegging information (like total) for us.
class TestPeg:
    def __init__(self):
        self.total = 0


peg = TestPeg()
# my_player.send_cards_to_crib()
my_player.make_move()
