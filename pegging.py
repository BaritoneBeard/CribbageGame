from scoring import calc_score


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
