import json
import requests

available_letters = ['a', 'b', 'c', 'd', 'e', 'f']
letter_options = []
localhost_url = 'http://127.0.0.1:5000/'

# Frontend Class
class Player:
    def __init__(self, player_hand, crib_turn, turn, name, score):
        self.hand = player_hand
        self.score = score  # 0 for a player just starting out.
        self.crib_turn = crib_turn  # Every round this will flip for the two players
        self.turn = turn
        self.name = name

    # returns a list of the cards in the player's hand in dictionary form (rank, suit and name)
    def get_hand(self):
        hand_list = []
        for i in range(len(self.hand.card_list)):
            hand_list[i] = {'rank': self.hand.card_list[i].rank, 'suit': self.hand.card_list[i].suit,
                            'name': self.hand.card_list[i].name}
        return hand_list

    def get_player_name(self):
        print("Please enter your name.")
        self.name = str(input())

    # Don't think we need this - here just in case
    def get_player_score(self):
        return self.score

    def display_hand(self):
        for k in range(len(self.hand.card_list)):
            print(letter_options[k]+":", end=" ")
            self.hand.card_list[k].print_card()
        print()

    # Append letters to a list for display to the user depending on how many cards they have in their hand.
    def get_letter_options(self):
        for i in range(len(self.hand.card_list)):
            letter_options.append(available_letters[i])

    # Call put to move, pass in your move as the data
    def make_move(self, game_id, move_instance_id):

        self.get_letter_options()  # Just gets the letters for display
        self.display_hand()  # Display the cards/options to the player

        print("Please select the appropriate letter to play your card.")

        # when refactoring, some stuff was moved around, if we revert, remember to change tabbing
        selection = None
        while (selection not in letter_options): # selection not in letter_options
            selection = str(input())

            if selection in letter_options:
                input_return = letter_options.index(selection)  # e.g. "b" has index 1
                inputted_card = self.hand.card_list[input_return]

                # inputted_card is a Card class, so need to convert it to a dict to send over API
                card_dict = {"rank": inputted_card.rank, "suit": inputted_card.suit}
                card_dict_json = json.dumps(card_dict)

                # Attempt to make the move. Does not account for illegal moves.
                make_move = requests.put(url=localhost_url+'games/'+str(game_id)+'/'+self.name+'/moves/'
                                             +str(move_instance_id), data={'move_card': card_dict_json})

                # Add points of move onto player's score and remove that card from their hand.
                earned_pegging_points = int(make_move.content)
                self.score += earned_pegging_points
                self.hand.remove_card(inputted_card)

            else:
                print("** Not a valid letter option. **")

    # Asks the user for two cards, verifies they are in their hand, removes them, and sends them to the crib
    def send_cards_to_crib(self, crib):

        print("Player " + self.name + "'s hand: ")
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
# class TestPeg:
#     def __init__(self):
#         self.total = 0



# The code below is for testing purposes only
# def main():
#     # Create a player hand using these cards.
#     player_hand = Hand(987, card_list=[Card(0), Card(1), Card(2), Card(3), Card(4), Card(5)], cards_on_table=[])
#     my_player = Player(player_hand, True, True)
#     peg = TestPeg()
#     my_player.send_cards_to_crib()
#     print()
#     my_player.make_move()
#
#
# if __name__ == '__main__':
#     main()
