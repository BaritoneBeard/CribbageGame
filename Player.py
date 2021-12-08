import json

import requests

from Hand import Hand
from Crib import Crib
from Card import Card

available_letters = ['a', 'b', 'c', 'd', 'e', 'f']
letter_options = []
crib = Crib([])


# Frontend Class
class Player:
    def __init__(self, player_hand, crib_turn, turn):
        self.hand = player_hand  # Since Hand is on FE with player, no need to call API
        self.score = 0  # 0 for a player just starting out.
        self.crib_turn = crib_turn
        self.turn = turn

    # returns a list of the cards in the player's hand in dictionary form (rank, suit and name)
    # TODO maybe refactor later? it'll return a list of cards when done
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
        for k in range(len(self.hand.card_list)):
            print(letter_options[k] + ": " + self.hand.card_list[k].name)
        print()

    # Append letters to a list for display to the user depending on how many cards they have in their hand.
    def get_letter_options(self):
        for i in range(len(self.hand.card_list)):
            letter_options.append(available_letters[i])

    # TODO: Might need to call calc_score for player.
    # Asks a player for a single card, verifies it is in their hand, and adds the card's rank to the pegging total.
    def make_move(self):
        if not self.turn:
            return

        self.get_letter_options()  # Just gets the letters for display
        self.display_hand()  # Display the cards/options to the player

        print("Please select the appropriate letter to play your card.")

        # when refactoring, some stuff was moved around, if we revert, remember to change tabbing
        selection = None
        while (selection not in letter_options):
            selection = str(input())

            if selection in letter_options:
                input_return = letter_options.index(selection)  # e.g. "b" has index 1
                inputted_card = self.hand.card_list[input_return]
                # peg.total += inputted_card.rank
                self.hand.remove_card(inputted_card)
            else:
                print("** Not a valid letter option. **")

    # Asks the user for two cards, verifies they are in their hand, removes them, and sends them to the crib
    def send_cards_to_crib(self):
        # if not self.crib_turn:        # Both players send cards to crib each turn
        #     return

        self.get_letter_options()  # Just gets the letters for display
        self.display_hand()  # Display the cards/options to the player

        inputted_card_1, inputted_card_2 = None, None
        while (inputted_card_1 == None or inputted_card_2 == None):
            inputted_card_1, inputted_card_2 = None, None
            print("Please select two letters to add those cards to the crib")

            str_cards = str(input())
            if (len(str_cards.split()) > 1):
                card_1, card_2 = str_cards.split()
                card_1 = card_1.strip()[0]  # take only the first character, so apples, bananas would still be a b
                card_2 = card_2.strip()[0]
            else:
                print("** Not enough letters **")
                continue

            if card_1 in letter_options:
                input_return = letter_options.index(card_1)
                inputted_card_1 = self.hand.card_list[input_return]
            else:
                print("** Not a valid selection for card 1 **")
                continue

            # Gets second card and checks to make sure we don't have duplicate letter choices.
            if (card_2 != card_1 and card_2 in letter_options):
                input_return = letter_options.index(card_2)
                inputted_card_2 = self.hand.card_list[input_return]
                self.hand.remove_card(inputted_card_1)
                self.hand.remove_card(inputted_card_2)
                crib.grab_cards(inputted_card_1, inputted_card_2)

            else:
                print("** Not a valid selection for card 2 **")


# This would be a place where we'd call the FE/BE API to get the pegging information (like total) for us.
class TestPeg:
    def __init__(self):
        self.total = 0


# The code below is for testing purposes only
def main():
    # Create a player hand using these cards.
    player_hand = Hand(987, card_list=[Card(0), Card(1), Card(2), Card(3), Card(4), Card(5)], cards_on_table=[])
    my_player = Player(player_hand, True, True)
    peg = TestPeg()
    my_player.send_cards_to_crib()
    print()
    my_player.make_move()


if __name__ == '__main__':
    main()
