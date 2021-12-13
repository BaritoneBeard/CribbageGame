import json
import random

import requests
from flask import Flask, request, Response, jsonify, make_response
from flask_restful import Resource, Api
import logging

import pegging
import scoring
from BE_Game import BE_Game
from Player_BE import Player_BE
from scoring import *
import Card
import Move
from pegging import *



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
            print("Here's my starter card: ", game_info["starter_card"])
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
            return Response(status=200, response=str(earned_points))
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


'''
How can I do Move here? In Player's make_move(), I can call POST to this Move resource here, then, using that move,
I can call the pegging class to calculate the score based on that. Update the score, and return the score.

I've already calculated the score based on the 4-card hand, so do i need to update the player's hand??? Not really,
unless I have another reason for doing it, I think it's fine.

When I bring a move in, I should make a Move object out of it. I need:
    -move_id
    -player (pass in player name, then do BE_Game.player_1 or something?)
    -moves_so_far (just add a Card object (translated from a dict coming in) to this list. moves_so_far.append(card)
    -move -- do i really need? I don't think so because the move is a Move object itself.

'''

# Player's Move comes in, a Move object is created, then passed into pegging for a score which is returned.
class MoveInstance(Resource):  # Not to be confused with the BE Move class that we import
    def post(self, game_id):
        try:
            move_id = random.randint(1,10000)

            single_move_obj = Move.create_move_instance(move_id)
            moves[move_id] = single_move_obj  # store the move instance at game_id so everyone can have access to it.

            return Response(status=201, response=str(move_id))
        except KeyError:
            return Response(status=409, response="Unable to process the requested move at this time.")

    def get(self, game_id):
        try:
            pass
            # return make_response(jsonify(moves[move_id]), 200)
        except:
            return Response(status=404, response="The move you want to access cannot be found.")

    # def put(self, player_name, game_id):
    #     try:
    #         current_game = games[game_id]
    #         if current_game.player_1.name == player_name:
    #             current_player = current_game.player_1
    #         else:
    #             current_player = current_game.player_2
    #
    #         players_move = request.form['move_card']
    #         players_move = json.loads(players_move)  # Now a dictionary.
    #         card_obj = Card.make_card(players_move)
    #
    #         player_move = Move.receive_move(move_id, card_obj)
    #         earned_points = get_score_for_move(player_move)
    #         current_player.score += earned_points

    def delete(self, game_id):
        try:
            # del moves[move_id]
            return Response(status=205, response="This move has been deleted from the game.")
        except KeyError:
            return Response(status=404, response="Cannot delete this move because it does not exist.")



class MoveAPI(Resource):
    def put(self, player_name, game_id, move_id):

        # Get the current game and move instance (Move object) associated with it.
        current_game = games[game_id]
        starter = current_game.starter_card
        print("After game_id")
        move_instance = moves[move_id]
        print("After move_id")

        # For easier purposes.
        if current_game.player_1.name == player_name:
            current_player = current_game.player_1
        else:
            current_player = current_game.player_2

        # add the incoming player's move card to your "move" attribute of your move instance.
        player_move = request.form['move_card']
        print("After requesting data")
        player_move = json.loads(player_move)  # Now a dictionary.
        print("After json loads")
        card_obj = Card.make_card(player_move)  # Now a Card object, we can pass to pegging.
        print("After making card object", card_obj)


        # TODO: OOH I need to pass in a MOVE OBJECT, not a Card object, when i call detect_illegal_move()
        # Set my move_instance.move = Card object
        # Then call illegal moves
        # Then if move is good, get score and add it to moves so far
        # Then return the score here.

        print("Move_instance should be a move: ", move_instance)
        move_instance.move = card_obj
        print("What is move? ", move_instance.move)


        # If detect illegal moves returns a True (it's an illegal move), return a response. Then on FE if response
        # is False, move to the next player.
        # if pegging.detect_illegal_move(move_instance):
        #     return Response(status=409, response=json.dumps(False))
        # else:
        earned_points_for_peg = pegging.get_score_for_move(move_instance, starter)  # Will auto append move to moves_so_far
        print("Earned points: ", earned_points_for_peg)
        current_player.score += earned_points_for_peg
        return Response(status=200, response=str(earned_points_for_peg))

            # It wasn't an illegal move, so get score, add card to moves_so_far, return score








class Crib(Resource):
    def post(self, game_id):
        try:
            current_game = games[game_id]

            # Generate a random crib_id and grab crib_list from frontend.
            crib_id = str(random.randint(1,10000))
            crib_card_list = request.form['crib_card_list']
            cards_list = json.loads(crib_card_list)  # Gives a list of card dicts (dicts with rank+suit)

            for i in range(len(cards_list)):
                new_card = Card.make_card(cards_list[i])
                current_game.crib_list.append(new_card)  # Takes dictionary, makes card out of it and adds to list

            # Store cards from crib into our current game
            # current_game.crib_list = cards_list

            flipped_card = Card.make_card(current_game.starter_card)

            # Calculate score based on cards in crib and return it. First turn each dictionary in list to Card object
            crib_score = scoring.calc_score(current_game.crib_list, flipped_card)

            return Response(status=201, response=str(crib_score))
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
api_instance.add_resource(MoveInstance, '/games/<int:game_id>/moves')  # Just for creating a Move object (setting up)
api_instance.add_resource(MoveAPI, '/games/<int:game_id>/<string:player_name>/moves/<int:move_id>')
api_instance.add_resource(Crib, '/games/<int:game_id>/cribs')



if __name__ == '__main__':
    flask_instance.run(debug=True)