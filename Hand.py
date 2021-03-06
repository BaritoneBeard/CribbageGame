import Card


class Hand:
    def __init__(self, hand_id = 0, card_list:list = None, cards_on_table:list = None):
        self.card_list = card_list
        self.cards_on_table = cards_on_table  # cards_on_table might not be needed if crib gets added to hand
        self.hand_id = hand_id   # Used to track which hands belong to which players.

    def display_hand(self):
        for card in self.card_list:
            card.print_card()

    def add_card(self, card: Card):
        self.card_list.append(card)

    def remove_card(self, card: Card = None,  index: int = -1):
        try:
            if card != None :
                for c in self.card_list:
                    if card.rank == c.rank and card.suit == c.suit:
                        self.card_list.remove(c)
            elif index != -1:
                self.card_list.remove(index)
            else:
                raise ValueError
        except ValueError as e:
            print("At least one field must be filled (either index or card)")
