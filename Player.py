from Hand import Hand
from Crib import Crib

# FRONTEND CLASS
class Player:
    def __init__(self, player_hand, crib_turn):
        self.hand = player_hand # For now, not calling the API for the hand, just assigning a random Hand object
        self.score = 0  # 0 for a player just starting out.
        self.crib_turn = crib_turn

    # why need this?
    def get_hand(self):
        return self.hand

    # return player score - do we really need this?
    def get_player_score(self):
        return self.score

    # Ask a player for a card to make the move, then do the necessary move
    # Add the card to the pegging table, as necessary.
    # You can display the move made by the player in this function, no need for an extra function
    def make_move(self):
        print("Please input a card as your move.")
        card = str(input())



    # Need to ask for TWO cards from player.
    # Delete those cards from their own hand and add the cards to the crib card_list
    def send_cards_to_crib(self):
        print("Please input 2 cards to send to the crib.") # will get something like '4S' and 'KD'
        card_1, card_2 = str(input())
        if card_1 in self.hand and card_2 in self.hand:
            self.hand.remove_card(card_1)
            self.hand.remove_card(card_2)

        # add cards to the crib
        crib.grab_cards(card_1, card_2) # I want crib to have 2 cards as parameters, so I can pass those in.


player_hand = Hand(987, card_list=['4S', 'AH', '5D', '6C'], cards_on_table=[])  # Add stuff here.
Player(player_hand, False)
crib = Crib([]) # Just make an empty crib.

class Test_Peg:
    def __init__(self, total):
        self.total = total