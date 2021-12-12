from scoring import *



def check_run(player_move):
    moves_so_far = player_move.moves_so_far
    new_move = player_move.move

    if new_move in moves_so_far:
        moves_so_far.remove(new_move)  # just in case it was implemented in such a way

    before_add = calc_run(moves_so_far)

    moves_so_far.append(new_move)

    after_add = calc_run(moves_so_far)

    if before_add == after_add:
        return 0
    else:
        return after_add


def get_score_for_move(player_move):
    if not detect_illegal_move(player_move):
        total = calc_score(player_move.moves_so_far)    #TODO: don't want to run this EVERY time
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
    if total_rank_value > 31:
        return True
    else:
        return False
