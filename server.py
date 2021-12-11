import json

from flask import Flask, request, Response, jsonify, make_response
from flask_restful import Resource, Api
import logging



FORMAT = '%(asctime)s|%(filename)s/%(name)s|%(funcName)s[%(lineno)d]|%(message)s'
logging.basicConfig(filename='PycharmProjects/SoftwareEngineering/serverlog.txt', format=FORMAT)
logger = logging.getLogger("server.py")
logger.setLevel(logging.DEBUG)


flask_instance = Flask(__name__)
api_instance = Api(flask_instance)


games = {}  # holds game resources
players = {}  # holds player resources
hands = {}  # holds hand resources for players
moves = {} # holds move resources for players
cribs = {}


class Game(Resource):
    def post(self, game_id):
        try:
            req = request.form['game_info']  # a json string
            games[game_id] = json.loads(req)  # Load json string into a python dict and store it
            logger.info("INFO: Game Resource posted successfully.")
            return Response(status=201, response="Successfully created the game.")

        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource POST call.")
            return Response(status=409, response="Unable to create a game at this time.")

    def get(self, game_id):
        try:
            logger.info("INFO: Game Resource retrieved successfully.")
            return make_response(jsonify(games[game_id]), 200)
            #return Response(status=200, response=games[game_id])
        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource GET call.")
            return Response(status=404, response="The game you are looking for cannot be found.")

    def delete(self, game_id):
        try:
            del games[game_id]
            logger.info("INFO: Game Resource deleted successfully.")
            return Response(status=205, response="Your game has been deleted.")
        except KeyError:
            logger.error("ERROR: KeyError exception encountered with Game Resource DELETE call.")
            return Response(status=404, response="Cannot delete game because it does not exist.")


class Player(Resource):
    def post(self, player_name, game_id):  # game_ID needed to make add_resource method work
        try:
            req = request.form['player_info']
            players[player_name] = json.loads(req)
            return Response(status=201, response="Successfully created player: " + player_name)
        except KeyError:
            return Response(status=409, response="Unable to create a new player at this time.")

    # Potentially need to check if the game exists first before trying to access the player.
    def get(self, player_name, game_id):
        try:
            return make_response(jsonify(players[player_name]), 200)
            #return Response(status=200, response=players[player_name])
        except:
            return Response(status=404, response="The player you are looking for cannot be found.")

    def delete(self, player_name, game_id):
        try:
            del players[player_name]
            return Response(status=205, response="Player has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete player because it does not exist.")




class Hand(Resource):
    def post(self, hand_id, game_id):  # player_name and game_ID needed to make add_resource method work
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


# Come back to this - might not need it with the implementation
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




# Come back to this - might not need it with the implementation
class Crib(Resource):
    def post(self, crib_id, player_name, game_id):
        try:
            req = request.form['crib_info']
            cribs[crib_id] = json.loads(req)
            return Response(status=201, response="Successfully stored a crib.")
        except KeyError:
            return Response(status=409, response="Unable to create a crib at this time.")

    def get(self, crib_id, player_name, game_id):
        try:
            return make_response(jsonify(cribs[crib_id]), 200)
        except:
            return Response(status=404, response="The crib you want to access cannot be found.")

    def delete(self, crib_id, player_name, game_id):
        try:
            del cribs[crib_id]
            return Response(status=205, response="This crib has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this crib because it does not exist.")


api_instance.add_resource(Game, '/games/<int:game_id>')
api_instance.add_resource(Player, '/games/<int:game_id>/players/<string:player_name>')
api_instance.add_resource(Hand, '/games/<int:game_id>/hands/<int:hand_id>')
api_instance.add_resource(Move, '/games/<int:game_id>/players/<string:player_name>/moves/<int:move_id>')
api_instance.add_resource(Crib, '/games/<int:game_id>/cribs/<int:crib_id>')



if __name__ == '__main__':
    flask_instance.run(debug=True)