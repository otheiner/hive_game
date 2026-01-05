from enum import Enum

from src.texture import Texture
from src.move import Move

class Piece:
    class PieceType(Enum):
        QUEEN = "queen"
        ANT = "ant"
        SPIDER = "spider"
        GRASSHOPPER = "grasshopper"
        BEETLE = "beetle"
        MOSQUITTO = "mosquito"
        LADYBUG = "ladybug"
        PILLBUG = "pillbug"

    class PieceColour(Enum):
        BLACK = "black"
        WHITE = "white"

    # Precompute mapping once
    TEXTURE_MAP = {
        (PieceType.QUEEN, PieceColour.BLACK): Texture.TextureType.BLACK_QUEEN,
        (PieceType.ANT, PieceColour.BLACK): Texture.TextureType.BLACK_ANT,
        (PieceType.SPIDER, PieceColour.BLACK): Texture.TextureType.BLACK_SPIDER,
        (PieceType.GRASSHOPPER, PieceColour.BLACK): Texture.TextureType.BLACK_GRASSHOPPER,
        (PieceType.BEETLE, PieceColour.BLACK): Texture.TextureType.BLACK_BEETLE,
        (PieceType.MOSQUITTO, PieceColour.BLACK): Texture.TextureType.BLACK_MOSQUITTO,
        (PieceType.LADYBUG, PieceColour.BLACK): Texture.TextureType.BLACK_LADYBUG,
        (PieceType.PILLBUG, PieceColour.BLACK): Texture.TextureType.BLACK_PILLBUG,
        (PieceType.QUEEN, PieceColour.WHITE): Texture.TextureType.WHITE_QUEEN,
        (PieceType.ANT, PieceColour.WHITE): Texture.TextureType.WHITE_ANT,
        (PieceType.SPIDER, PieceColour.WHITE): Texture.TextureType.WHITE_SPIDER,
        (PieceType.GRASSHOPPER, PieceColour.WHITE): Texture.TextureType.WHITE_GRASSHOPPER,
        (PieceType.BEETLE, PieceColour.WHITE): Texture.TextureType.WHITE_BEETLE,
        (PieceType.MOSQUITTO, PieceColour.WHITE): Texture.TextureType.WHITE_MOSQUITTO,
        (PieceType.LADYBUG, PieceColour.WHITE): Texture.TextureType.WHITE_LADYBUG,
        (PieceType.PILLBUG, PieceColour.WHITE): Texture.TextureType.WHITE_PILLBUG,
    }

    def __init__(self, piece_type, piece_color):
        self.type = piece_type
        self.color = piece_color
        self.coord = None
        self.texture = self.TEXTURE_MAP[(self.type, self.color)]

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
            return self.piece_movement_pattern(game_state)

class Ant(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.ANT, colour)

    def piece_movement_pattern(self, game_state):
        return self.flood_fill_ant(self.coord, game_state)

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
                    game_state.have_common_occupied_neighbor(empty_neighbor.coord, start_coord) and
                    empty_neighbor not in visited):
                self.flood_fill_ant(empty_neighbor.coord, game_state, visited)
        return visited

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.QUEEN, colour)

    def occupied_neighbors(self, game_state):
        return len(game_state.get_occupied_neighbors(self.coord))

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        possible_moves = []
        queen_cell = game_state.get_cell(coord)
        empty_queen_neighbors = game_state.get_empty_neighbors(queen_cell.coord)
        for neighbor in empty_queen_neighbors:
            if ((neighbor not in possible_moves) and
                game_state.have_common_occupied_neighbor(coord, neighbor.coord) and
                game_state.freedom_to_move(coord, neighbor.coord)):
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

#FIXME This is not working well when  beetle is on top of stack and should move
# on to of stack on opponent's piece - I don't know why
# TODO: Beetle can jump "over the bay"
class Beetle(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.BEETLE, colour)

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        possible_moves = []
        print("beetle")
        # levels indexed from 1, level 0 is empty cell
        #TODO Not sure if there shouldn't be + 2
        level = game_state.get_cell(coord).get_pieces().index(self) + 1
        beetle_cell = game_state.get_cell(coord)
        for neighbor in game_state.get_neighbors(beetle_cell.coord):
            neighbor_height = len(neighbor.get_pieces())
            if (game_state.freedom_to_move(coord, neighbor.coord, level) and
                (len(game_state.get_occupied_neighbors(neighbor.coord)) > 1)):
                print("appending 1")
                possible_moves.append(neighbor)
            # Allow jumping to the higher level
            elif (neighbor_height >= level and
                game_state.freedom_to_move(coord, neighbor.coord, neighbor_height + 1)):
                print("appending 2")
                possible_moves.append(neighbor)
        return possible_moves

