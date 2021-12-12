import json
import random

import requests
from flask import Flask, request, Response, jsonify, make_response
from flask_restful import Resource, Api
import logging
from BE_Game import BE_Game
from Player_BE import Player_BE



FORMAT = '%(asctime)s|%(filename)s/%(name)s|%(funcName)s[%(lineno)d]|%(message)s'
logging.basicConfig(filename='PycharmProjects/SoftwareEngineering/serverlog.txt', format=FORMAT)
logger = logging.getLogger("server.py")
logger.setLevel(logging.DEBUG)


flask_instance = Flask(__name__)
api_instance = Api(flask_instance)

deck_and_card_url = 'http://pcms.game-host.org:8543/'
deckname = 'decks/bgame'


games = {}  # holds game resources
players = {}  # holds player resources
hands = {}  # holds hand resources for players
moves = {} # holds move resources for players
cribs = {}


class Game(Resource):
    def post(self):
        try:
            game_id = str(random.randint(1,10000))

            # Create a new deck
            new_deck = requests.post(deck_and_card_url+deckname)

            logger.info("INFO: Game Resource posted successfully.")
            return Response(status=201, response=game_id)  # Return game_id to the frontend.

        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource POST call.")
            return Response(status=409, response="Unable to create a game at this time.")

    def get(self):
        try:
            logger.info("INFO: Game Resource retrieved successfully.")
            #return make_response(jsonify(games[game_id]), 200)
            #return Response(status=200, response=games[game_id])
        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource GET call.")
            return Response(status=404, response="The game you are looking for cannot be found.")

    def delete(self):
        try:
            #del games[game_id]
            logger.info("INFO: Game Resource deleted successfully.")
            return Response(status=205, response="Your game has been deleted.")
        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource DELETE call.")
            return Response(status=404, response="Cannot delete game because it does not exist.")


# Still need to pass player_name and hand to Player_BE for storage.
class Player(Resource):
    def post(self, player_name, game_id):
        try:
            # Call PCMS to create hand for the player - then send it back to frontend.
            player_hand = requests.get(deck_and_card_url + deckname + '/cards/6')  # This returns a list of dicts

            return Response(status=201, response=player_hand)
        except KeyError:
            return Response(status=409, response="Unable to create a new player at this time.")

    def get(self, player_name):
        try:
            return make_response(jsonify(players[player_name]), 200)
            #return Response(status=200, response=players[player_name])
        except:
            return Response(status=404, response="The player you are looking for cannot be found.")

    # Here, have URL be 'games/'+player_name+'/update' - used to update info about player and return it (like score)
    def put(self, player_name):
        pass

    def delete(self, player_name):
        try:
            del players[player_name]
            return Response(status=205, response="Player has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete player because it does not exist.")


# Have not modified yet.
class Hand(Resource):
    def post(self, hand_id, game_id):
        try:
            req = request.form['hand_info']
            hands[hand_id] = json.loads(req)
            return Response(status=201, response="Successfully created a hand for the player.")
        except KeyError:
            return Response(status=409, response="Unable to create a new hand for at this time.")

    def get(self, hand_id, game_id):
        try:
            return make_response(jsonify(hands[hand_id]), 200)
            #return Response(status=200, response=hands[hand_id])
        except:
            return Response(status=404, response="The hand you want to retrieve cannot be found.")

    def delete(self, hand_id, game_id):
        try:
            del hands[hand_id]
            return Response(status=205, response="This hand has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this hand because it does not exist.")


# Have not modified yet
class Move(Resource):
    def post(self, move_id, player_name, game_id):
        try:
            req = request.form['move_info']
            moves[move_id] = json.loads(req)
            return Response(status=201, response="Successfully stored a move for player: " + player_name)
        except KeyError:
            return Response(status=409, response="Unable to process the requested move at this time.")

    def get(self, move_id, player_name, game_id):
        try:
            return make_response(jsonify(moves[move_id]), 200)
        except:
            return Response(status=404, response="The move you want to access cannot be found.")

    def delete(self, move_id, player_name, game_id):
        try:
            del moves[move_id]
            return Response(status=205, response="This move has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this move because it does not exist.")




class Crib(Resource):
    def post(self, game_id):
        try:
            crib_id = str(random.randint(1,10000))
            crib_card_list = request.form['crib_card_list']
            cards_list = json.loads(crib_card_list)["card_list"]  # Gives a list of card dicts (dicts with rank+suit)

            # games[game_id].crib = cards_list  -- this would be our BE_Game we create accessing and setting the crib.
            # The crib would then be a list of dictionaries that we pass into scoring.

            return Response(status=201, response=crib_id)
        except KeyError:
            return Response(status=409, response="Unable to create a crib at this time.")

    def get(self, crib_id, player_name, game_id):
        try:
            return make_response(jsonify(cribs[crib_id]), 200)
        except:
            return Response(status=404, response="The crib you want to access cannot be found.")

    # Modify the crib on the backend, using the crib_id to access and change a specific crib.
    def put(self, crib_id, game_id):
        pass

    def delete(self, crib_id, player_name, game_id):
        try:
            del cribs[crib_id]
            return Response(status=205, response="This crib has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this crib because it does not exist.")


api_instance.add_resource(Game, '/games')
api_instance.add_resource(Player, '/games/<int:game_id>/<string:player_name>')
# api_instance.add_resource(Hand, '/games/<int:game_id>/hands/<int:hand_id>')
# api_instance.add_resource(Move, '/games/<int:game_id>/players/<string:player_name>/moves/<int:move_id>')
api_instance.add_resource(Crib, '/games/<int:game_id>/cribs')



if __name__ == '__main__':
    flask_instance.run(debug=True)