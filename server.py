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
    def post(self, player_name, game_ID):  # game_ID added to make add_resource work correctly.
        try:
            players[player_name] = request.form['player']
            return Response(status=201, response="Successfully created a player.")
        except KeyError:
            return Response(status=409, response="Unable to create a new player at this time.")

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


api_instance.add_resource(Game, '/games/<int:game_ID>')
api_instance.add_resource(Player, '/games/<int:game_ID>/<string:player_name>')

if __name__ == '__main__':
    flask_instance.run(debug=True)