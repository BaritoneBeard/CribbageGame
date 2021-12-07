import Hand

'''
Each player looks at their six cards and "lays away" two of them face down to reduce the hand to four. 
The four cards laid away together constitute "the crib". 
The crib belongs to the dealer, but these cards are not exposed or used until after the hands have been played.
'''


# If player is dealer add crib to their hand after scoring their hand's cards_on_table (or just their hand?)
# for pegging round.

class Crib:
    def __init__(self, hand: Hand, display=0):
        self.hand = hand
        self.display = display

    def display_crib(self):  # if display is 1, cards can be added to hand.
        self.display = 1
        self.hand.display_hand()

    def grab_cards(self):
        pass  # implement when player class is completed
