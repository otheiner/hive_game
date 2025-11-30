# import importlib
# import game_engine
# importlib.reload(game_engine)

ANT = 1
QUEEN = 2

class Piece:
    def __init__(self, piece_type):
        self.type = piece_type

    def get_allowed_moves(self, current_cell, game_state):
        raise NotImplementedError

class Ant(Piece):
    def __init__(self):
        super().__init__(ANT)

    def get_allowed_moves(self, current_cell, game_state):
        if not game_state.move_preserves_continuity(current_cell):
            print("Warning: this piece cannot be moved")
            return []
        else:
            return game_state.get_playable_border(current_cell)