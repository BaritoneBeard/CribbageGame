import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json
from Hand import Hand


base_url = 'http://127.0.0.1:5000/'


def test_game_resource_post(game_obj, game_id):
    URL = base_url + 'games/' + str(game_id)
    DATA = {'game_ID': game_obj}
    post_request = requests.post(url=URL, data=DATA)
    # post_info = json.loads(post_request.text)
    # print("Regular post_request text: ", post_request.text)
    # print("Converted Json info: ", post_info)


def test_game_resource_get(game_id):
    URL = base_url + 'games/' + str(game_id)
    get_request = requests.get(url=URL)
    print(get_request.text)


def test_game_resource_delete(game_id):
    URL = base_url + 'games/' + str(game_id)
    delete_request = requests.delete(url=URL)
    print(delete_request.text)


def test_player_resource_post(player_obj, game_id):  # specify the game_ID the player is a part of.
    URL = base_url + 'games/' + str(game_id) + '/' + player_obj.player_name
    DATA = {'player': player_obj}
    player_post_request = requests.post(url=URL, data=DATA)
    print(player_post_request.text)


def test_player_resource_get(player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name
    player_get_request = requests.get(url=URL)
    print(player_get_request.text)


def test_player_resource_delete(player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name
    player_delete_request = requests.delete(url=URL)
    print(player_delete_request.text)


def test_hand_resource_post(hand_obj, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/hand/' + str(hand_obj.hand_id)
    DATA = {'hand_ID': hand_obj}
    hand_post_request = requests.post(url=URL, data=DATA)
    print(hand_post_request.text)


def test_hand_resource_get(hand_id, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/hand/' + str(hand_id)
    hand_get_request = requests.get(url=URL)
    print(hand_get_request.text)


def test_hand_resource_delete(hand_id, player_name, game_id):
    URL = base_url + 'games/' + str(game_id) + '/' + player_name + '/hand/' + str(hand_id)
    hand_delete_request = requests.delete(url=URL)
    print(hand_delete_request.text)


def testing_grounds():
    sample_game = Game(123)  # the game_ID will be randomly generated and stored on the backend when the user requests to start a new game.
    sample_hand = Hand(3935, ['2H', 'KD'], ['AS', '7C'])  # the hand_ID should be randomly generated and stored. Perhaps Player class can keep a list of unique hand_IDs
    sample_player = Player(sample_hand, True, False, 'tyler')

    test_game_resource_post(sample_game, sample_game.game_id)
    test_game_resource_get(sample_game.game_id)
    test_game_resource_delete(sample_game.game_id)

    print()

    test_player_resource_post(sample_player, sample_game.game_id)
    test_player_resource_get(sample_player.player_name, sample_game.game_id)
    test_player_resource_delete(sample_player.player_name, sample_game.game_id)

    print()

    test_hand_resource_post(sample_hand, sample_player.player_name, sample_game.game_id)
    test_hand_resource_get(sample_hand.hand_id, sample_player.player_name, sample_game.game_id)
    test_hand_resource_delete(sample_hand.hand_id, sample_player.player_name, sample_game.game_id)


class Game:
    def __init__(self, game_id):
        self.player_1 = Player
        self.player_2 = Player
        self.game_id = game_id


class Player:
    def __init__(self, hand, turn, crib_turn, name):
        self.hand = hand
        self.score = 0
        self.turn = turn
        self.crib_turn = crib_turn
        self.player_name = name


testing_grounds()