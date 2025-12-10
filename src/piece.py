import copy

from src.cell import GridCoordinates
from src.texture import Texture
from src.move import Move

class Piece:
    class PieceType:
        QUEEN = "queen"
        ANT = "ant"
        SPIDER = "spider"
        GRASSHOPPER = "grasshopper"
        BEETLE = "beetle"
        MOSQUITTO = "mosquito"
        LADYBUG = "ladybug"
        PILLBUG = "pillbug"

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
        if self.type == Piece.PieceType.PILLBUG and self.color == Piece.PieceColour.BLACK:
            self.texture = Texture.TextureType.BLACK_PILLBUG
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
        if self.type == Piece.PieceType.PILLBUG and self.color == Piece.PieceColour.WHITE:
            self.texture = Texture.TextureType.WHITE_PILLBUG

    def __repr__(self):
        return f"{self.color} {self.type}"

    def piece_movement_pattern(self, game_state):
        raise NotImplementedError

    def get_possible_moves(self, game_state):
        coord = self.coord
        #Look for position where to place
        if coord is None:
            return game_state.get_possible_placements(self)
        else:
            if not game_state.piece_movable(self):
                return []
            else:
                return self.piece_movement_pattern(game_state)

class Ant(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.ANT, colour)

    def piece_movement_pattern(self, game_state):
        return self.flood_fill_ant(self.coord, game_state)

    #FIXME Ant can't move from inside of island even if it follows freedom of move rule.
    # On contrary, when there is cell at the edge of island which is NOT reachable by
    # freedom of move, ant selects this cell!
    def flood_fill_ant(self, start_coord, game_state, visited=None):
        if visited is None:
            visited = set()
        if not start_coord == self.coord:
            visited.add(game_state.get_cell(start_coord))
        for empty_neighbor in game_state.get_empty_neighbors(start_coord):
            # Check if the only neighbor isn't the piece - then don't include it to playable border
            occupied = game_state.get_occupied_neighbors(empty_neighbor.coord)
            if len(occupied) == 1:
                if occupied[0].coord == self.coord:
                    continue
            if (len(game_state.get_occupied_neighbors(empty_neighbor.coord)) > 0 and
                    game_state.freedom_to_move(start_coord, empty_neighbor.coord) and
                    empty_neighbor not in visited):
                self.flood_fill_ant(empty_neighbor.coord, game_state, visited)
        return visited

# FIXME Queen can skip over the bay and it shouldn't
class Queen(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.QUEEN, colour)

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        possible_moves = []
        queen_cell = game_state.get_cell(coord)
        for neighbor in game_state.get_empty_neighbors(queen_cell.coord):
            if  (game_state.freedom_to_move(coord, neighbor.coord) and
                (len(game_state.get_occupied_neighbors(neighbor.coord)) > 1)):
                possible_moves.append(neighbor)
        return possible_moves

class Grasshopper(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.GRASSHOPPER, colour)

    def piece_movement_pattern(self,  game_state):
        coord = self.coord
        possible_placements = []
        for neighbor in game_state.get_occupied_neighbors(coord):
            direction = neighbor.coord - coord
            new_coord = neighbor.coord
            while game_state.get_cell(new_coord).has_piece():
                new_coord += direction
            possible_placements.append(game_state.get_cell(new_coord))
        return possible_placements

class Beetle(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.BEETLE, colour)

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        possible_moves = []
        # levels indexed from 1, level 0 is empty cell
        level = game_state.get_cell(coord).get_pieces().index(self) + 1
        beetle_cell = game_state.get_cell(coord)
        for neighbor in game_state.get_neighbors(beetle_cell.coord):
            neighbor_height = len(neighbor.get_pieces())
            if (game_state.freedom_to_move(coord, neighbor.coord, level) and
                (len(game_state.get_occupied_neighbors(neighbor.coord)) > 1)):
                possible_moves.append(neighbor)
            # Allow jumping to the higher level
            elif (neighbor_height >= level and
                game_state.freedom_to_move(coord, neighbor.coord, neighbor_height + 1)):
                possible_moves.append(neighbor)
        return possible_moves