class Mosquito(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.MOSQUITTO, colour)

    def piece_movement_pattern(self, game_state):
        coord = self.coord
        level = game_state.get_cell(coord).get_pieces().index(self) + 1
        new_piece_type = None
        possible_moves = []
        if len(game_state.get_occupied_neighbors(coord)) == 1:
            if game_state.get_occupied_neighbors(coord)[0].get_top_piece().type == Piece.PieceType.MOSQUITTO:
                return []
        if level > 1:
            new_piece_type = Beetle(self.color)
            game_state.get_cell(coord).remove_piece(self)
            game_state.get_cell(coord).add_piece(new_piece_type)
            possible_moves = new_piece_type.piece_movement_pattern(game_state)
            game_state.get_cell(coord).remove_piece(new_piece_type)
            game_state.get_cell(coord).add_piece(self)
            return possible_moves
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
                    game_state.get_cell(coord).remove_piece(self)
                    game_state.get_cell(coord).add_piece(new_piece_type)
                    for placement in new_piece_type.piece_movement_pattern(game_state):
                        if placement not in possible_moves:
                            possible_moves.append(placement)
                    game_state.get_cell(coord).remove_piece(new_piece_type)
                    game_state.get_cell(coord).add_piece(self)

        return possible_moves

class Spider(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.SPIDER, colour)

    def piece_movement_pattern(self, game_state):
        return self.dfs_spider(self.coord, game_state)

    def dfs_spider(self, start_coord, game_state, visited = None, possible_moves=None, depth=0):
        if visited is None:
            visited = {start_coord : depth}
            possible_moves = set()

        if depth == 3:
            if start_coord not in possible_moves:
                possible_moves.add(game_state.get_cell(start_coord))
        if depth < 3:
            for empty_neighbor in game_state.get_empty_neighbors(start_coord):
                if (game_state.have_common_occupied_neighbor(start_coord, empty_neighbor.coord) and
                    game_state.freedom_to_move(start_coord, empty_neighbor.coord)):
                    move = Move(start_coord, empty_neighbor.coord, self)
                    game_state._move_piece(move, testing=True)

                    if empty_neighbor.coord not in visited.keys():
                        visited[empty_neighbor.coord] = depth
                        self.dfs_spider(empty_neighbor.coord, game_state, visited, possible_moves, depth + 1)
                        visited.pop(empty_neighbor.coord)

                    game_state._move_piece_backwards(move)
        return possible_moves

class Ladybug(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.LADYBUG, colour)

    def piece_movement_pattern(self, game_state):
        return self.dfs_ladybug(self.coord, game_state)

    def dfs_ladybug(self, start_coord, game_state, depth = 0, possible_placements = None, original_piece_coord=None):
        if possible_placements is None:
            possible_placements = set()
            original_piece_coord = self.coord

        if depth == 0 or depth == 1:
            for neighbor in game_state.get_occupied_neighbors(start_coord):
                move = Move(start_coord, neighbor.coord, self)
                game_state._move_piece(move, testing=True)
                self.dfs_ladybug(neighbor.coord, game_state, depth + 1, possible_placements, original_piece_coord)
                game_state._move_piece_backwards(move)
        if depth == 2:
            for neighbor in game_state.get_empty_neighbors(start_coord):
                if (neighbor not in possible_placements) and (neighbor.coord != original_piece_coord):
                    possible_placements.add(neighbor)

        return possible_placements

# TODO Implement movement of this piece - it is too many rules, so I am leaving it for later
#  since it is not in the original game edition
class Pillbug(Piece):
    def __init__(self, colour):
        super().__init__(self.PieceType.PILLBUG, colour)

    def piece_movement_pattern(self, game_state):
        #TODO implement me
        return