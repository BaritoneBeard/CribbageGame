from Player import Player

'''
How does a player make a move? What's the process?
On the frontend, the player will be asked to select a card from their associated Hand. Once they do, the frontend will
call the API to 

A move is just a card - so what are we doing with that card? We are going to have the Pegging class receive that move
(so just call the pegging method to receive the move and pass in the Move card as parameter). When the pegging class receives the move,
then receive_pegging_move(player_move) will call detect_illegal_move(), then calc_score() and update as it needs to.


'''

# BACKEND CLASS - use API to access player information, don't just import Player^^^^^^
class Move:
    def __init__(self, card_list:list, move, move_id):
        # Each instance of the Move class has a player associated with it and a list of moves it is keeping track of.
        self.player = Player() # We need to know who made the move.
        self.move = move # need a string to know which move it is ('5D', KH', etc)
        self.move_id = move_id # identifies / categorizing the different moves

        self.player_list_of_moves = card_list # This doesn't really make sense in the context.


# We need a way to bring this to the frontend. Or just have it return the move, thne have the frontend call the function.
    # Just have it return the move to the frontend, then the frontend can display the move.

# Note: display_move() has been removed because that is a job for the frontend. The frontend can call to API to get move, then display it as necesssary.

    # I only need this method. Because display_move should happen on the frontend.
    # This method can be called to API to obtain a move made by a particular player. Then we can receive this move,
            # and once we have the move here, we can return in the function. Then other methods on backend can call it
            # to get the move and do whatever they need to do.


    def receive_move(self, player_name, player_card):
        pass