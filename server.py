import json
import random

import requests
from flask import Flask, request, Response, jsonify, make_response
from flask_restful import Resource, Api
import logging
from BE_Game import BE_Game
from Player_BE import Player_BE
from scoring import *
import Card



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
            # Generate a random game_id + create a new BE_Game to store all information about a game.
            game_id = random.randint(1,10000)
            new_game = BE_Game(game_id)

            # store our newly create game in games so other Resources can access it
            games[game_id] = new_game

            # game_id and starter_card need to be accessed by the FE, so store in a json string and pass it
            game_info = {"game_id": game_id, "starter_card": new_game.starter_card}
            game_json = json.dumps(game_info)

            logger.info("INFO: Game Resource posted successfully.")
            return Response(status=201, response=game_json)

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



class Player(Resource):
    def post(self, player_name, game_id):
        try:
            # Access the current game
            current_game = games[int(game_id)]

            # Creates a new player if player attribute of BE_Game is None
            current_game.create_player(player_name)

            # Return the player's hand depending on which player it is
            if current_game.player_1.name == player_name:
                hand_json = json.dumps(current_game.player_1.hand)
                return Response(status=201, response=hand_json)
            else:
                hand_json = json.dumps(current_game.player_2.hand)
                return Response(status=201, response=hand_json)

        except KeyError:
            return Response(status=409, response="Unable to create a new player at this time.")

    def get(self, player_name, game_id):
        try:
            current_game = games[game_id]

            # Makes things easier for referencing the player we're talking about
            if current_game.player_1.name == player_name:
                current_player = current_game.player_1
            else:
                current_player = current_game.player_2

            return Response(status=200, response=str(current_player.score))
            # return make_response(jsonify(players[player_name]), 200)
        except:
            return Response(status=404, response="The player you are looking for cannot be found.")

    # Takes in the player's 4-card hand, stores it, calculates the score based on that hand and returns the score.
    def put(self, player_name, game_id):
        try:
            current_game = games[game_id]

            # Just to make things easier for referencing players
            if current_game.player_1.name == player_name:
                current_player = current_game.player_1
            else:
                current_player = current_game.player_2

            # Grabs incoming data as player's updated hand and updates BE_Game's player hand (depending on who it is)
            updated_player_hand = request.form['updated_player_hand']
            updated_player_hand = json.loads(updated_player_hand)  # Takes the json string and makes it a list again.

            current_player.hand = updated_player_hand

            # Convert my list of dictionaries into a list of Card objects before we call scoring.
            player_list_of_cards = []
            for i in range(len(current_game.player_1.hand)):
                convert_to_card = Card.make_card(current_game.player_1.hand[i])
                player_list_of_cards.append(convert_to_card)

            # Call scoring.py method, update the player's score, then return the score in the response.
            earned_points = calc_score(player_list_of_cards)
            current_player.score += earned_points
            return Response(status=200, response=str(current_player.score))
        except:
            return Response(status=404, response="Could not update player's hand and return new score.")

    def delete(self, player_name, game_id):
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
            # Generate a random crib_id and grab crib_list from frontend.
            crib_id = str(random.randint(1,10000))
            crib_card_list = request.form['crib_card_list']
            cards_list = json.loads(crib_card_list)  # Gives a list of card dicts (dicts with rank+suit)

            # Store cards from crib into our current game
            current_game = games[game_id]
            current_game.crib_list = cards_list

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