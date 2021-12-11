import json
import random

import requests
from BE_Game import BE_Game
from Card import make_card

from Player import Player

'''
How does a player make a move? What's the process?
On the frontend, the player will be asked to select a card from their associated Hand. Once they do, the frontend will
call the API to 

A move is just a card - so what are we doing with that card? We are going to have the Pegging class receive that move
(so just call the pegging method to receive the move and pass in the Move card as parameter). When the pegging class receives the move,
then receive_pegging_move(player_move) will call detect_illegal_move(), then calc_score() and update as it needs to.


'''

move_id_list = []
localhost_url = 'http://127.0.0.1:5000/'

# Move will just be a Card dict or card object from Card.py
class Move:
    def __init__(self, move_id): # had card_list: list
        self.player = None # TODO: How to set player here
        self.moves_so_far = []
        self.move = None  # Will get when we call receive_move
        self.move_id = move_id # identifies / categorizing the different moves
        #self.player_list_of_moves = card_list # This doesn't really make sense in the context.

    # Call GET on API server
    # Call to specific game of the player. Then using that game_id, player_name, access the move.
    def receive_move(self, player_name): # TODO: Pass in info about player?
        # How to get game_id here of specific player?
        URL = localhost_url+'games/' + str(0000) + '/' + player_name + '/moves/' + str(self.move_id)
        get_req = requests.get(url=URL)
        get_req = json.loads(get_req.text)[0]  # We get a card_dictionary here
        make_the_move_a_card = make_card(get_req)
        self.move = make_the_move_a_card  # gives a Card object with rank and suit.
        print("Rank of Move: ", self.move.rank)
        print("Suit of Move: ", self.move.suit)

def create_random_move_id():
    id = random.randint(1,10000)
    while True:
        if id in move_id_list:
            id = random.randint(1,10000)
        else:
            return id


my_move = Move(create_random_move_id())
my_move.receive_move('tyler')

# Need to modify Player's make_move to send a move over the API. Then in receive_move, we can access it.
# When testing, be sure to create a new game (BE_Game), then have player_1 in BE_Game call Player's method make_move()
# You might have to change this later b/c Player make_move() method on FE and BE_Game on backend, but just ignore it
# make_move() when called, should put a move on the API, then call your receive_move here to get that specific move


# Use a specific game_id and player_name for testing purposes
