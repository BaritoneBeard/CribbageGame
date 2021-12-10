import json

from flask import Flask, request, Response, jsonify, make_response
from flask_restful import Resource, Api
import logging
from json_converter import JSONGame



FORMAT = '%(asctime)s|%(filename)s/%(name)s|%(funcName)s[%(lineno)d]|%(message)s'
logging.basicConfig(filename='PycharmProjects/SoftwareEngineering/serverlog.txt', format=FORMAT)
logger = logging.getLogger("server.py")
logger.setLevel(logging.DEBUG)


flask_instance = Flask(__name__)
api_instance = Api(flask_instance)

# Note: No Crib Resource class was added because a crib is just a type of hand, so there is no need for one.

games = {}  # holds game resources
players = {}  # holds player resources
hands = {}  # holds hand resources for players
moves = {} # holds move resources for players


'''
I know what to do now. request.form only gets 1 item, so I need to use separate request.forms to get all the info I need
Then put that in a dictionary. Then store that in my games[game_id]. In get, instead of a Response return, I'll need to
do something like: return games[game_id], 200. This will indeed return a dictionary.

But wait, isn't a dictionary a class? How can I send it over to the server from the client if it is an object.
If this is the case, I'll have to resort using json to convert my dictionary into a string, passing the string over http
then deserializing it here on the server.

'''


class Game(Resource):
    def post(self, game_id):
        try:
            req = request.form['game_info'] # a json string
            req = json.loads(req) # take a json string and load it into a python dictionary.
            games[game_id] = req # We are storing the python dictionary into our games, so we can access it.
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



'''
class Hand(Resource):
    def post(self, hand_id, player_name, game_id):  # player_name and game_ID needed to make add_resource method work
        try:
            hands[hand_id] = request.form['hand_ID']
            return Response(status=201, response="Successfully created a hand for player: " + player_name)
        except KeyError:
            return Response(status=409, response="Unable to create a new hand for player at this time.")

    def get(self, hand_id, player_name, game_id):
        try:
            return Response(status=200, response=hands[hand_id])
        except:
            return Response(status=404, response="The hand you want to retrieve cannot be found.")

    def delete(self, hand_id, player_name, game_id):
        try:
            del hands[hand_id]
            return Response(status=205, response="This hand has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this hand because it does not exist.")


# Come back to this - might not need it with the implementation
class Move(Resource):
    def post(self, move_id, player_name, game_id):
        try:
            moves[move_id] = request.form['player_move']
            return Response(status=201, response="Successfully stored a move for player: " + player_name)
        except KeyError:
            return Response(status=409, response="Unable to process the requested move at this time.")

    def get(self, move_id, player_name, game_id):
        try:
            return Response(status=200, response=moves[move_id])
        except:
            return Response(status=404, response="The move you want to access cannot be found.")

    def delete(self, move_id, player_name, game_id):
        try:
            del moves[move_id]
            return Response(status=205, response="This move has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this move because it does not exist.")
'''

api_instance.add_resource(Game, '/games/<int:game_id>')
api_instance.add_resource(Player, '/games/<int:game_id>/<string:player_name>')
#api_instance.add_resource(Hand, '/games/<int:game_id>/<string:player_name>/hand/<int:hand_id>')

#api_instance.add_resource(Move, '/games/<int:game_id>/<string:player_name>/moves/<int:move_id>')




if __name__ == '__main__':
    flask_instance.run(debug=True)