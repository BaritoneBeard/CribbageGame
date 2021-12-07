import Hand

'''
Each player looks at their six cards and "lays away" two of them face down to reduce the hand to four. 
The four cards laid away together constitute "the crib". 
The crib belongs to the dealer, but these cards are not exposed or used until after the hands have been played.
'''


# If player is dealer add crib to their hand after scoring their hand's cards_on_table (or just their hand?)
# for pegging round.

class Crib:
    def __init__(self, hand: Hand, crib_id = 0, display=False):
        self.hand = hand
        self.crib_id = crib_id
        self.display = display

    def display_crib(self):  # Not sure if this boolean will be needed, but might as well have a check.
        self.display = True
        self.hand.display_hand()

    def grab_cards(self):
        pass  # implement when player class is completed
