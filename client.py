import os  # is this included in base python? attempting to install throws error
import requests
import logging
import json

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


def testing_grounds():
    game = Game(123)
    test_game_resource_post(game, game.game_ID)
    test_game_resource_get(game.game_ID) # Access (get) a game by passing in that game's ID number.
    test_game_resource_delete(game.game_ID)


class Game:
    def __init__(self, game_ID):
        self.player_1 = Player
        self.player_2 = Player
        self.game_ID = game_ID

class Player:
    pass


testing_grounds()