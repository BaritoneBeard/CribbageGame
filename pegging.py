from scoring import *


def check_score(player_move, func_to_call: classmethod, flipped_card = None):
    moves_so_far = player_move.moves_so_far
    new_move = player_move.move

    if new_move in moves_so_far:
        moves_so_far.remove(new_move)  # just in case it was implemented in such a way

    if flipped_card:
        before_add = func_to_call(moves_so_far, flipped_card)
    else:
        before_add = func_to_call(moves_so_far)

    moves_so_far.append(new_move)

    if flipped_card:
        after_add = func_to_call(moves_so_far, flipped_card)
    else:
        after_add = func_to_call(moves_so_far)

    if flipped_card:
        moves_so_far.remove(new_move.suit)
    else:
        moves_so_far.remove(new_move.rank)

    if before_add == after_add:
        return 0
    else:
        return after_add


def get_score_for_move(player_move, flipped_card = None):
    total = 0
    list_of_methods = [calc_run, calc_15, calc_pairs]
    if not detect_illegal_move(player_move):
        for i in list_of_methods:
            total += check_score(player_move, i)
        total += check_score(player_move, calc_flush, flipped_card)
        player_move.moves_so_far.append(player_move)                    # APPENDS PLAYER MOVE
        return total
    else:
        print("** Illegal move **")


def receive_pegging_move(player):   # Might not need due to our implementation?
    pass


def detect_illegal_move(player_move):   # What's "illegal" in cribbage?
    total_rank_value = 0

    for i in range(len(player_move.moves_so_far)):
        total_rank_value += player_move.moves_so_far[i].rank

    if player_move.move is not None:
            total_rank_value += player_move.move.rank

    # NOTE: if no moves are available, empty the moves_so_far list.
    if total_rank_value > 31:
        return True
    else:
        return False
