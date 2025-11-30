# import importlib
# import game_engine
# importlib.reload(game_engine)

class Piece:
    class PieceType():
        QUEEN = 1
        ANT = 2
        SPIDER = 3
        GRASSHOPPER = 4
        BEETLE = 5

    def __init__(self, piece_type):
        self.type = piece_type

    def get_possible_moves(self, current_cell, game_state):
        raise NotImplementedError

class Ant(Piece):
    def __init__(self):
        super().__init__(self.PieceType.ANT)

    def get_possible_moves(self, current_cell, game_state):
        return game_state.get_playable_border(current_cell)