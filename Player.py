import json

import requests

from Hand import Hand
from Crib import Crib
from Card import Card

letter_options = []

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
            letter_options.append("a")
        elif len(self.hand.card_list) == 2:
            letter_options.append("a")
            letter_options.append("b")
        elif len(self.hand.card_list) == 3:
            letter_options.append("a")
            letter_options.append("b")
            letter_options.append("c")
        elif len(self.hand.card_list) == 4:
            letter_options.append("a")
            letter_options.append("b")
            letter_options.append("c")
            letter_options.append("d")
        elif len(self.hand.card_list) == 5:
            letter_options.append("a")
            letter_options.append("b")
            letter_options.append("c")
            letter_options.append("d")
            letter_options.append("e")
        elif len(self.hand.card_list) == 6:
            letter_options.append("a")
            letter_options.append("b")
            letter_options.append("c")
            letter_options.append("d")
            letter_options.append("e")
            letter_options.append("f")

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
                print(letter_options[k] + ": " + self.hand.card_list[k].name)

            print()

            selection = str(input())
            try:
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
                    print("** Not a valid selection. **")
                    continue

                peg.total += inputted_card.rank
                self.hand.remove_card(inputted_card)
                break

            except IndexError:  # User tries to choose a letter that is not listed as one of the options.
                print("** Not a valid letter option. **")
                continue

    # Asks the user for two cards, verifies they are in their hand, removes them, and sends them to the crib
    def send_cards_to_crib(self):
        if not self.crib_turn:
            return

        self.get_letter_options()  # Just gets the letters for display
        self.display_hand()  # Display the cards/options to the player

        while True:
            print("Please select two letters to play your card.")
            for k in range(len(self.hand.card_list)):
                print(letter_options[k] + ": " + self.hand.card_list[k].name)

            print()

            card_1, card_2 = str(input()).split()

            try:
                if card_1 == "a":
                    inputted_card_1 = self.hand.card_list[0]
                elif card_1 == "b":
                    inputted_card_1 = self.hand.card_list[1]
                elif card_1 == "c":
                    inputted_card_1 = self.hand.card_list[2]
                elif card_1 == "d":
                    inputted_card_1 = self.hand.card_list[3]
                elif card_1 == "e":
                    inputted_card_1 = self.hand.card_list[4]
                elif card_1 == "f":
                    inputted_card_1 = self.hand.card_list[5]
                else:
                    print("** Not a valid selection. **")
                    continue
            except IndexError:
                print("** Not a valid letter option. **")  # User tries to choose a letter that is not listed as one of the options.
                continue

            # Gets second card and checks to make sure we don't have duplicate letter choices.
            try:
                if card_2 == "a" and card_1 != "a":
                    inputted_card_2 = self.hand.card_list[0]
                elif card_2 == "b" and card_1 != "b":
                    inputted_card_2 = self.hand.card_list[1]
                elif card_2 == "c" and card_1 != "c":
                    inputted_card_2 = self.hand.card_list[2]
                elif card_2 == "d" and card_1 != "d":
                    inputted_card_2 = self.hand.card_list[3]
                elif card_2 == "e" and card_1 != "e":
                    inputted_card_2 = self.hand.card_list[4]
                elif card_2 == "f" and card_1 != "f":
                    inputted_card_2 = self.hand.card_list[5]
                else:
                    print("** Not a valid selection. **")
                    continue

                self.hand.remove_card(card_1)
                self.hand.remove_card(card_2)
                crib.grab_cards(card_1, card_2)
                break

            except IndexError:
                print("** Not a valid letter option. **")
                continue


# The code below is for testing purposes only

# Create a player hand using these cards.
player_hand = Hand(987, card_list=[Card(0), Card(1), Card(2), Card(3), Card(4), Card(5)], cards_on_table=[])
my_player = Player(player_hand, True, True)
crib = Crib([])


# This would be a place where we'd call the FE/BE API to get the pegging information (like total) for us.
class TestPeg:
    def __init__(self):
        self.total = 0


peg = TestPeg()
my_player.make_move()
my_player.send_cards_to_crib()