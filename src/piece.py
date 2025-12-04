from texture import Texture



class Piece:
    class PieceType:
        QUEEN = "queen"
        ANT = "ant"
        SPIDER = "spider"
        GRASSHOPPER = "grasshopper"
        BEETLE = "beetle"
        MOSQUITTO = "mosquito"
        LADYBUG = "ladybug"

    class PieceColour():
        BLACK = "black"
        WHITE = "white"

    def __init__(self, piece_type, piece_color):
        self.type = piece_type
        self.color = piece_color
        self.coord = None
        if self.type == Piece.PieceType.QUEEN and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_QUEEN
        if self.type == Piece.PieceType.ANT and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_ANT
        if self.type == Piece.PieceType.BEETLE and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_BEETLE
        if self.type == Piece.PieceType.GRASSHOPPER and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_GRASSHOPPER
        if self.type == Piece.PieceType.SPIDER and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_SPIDER
        if self.type == Piece.PieceType.MOSQUITTO and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_MOSQUITTO
        if self.type == Piece.PieceType.LADYBUG and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_LADYBUG
        if self.type == Piece.PieceType.QUEEN and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_QUEEN
        if self.type == Piece.PieceType.ANT and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_ANT
        if self.type == Piece.PieceType.BEETLE and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_BEETLE
        if self.type == Piece.PieceType.GRASSHOPPER and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_GRASSHOPPER
        if self.type == Piece.PieceType.SPIDER and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_SPIDER
        if self.type == Piece.PieceType.MOSQUITTO and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_MOSQUITTO
        if self.type == Piece.PieceType.LADYBUG and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_LADYBUG

    def __repr__(self):
        return f"{self.color} {self.type}"

    def get_possible_moves(self, game_state):
        raise NotImplementedError

class Ant(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.ANT, colour)

    #TODO implement freedom to move rule
    def get_possible_moves(self, game_state):
        coord = self.coord
        #Look for position where to place
        if coord is None:
            return game_state.get_possible_placements(self)
        else:
            return game_state.get_playable_border(coord)

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.QUEEN, colour)

    def get_possible_moves(self, game_state):
        #TODO implement me (don't forget sliding rule)
        coord = self.coord
        if coord is None:
            return game_state.get_possible_placements(self)
        else:
            outer_border_without_queen = game_state.get_playable_border(self.coord)
            print(f"Outer border without queen: {outer_border_without_queen}")
            # If queen is not on outer border, it cannot move (freedom to move rule)
            if not game_state.get_cell(coord) in outer_border_without_queen:
                print("test1")
                return []
            # If queen can move return intersection of queen neighbours with playable border
            else:
                print("test2")
                possible_moves = []
                queen_neighbours = game_state.get_empty_neighbors(coord)
                for neighbour in queen_neighbours:
                    if neighbour in outer_border_without_queen:
                        possible_moves.append(neighbour)
                return possible_moves

class Spider(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.SPIDER, colour)

    def get_possible_moves(self, game_state):
        #TODO implement me
        return

class Grasshopper(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.GRASSHOPPER, colour)

    def get_possible_moves(self,  game_state):
        #TODO implement me
        return

class Beetle(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.BEETLE, colour)

    def get_possible_moves(self, game_state):
        #TODO implement me
        return

class Mosquito(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.MOSQUITTO, colour)

    def get_possible_moves(self, game_state):
        #TODO implement me
        return

class Ladybug(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.LADYBUG, colour)

    def get_possible_moves(self, game_state):
        #TODO implement me
        return