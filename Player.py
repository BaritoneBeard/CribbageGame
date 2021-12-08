from Hand import Hand
from Crib import Crib
from Card import Card


# Frontend Class
class Player:
    def __init__(self, player_hand, crib_turn, turn):
        self.hand = player_hand  # Since Hand is on FE with player, no need to call API
        self.score = 0  # 0 for a player just starting out.
        self.crib_turn = crib_turn
        self.turn = turn

    # Don't think we need this - here just in case
    def get_hand(self):
        return self.hand

    # Don't think we need this - here just in case
    def get_player_score(self):
        return self.score

    # Asks a player for a single card, verifies it is in their hand, and adds the card's rank to the pegging total.
    def make_move(self):
        if not self.turn:
            return

        # Display the cards to the player
        print("You hand is currently:", end=" ")
        for i in range(len(self.hand.card_list)):
            print(str(self.hand.card_list[i].rank) + self.hand.card_list[i].suit, end=" ")
        print()

        while True:
            print("Please input a card as your move.")
            inputted_card = str(input())
            inputted_card = Card(int(inputted_card[0]), inputted_card[1]) # Stores user's choice into a Card object for comparison
            for i in range(len(self.hand.card_list)):

                # compare suit and rank of inputted card to see if it matches any card in the player's hand
                if inputted_card.rank == self.hand.card_list[i].rank and inputted_card.suit == self.hand.card_list[i].suit:
                    peg.total += inputted_card.rank  # peg.total is something we'd get from the API
                    self.hand.remove_card(inputted_card)  # remove the played card from the player's hand
                    break
            else:
                print("That card is not currently in your hand.")
                continue

            break

    # Asks the user for two cards, verifies they are in their hand, removes them, and sends them to the crib
    def send_cards_to_crib(self):
        if not self.crib_turn:
            return

        # Display player's cards to them
        print("You hand is currently:", end=" ")
        for i in range(len(self.hand.card_list)):
            print(str(self.hand.card_list[i].rank) + self.hand.card_list[i].suit, end=" ")
        print()

        # Loop through until player has selected two valid cards
        while True:
            print("Please select two cards to send to the crib.")
            inputted_card_1, inputted_card_2 = str(input()).split()
            inputted_card_1 = Card(int(inputted_card_1[0]), inputted_card_1[1])
            inputted_card_2 = Card(int(inputted_card_2[0]), inputted_card_2[1])

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


# All the following code is for testing purposes only

card_1 = Card(4, 'S')
card_2 = Card(5, 'H')
card_3 = Card(5, 'D')
card_4 = Card(6, 'C')

player_hand = Hand(987, card_list=[card_1, card_2, card_3, card_4], cards_on_table=[])
my_player = Player(player_hand, True, True)
crib = Crib([])

# This would be a place where we'd call the API to get the pegging information (like total) for us.
class TestPeg:
    def __init__(self):
        self.total = 0


peg = TestPeg()
my_player.send_cards_to_crib()
my_player.make_move()
