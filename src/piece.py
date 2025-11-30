# import importlib
# import game_engine
# importlib.reload(game_engine)

class Piece:
    class PieceType():
        QUEEN = "queen"
        ANT = "ant"
        SPIDER = "spider"
        GRASSHOPPER = "grasshopper"
        BEETLE = "beetle"

    class PieceColour():
        BLACK = "black"
        WHITE = "white"

    def __init__(self, piece_type, piece_color):
        self.type = piece_type
        self.color = piece_color

    def __repr__(self):
        return f"{self.color} {self.type}"

    def get_possible_moves(self, current_cell, game_state):
        raise NotImplementedError

class Ant(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.ANT, colour)

    def get_possible_moves(self, coord, game_state):
        return game_state.get_playable_border(coord)

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.QUEEN, colour)

    def get_possible_moves(self, coord, game_state):
        #TODO implement me
        return

class Spider(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.SPIDER, colour)

    def get_possible_moves(self, coord, game_state):
        #TODO implement me
        return

class Grasshopper(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.GRASSHOPPER, colour)

    def get_possible_moves(self, coord, game_state):
        #TODO implement me
        return

class Beetle(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.BEETLE, colour)

    def get_possible_moves(self, coord, game_state):
        #TODO implement me
        return