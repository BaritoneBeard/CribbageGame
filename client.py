import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json
from Hand import Hand

logger = logging.getLogger("client.py")
logging.basicConfig(filename="clientlog.txt")
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

url = 'http://127.0.0.1:5000/'


def test_game_resource_post(game_obj, game_ID):
    URL = url + 'games/' + str(game_ID)
    DATA = {'game_ID': game_obj}
    post_request = requests.post(url=URL, data=DATA)
    print(post_request.text)


def test_game_resource_get(game_ID):
    URL = url + 'games/' + str(game_ID)
    get_request = requests.get(url=URL)
    print(get_request.text)


def test_game_resource_delete(game_ID):
    URL = url + 'games/' + str(game_ID)
    delete_request = requests.delete(url=URL)
    print(delete_request.text)


def test_player_resource_post(player_obj, game_ID):
    URL = url + 'games/' + str(game_ID) + '/' + player_obj.player_name  # specify the game_ID the player is a part of.
    DATA = {'player': player_obj}
    player_post_request = requests.post(url=URL, data=DATA)
    print(player_post_request.text)






def testing_grounds():
    sample_game = Game(123)
    test_game_resource_post(sample_game, sample_game.game_ID)
    test_game_resource_get(sample_game.game_ID) # Access (get) a sample_game by passing in that sample_game's ID number.
    test_game_resource_delete(sample_game.game_ID)

    print()

    sample_hand = Hand(['2H', 'KD'], ['AS', '7C'])
    sample_player = Player(sample_hand, True, False, 'tyler')
    test_player_resource_post(sample_player, sample_game.game_ID)


class Game:
    def __init__(self, game_ID):
        self.player_1 = Player
        self.player_2 = Player
        self.game_ID = game_ID


class Player:
    def __init__(self, hand, turn, crib_turn, name):
        self.hand = hand
        self.score = 0
        self.turn = turn
        self.crib_turn = crib_turn
        self.player_name = name


testing_grounds()