#FIXME Doesn't check all adjecent pieces - or it looks like that
class Mosquito(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.MOSQUITTO, colour)

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        level = game_state.get_cell(coord).get_pieces().index(self) + 1
        game_copy = copy.deepcopy(game_state)
        new_piece_type = None
        if len(game_state.get_occupied_neighbors(coord)) == 1:
            if game_state.get_occupied_neighbors(coord)[0].get_top_piece().type == Piece.PieceType.MOSQUITTO:
                return []
        if level > 1:
            new_piece_type = Beetle(self.color)
        else:
            for neighbor in game_state.get_occupied_neighbors(coord):
                top_piece_type = neighbor.get_top_piece().type
                if top_piece_type == Piece.PieceType.QUEEN:
                    new_piece_type = Queen(self.color)
                elif top_piece_type == Piece.PieceType.ANT:
                    new_piece_type = Ant(self.color)
                elif top_piece_type == Piece.PieceType.GRASSHOPPER:
                    new_piece_type = Grasshopper(self.color)
                elif top_piece_type == Piece.PieceType.BEETLE:
                    new_piece_type = Beetle(self.color)
                elif top_piece_type == Piece.PieceType.SPIDER:
                    new_piece_type = Spider(self.color)
                elif top_piece_type == Piece.PieceType.LADYBUG:
                    new_piece_type = Ladybug(self.color)
                elif top_piece_type == Piece.PieceType.PILLBUG:
                    new_piece_type = Pillbug(self.color)

        if new_piece_type is None:
            return []
        else:
            piece = None
            for p in game_copy.get_cell(coord).get_pieces():
                if p.type == self.type and p.color == self.color:
                    piece = p
            game_copy.get_cell(coord).remove_piece(piece)
            game_copy.get_cell(coord).add_piece(new_piece_type)
            return new_piece_type.piece_movement_pattern(game_copy)

class Spider(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.SPIDER, colour)

    def piece_movement_pattern(self, game_state):
        return self.flood_fill_spider(self.coord, game_state)

    def flood_fill_spider(self, start_coord, game_state, visited = None, depth = 0, possible_placements = None):
        if visited is None:
            visited = {}
            visited[start_coord] = depth
            possible_placements = set()

            # Copy gaem and also piece (using copy_move_object) but using only piece copy
            game_state = copy.deepcopy(game_state)
            move = Move(self.coord, self.coord, self)
            move_copy = game_state.copy_move_object(game_state, move)
            game_state.get_cell(self.coord).remove_piece(move_copy.piece)

        for empty_neighbor in game_state.get_empty_neighbors(start_coord):
            current_neighbors = game_state.get_occupied_neighbors(start_coord)
            neighbor_neighbors = game_state.get_occupied_neighbors(empty_neighbor.coord)
            intersection = set(current_neighbors).intersection(set(neighbor_neighbors))
            if game_state.freedom_to_move(start_coord, empty_neighbor.coord) and len(intersection) > 0:
                # This is to make sure that we always follow the island edge and we never
                # "jump over the bay"
                if len(intersection) == 1:
                    if list(intersection)[0].coord == self.coord:
                        continue
                if depth == 3 and (empty_neighbor.coord not in visited):
                    possible_placements.add(game_state.get_cell(start_coord))
                else:
                    if (empty_neighbor.coord not in visited) or (visited[empty_neighbor.coord] > depth):
                        visited[empty_neighbor.coord] = depth
                        self.flood_fill_spider(empty_neighbor.coord, game_state, visited, depth + 1, possible_placements)
        return possible_placements

class Ladybug(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.LADYBUG, colour)

    def piece_movement_pattern(self, game_state):
        #TODO implement me
        return

class Pillbug(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.PILLBUG, colour)

    def piece_movement_pattern(self, game_state):
        #TODO implement me
        return