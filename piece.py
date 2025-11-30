class Piece:
    def __init__(self, piece_type):
        self.type = piece_type

    def get_allowed_moves(self, board_state):
        raise NotImplementedError