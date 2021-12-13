
move_id_list = []
localhost_url = 'http://127.0.0.1:5000/'


class Move:
    def __init__(self, move_id):
        self.move = None
        self.move_id = move_id  # identifies / categorizing the different moves
        self.moves_so_far = []  # list of Card objects



def create_move_instance(move_id):
    new_move = Move(move_id)
    return new_move
