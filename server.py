from flask import Flask, request, Response
from flask_restful import Resource, Api

flask_instance = Flask(__name__)
api_instance = Api(flask_instance)

games = {}  # holds game resources
players = {}  # used to hold player resources
hands = {}  # holds hand resources for players


class Game(Resource):
    def post(self, game_ID):
        try:
            games[game_ID] = request.form['game_ID']
            return Response(status=201, response="Successfully created the game.")
        except KeyError:
            return Response(status=409, response="Unable to create a game at this time.")

    def get(self, game_ID):
        try:
            return Response(status=200, response=games[game_ID]) # Using game_ID to get the game object.
        except KeyError:
            return Response(status=404, response="The game you are looking for cannot be found.")

    def delete(self, game_ID):
        try:
            del games[game_ID]
            return Response(status=205, response="Your game has been deleted.")
        except KeyError:
            return Response(status=404, response="Cannot delete game because it does not exist.")


class Player(Resource):
    def post(self, player_name, game_ID):  # game_ID needed to make add_resource method work
        try:
            players[player_name] = request.form['player']
            return Response(status=201, response="Successfully created a player.")
        except KeyError:
            return Response(status=409, response="Unable to create a new player at this time.")

    # Potentially need to check if the game exists first before trying to access the player.
    def get(self, player_name, game_ID):
        try:
            return Response(status=200, response=players[player_name])
        except:
            return Response(status=404, response="The player you are looking for cannot be found.")

    def delete(self, player_name, game_ID):
        try:
            del players[player_name]
            return Response(status=205, response="Player has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete player because it does not exist.")


class Hand(Resource):
    def post(self, hand_ID, player_name, game_ID):  # player_name and game_ID needed to make add_resource method work
        try:
            hands[hand_ID] = request.form['hand_ID']
            return Response(status=201, response="Successfully created a a hand for player.")
        except KeyError:
            return Response(status=409, response="Unable to create a new hand for player at this time.")

    def get(self, hand_ID, player_name, game_ID):
        try:
            return Response(status=200, response=hands[hand_ID])
        except:
            return Response(status=404, response="The hand you want to retrieve cannot be found.")

    def delete(self, hand_ID, player_name, game_ID):
        try:
            del hands[hand_ID]
            return Response(status=205, response="This hand has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this hand because it does not exist.")


# There will only be 1 crib per game. A crib is just a hand.
# class Crib(Resource):
#     def post(self, hand_ID, player_name, game_ID):
#         try:
#             hands[hand_ID] = request.form['hand_ID']
#             return Response(status=201, response="Successfully created a a hand for player.")
#         except KeyError:
#             return Response(status=409, response="Unable to create a new hand for player at this time.")
#
#     def get(self, hand_ID, player_name, game_ID):
#         try:
#             return Response(status=200, response=hands[hand_ID])
#         except:
#             return Response(status=404, response="The hand you want to retrieve cannot be found.")
#
#     def delete(self, hand_ID, player_name, game_ID):
#         try:
#             del hands[hand_ID]
#             return Response(status=205, response="This hand has been deleted from the game.")
#         except KeyError:
#             return Response(status=404, response="Cannot delete this hand because it does not exist.")


api_instance.add_resource(Game, '/games/<int:game_ID>')
api_instance.add_resource(Player, '/games/<int:game_ID>/<string:player_name>')
api_instance.add_resource(Hand, '/games/<int:game_ID>/<string:player_name>/<int:hand_ID>')

if __name__ == '__main__':
    flask_instance.run(debug=True)