import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json
from Player import Player
from Hand import Hand

base_url = 'http://127.0.0.1:5000/'




# pass in a json string, extract the game_id from it, pass in the json string as the data to be stored on the server
def test_game_resource_post(game_json_string):
    game_dict = json.loads(game_json_string) # now this is a dictionary and I can access the game_id
    URL = base_url + 'games/' + str(game_dict["game_id"])
    DATA = {"game_info": game_json_string}
    post_request = requests.post(url=URL, data=DATA)


def test_game_resource_get(game_id):
    URL = base_url + 'games/' + str(game_id)
    get_request = requests.get(url=URL)
    game_dict = json.loads(get_request.text)
    print(game_dict)


def test_game_resource_delete(game_id):
    URL = base_url + 'games/' + str(game_id)
    delete_request = requests.delete(url=URL)
    print(delete_request.text)





def test_player_resource_post(player_json_string, game_id):  # specify the game_ID the player is a part of.
    player_dict = json.loads(player_json_string)
    URL = base_url + 'games/' + str(game_id) + '/players/' + player_dict["name"]
    DATA = {'player_info': player_json_string}
    player_post_request = requests.post(url=URL, data=DATA)


def test_player_resource_get(player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/players/' + player_name
    player_get_request = requests.get(url=URL)
    player_dict = json.loads(player_get_request.text)
    print("player dictionary:", player_dict)


def test_player_resource_delete(player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/players/' + player_name
    player_delete_request = requests.delete(url=URL)
    print(player_delete_request.text)





def test_hand_resource_post(hand_json_string, game_id):
    hand_dict = json.loads(hand_json_string)
    URL = base_url + 'games/' + str(game_id) + '/hands/' + str(hand_dict["hand_id"])
    DATA = {'hand_info': hand_json_string}
    hand_post_request = requests.post(url=URL, data=DATA)
    print(hand_post_request.text)


def test_hand_resource_get(hand_id, game_id):
    URL = base_url + 'games/' + str(game_id) + '/hands/' + str(hand_id)
    hand_get_request = requests.get(url=URL)
    hand_dict = json.loads(hand_get_request.text)
    print("Hand information: ", hand_dict)
    return hand_dict


def test_hand_resource_delete(hand_id, game_id):
    URL = base_url + 'games/' + str(game_id) + '/hands/' + str(hand_id)
    hand_delete_request = requests.delete(url=URL)
    print(hand_delete_request.text)





# TODO: Move still need to be changed to conform with the new json way of setting up the server - might not need it.
def test_move_resource_post(player_move, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/moves/' + str(player_move.move_id)
    DATA = {'player_move': player_move}
    move_post_request = requests.post(url=URL, data=DATA)
    print(move_post_request.text)


def test_move_resource_get(player_move, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/moves/' + str(player_move.move_id)
    move_get_request = requests.get(url=URL)
    print(move_get_request.text)


def test_move_resource_delete(player_move, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/moves/' + str(player_move.move_id)
    move_delete_request = requests.delete(url=URL)
    print(move_delete_request.text)






def testing_grounds():
    game_id = 6886
    game_string_test = "This is my game string"
    sample_game = Game(game_id, game_string_test)

    game_dict = {"game_id": sample_game.game_id, "game_string_test": sample_game.game_string}
    game_json_string = json.dumps(game_dict) # dumps game_dict into a json string

    test_game_resource_post(game_json_string)
    test_game_resource_get(game_dict["game_id"])
    #test_game_resource_delete(game_dict["game_id"])

    print()
    my_hand = Hand(9900, ['2S', '7C'], ['3D', '5H'])
    hand_dict = {"hand_id": my_hand.hand_id, "card_list": my_hand.card_list, "cards_on_table": my_hand.cards_on_table}
    hand_json_string = json.dumps(hand_dict)

    test_hand_resource_post(hand_json_string, game_dict["game_id"])
    hand_info = test_hand_resource_get(hand_dict["hand_id"], game_dict["game_id"])
    test_hand_resource_delete(hand_dict["hand_id"], game_dict["game_id"])


    print()

    my_player = Player(hand_info["card_list"], False, True, 'tyler')
    player_dict = {"hand": my_player.hand, "crib_turn": my_player.crib_turn, "turn": my_player.turn,
                   "name": my_player.name, "score": 0} # do we need score
    player_json_string = json.dumps(player_dict) # creates a json string for player attributes.

    test_player_resource_post(player_json_string, game_dict["game_id"])
    test_player_resource_get(player_dict["name"], game_dict["game_id"])
    #test_player_resource_delete(player_dict["name"], game_dict["game_id"])

    print()

    #player_move = Move()


# NOTE: Anything besides game_id is just a TESTING VARIABLE. IT WILL NOT GO INTO THE FINAL IMPLEMENTATION.
class Game:
    def __init__(self, game_id, game_string):
        #self.player_1 = Player()
        #self.player_2 = Player()
        self.game_id = game_id
        self.game_string = game_string





testing_grounds()