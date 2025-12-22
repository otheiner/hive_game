import importlib
from enum import IntEnum

import src.board as board_lib
import src.piece as piece_lib
from src.cell import GridCoordinates
from src.cell import Cell
from src.move import Move

importlib.reload(board_lib)
importlib.reload(piece_lib)
from src.board import Board
from src.piece import Piece, Ant, Queen, Spider, Grasshopper, Beetle, Mosquito, Ladybug


class Log():
    class DebugLevel(IntEnum):
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3

        def __str__(self):
            return self.name

    def __init__(self, message, log_level):
        self.message = message
        self.log_level = log_level

    def __repr__(self):
        return f"{self.log_level}: {self.message}"

    def __str__(self):
        return f"{self.log_level}: {self.message}"

class Logbook():
    def __init__(self, log_level):
        self.messages = []
        self.log_level = Log.DebugLevel.INFO

    def add(self, message, debug_level = Log.DebugLevel.INFO):
        log = Log(message, debug_level)
        if self.log_level <= debug_level:
            self.messages.append(log)
            print(log)

    def debug(self, message):
        log = Log(message, Log.DebugLevel.DEBUG)
        if self.log_level <= Log.DebugLevel.DEBUG:
            self.messages.append(log)
            print(log)

    def info(self, message):
        log = Log(message, Log.DebugLevel.INFO)
        if self.log_level <= Log.DebugLevel.INFO:
            self.messages.append(log)
            print(log)

    def warning(self, message):
        log = Log(message, Log.DebugLevel.WARNING)
        if self.log_level <= Log.DebugLevel.WARNING:
            self.messages.append(log)
            print(log)

    def error(self, message):
        log = Log(message, Log.DebugLevel.ERROR)
        if self.log_level <= Log.DebugLevel.ERROR:
            self.messages.append(log)
            print(log)

class Game(Board):
    def __init__(self, halfwidth=30):
        super().__init__(halfwidth)
        self.logs = Logbook(Log.DebugLevel.INFO)
        self.winning_state = False
        self.white_turn = True
        self.white_queen_placed = False
        self.black_queen_placed = False
        self.round_counter = 1
        # self.bridges_in_current_state = set()
        self.piece_bank = { "white": {"queen": Queen(Piece.PieceColour.WHITE),
                                     "spider1": Spider(Piece.PieceColour.WHITE),
                                     "spider2": Spider(Piece.PieceColour.WHITE),
                                     "beetle1": Beetle(Piece.PieceColour.WHITE),
                                     "beetle2": Beetle(Piece.PieceColour.WHITE),
                                     "grasshopper1": Grasshopper(Piece.PieceColour.WHITE),
                                     "grasshopper2": Grasshopper(Piece.PieceColour.WHITE),
                                     "grasshopper3": Grasshopper(Piece.PieceColour.WHITE),
                                     "ant1": Ant(Piece.PieceColour.WHITE),
                                     "ant2": Ant(Piece.PieceColour.WHITE),
                                     "ant3": Ant(Piece.PieceColour.WHITE),
                                     "mosquito": Mosquito(Piece.PieceColour.WHITE),
                                     "ladybug": Ladybug(Piece.PieceColour.WHITE)
                                     },
                            "black" : {"queen": Queen(Piece.PieceColour.BLACK),
                                     "spider1": Spider(Piece.PieceColour.BLACK),
                                     "spider2": Spider(Piece.PieceColour.BLACK),
                                     "beetle1": Beetle(Piece.PieceColour.BLACK),
                                     "beetle2": Beetle(Piece.PieceColour.BLACK),
                                     "grasshopper1": Grasshopper(Piece.PieceColour.BLACK),
                                     "grasshopper2": Grasshopper(Piece.PieceColour.BLACK),
                                     "grasshopper3": Grasshopper(Piece.PieceColour.BLACK),
                                     "ant1": Ant(Piece.PieceColour.BLACK),
                                     "ant2": Ant(Piece.PieceColour.BLACK),
                                     "ant3": Ant(Piece.PieceColour.BLACK),
                                     "mosquito": Mosquito(Piece.PieceColour.BLACK),
                                     "ladybug": Ladybug(Piece.PieceColour.BLACK)
                                     }
                            }

    @staticmethod
    def print_cells(cells):
        for cell in cells:
            cell.print_cell()

    def check_win(self):
        white_queen_coord = self.piece_bank["white"]["queen"].coord
        black_queen_coord = self.piece_bank["black"]["queen"].coord
        self.logs.debug(f"White queen neighbours: {self.get_occupied_neighbors(white_queen_coord)}")
        self.logs.debug(f"Black queen neighbours: {self.get_occupied_neighbors(white_queen_coord)}")
        white_winner = False
        black_winner = False
        if len(self.get_occupied_neighbors(white_queen_coord)) == 6:
            self.winning_state = True
            black_winner = True
        if len(self.get_occupied_neighbors(black_queen_coord)) == 6:
            self.winning_state = True
            white_winner = True

        self.logs.debug(f"Checking winning state: {self.winning_state}")

        # This would be weird situation, but it would be a draw. Both queens have 6 neighbours.
        if white_winner and black_winner:
            return "How did you manage to do this?! This is draw!"
        # White is winner
        if white_winner and not black_winner:
            return "White wins!"
        # Black is winner
        if white_winner and black_winner:
            return "Black wins!"

        return False

    def get_piece_bank(self, piece_color):
        if piece_color == Piece.PieceColour.BLACK:
            return self.piece_bank["black"]
        elif piece_color == Piece.PieceColour.WHITE:
            return self.piece_bank["white"]
        else:
            raise ValueError(f"Piece has some weird colour - should be BLACK or WHITE")

    # def get_neighbors(self, coord):
    #     neighbors = []
    #     if coord is None:
    #         return neighbors
    #     for dq, dr, ds in Board.HEX_DIRECTIONS:
    #         key = (coord.q + dq, coord.r + dr, coord.s + ds)
    #         cell = self.cells.get(key)
    #         if cell is not None:
    #             neighbors.append(cell)
    #     return neighbors

   #FIXME This doesn't work with Minimax AI /the old version - commented out above) works.
    def get_neighbors(self, coord):
        if coord is None:
            return []
        neighbors = self.neighbors.get(coord)
        if neighbors is not None:
            return neighbors
        else:
            self.neighbors[coord] = []
            for dq, dr, ds in Board.HEX_DIRECTIONS:
                key = (coord.q + dq, coord.r + dr, coord.s + ds)
                cell = self.cells.get(key)
                if cell is not None:
                    self.neighbors[coord].append(cell)
                else:
                    self.cells[key] = Cell(key)
                    cell = self.cells.get(key)
                    self.neighbors[coord].append(cell)
            return self.neighbors.get(coord)

    def update_stats(self, backwards=False):
        self.white_turn = not self.white_turn
        #self.find_bridges()
        if not backwards:
            if self.white_turn:
                self.round_counter += 1
        else:
            if not self.white_turn:
                self.round_counter -= 1

    def have_common_occupied_neighbor(self, coord1, coord2):
        neighbors1 = self.get_occupied_neighbors(coord1)
        neighbors2 = self.get_occupied_neighbors(coord2)
        if len(set(neighbors1).intersection(set(neighbors2))) > 0 :
            return True
        else:
            return False

    def get_common_neighbors(self, coord1, coord2):
        neighbors1 = self.get_neighbors(coord1)
        neighbors2 = self.get_neighbors(coord2)
        return set(neighbors1).intersection(set(neighbors2))

    def get_occupied_cells(self):
        occupied_cells = []
        for cell in self.cells.values():
            if cell.has_piece():
                occupied_cells.append(cell)
        return occupied_cells

    def get_occupied_neighbors(self, coord):
        neighbours = self.get_neighbors(coord)
        occupied_neighbours = []
        if coord is None:
            return occupied_neighbours
        for neighbour in neighbours:
            if neighbour.has_piece():
                occupied_neighbours.append(neighbour)
        return occupied_neighbours

    def get_empty_neighbors(self, coord):
        neighbours = self.get_neighbors(coord)
        empty_neighbours = []
        if coord is None:
            return empty_neighbours
        for neighbour in neighbours:
            if not neighbour.has_piece():
                empty_neighbours.append(neighbour)
        return empty_neighbours

    def get_connected_cells(self, start_coord, visited=None):
        if start_coord is None:
            return []
        if visited is None:
            visited = set()
        visited.add(self.get_cell(start_coord))
        for neighbour in self.get_occupied_neighbors(start_coord):
            if neighbour not in visited:
                self.get_connected_cells(neighbour.coord, visited)
        return visited

    # Returns array of tuples (cell in island, distance_from_origin)
    def get_connected_cells_with_distances(self, start_coord, visited=None, origin_coord=None):
        if start_coord is None:
            return {}
        if visited is None:
            origin_coord = start_coord
            visited = {}
        distance = GridCoordinates.distance(start_coord, origin_coord)
        visited[self.get_cell(start_coord)] = distance
        for neighbour in self.get_occupied_neighbors(start_coord):
            if neighbour not in visited:
                self.get_connected_cells_with_distances(neighbour.coord, visited, origin_coord)
        return visited

    def is_piece_on_top(self, piece):
        piece_cell = self.get_cell(piece.coord)
        if piece_cell.get_top_piece() == piece:
            return True
        else:
            return False

    def piece_can_be_lifted(self,piece):
        piece_coord = piece.coord
        self.get_cell(piece.coord).remove_piece(piece)
        if self.is_valid_state():
            state_is_valid = True
        else:
            state_is_valid = False
        self.get_cell(piece_coord).add_piece(piece)
        return state_is_valid

    def is_valid_state(self):
        occupied_cells = self.get_occupied_cells()
        if len(occupied_cells) == len(self.get_connected_cells(occupied_cells[0].coord)):
            return True
        else:
            return False

    # Checks freedom to move only if two cells are neighboring, if they are not - returns false
    def freedom_to_move(self, coord_from, coord_to, level = 1):
        cell_from = self.get_cell(coord_from)
        cell_to = self.get_cell(coord_to)
        direction_between_cells = (cell_to.coord.q - cell_from.coord.q,
                                   cell_to.coord.r - cell_from.coord.r,
                                   cell_to.coord.s - cell_from.coord.s)

        # Piece is in bank - it can move to any cell (check if the cell on the playable border is not done here)
        if coord_from is None:
            return True
        # Moving back to bank is not possible
        if coord_to is None:
            return False

        if direction_between_cells == Board.HEX_DIRECTIONS[0]:
            bottleneck_left = Board.HEX_DIRECTIONS[1]
            bottleneck_right = Board.HEX_DIRECTIONS[5]
        elif direction_between_cells == Board.HEX_DIRECTIONS[1]:
            bottleneck_left = Board.HEX_DIRECTIONS[2]
            bottleneck_right = Board.HEX_DIRECTIONS[0]
        elif direction_between_cells == Board.HEX_DIRECTIONS[2]:
            bottleneck_left = Board.HEX_DIRECTIONS[3]
            bottleneck_right = Board.HEX_DIRECTIONS[1]
        elif direction_between_cells == Board.HEX_DIRECTIONS[3]:
            bottleneck_left = Board.HEX_DIRECTIONS[2]
            bottleneck_right = Board.HEX_DIRECTIONS[4]
        elif direction_between_cells == Board.HEX_DIRECTIONS[4]:
            bottleneck_left = Board.HEX_DIRECTIONS[3]
            bottleneck_right = Board.HEX_DIRECTIONS[5]
        elif direction_between_cells == Board.HEX_DIRECTIONS[5]:
            bottleneck_left = Board.HEX_DIRECTIONS[0]
            bottleneck_right = Board.HEX_DIRECTIONS[4]
        # Cells are not neighboring
        else:
            return False

        bottleneck_left_cell = self.get_cell(GridCoordinates(cell_from.coord.q + bottleneck_left[0],
                                                             cell_from.coord.r + bottleneck_left[1],
                                                             cell_from.coord.s + bottleneck_left[2]))
        bottleneck_right_cell = self.get_cell(GridCoordinates(cell_from.coord.q + bottleneck_right[0],
                                                              cell_from.coord.r + bottleneck_right[1],
                                                              cell_from.coord.s + bottleneck_right[2]))
        self.logs.debug(f"Freedom-to-move: from: {cell_from.coord}, to: {cell_to.coord}, L: {bottleneck_left_cell.coord}, R: {bottleneck_right_cell.coord}")

        # This can happen when we are at the edge of the game field
        #TODO Let's see if this fixes things or breaks (original line is commented). New rule should make
        # sure that we are able to reach the other cell by sliding and following the edge.
        if (bottleneck_left_cell is None) or (bottleneck_right_cell is None):
        #if (bottleneck_left_cell is None) != (bottleneck_right_cell is None):
            return True
        if bottleneck_left_cell.has_piece != bottleneck_left_cell.has_piece:
            return True
        if (len(bottleneck_left_cell.get_pieces()) < level or
            len(bottleneck_right_cell.get_pieces()) < level):
            return True
        else:
            return False

    def get_outer_border(self, require_freedom_to_move = False):
        # This can happen only before any piece is placed
        if len(self.get_occupied_cells()) == 0:
            return []
        # Any move except for the very first move of white player
        else:
            # Let's pick cell on the border of island. If we pick the furthest cell with piece from
            # reference cell, this cell then has to be on the outer border of island.
            reference_cell = self.get_occupied_cells()[0]
            connected_cells_dict = self.get_connected_cells_with_distances(reference_cell.coord)
            furthest_distance = 0
            furthest_cell = reference_cell
            for connected_cell in connected_cells_dict:
                if connected_cells_dict[connected_cell] > furthest_distance:
                    furthest_distance = connected_cells_dict[connected_cell]
                    furthest_cell = connected_cell

            # Let's now use furthest_cell, and get its any empty neighbor - this neighbor is then on
            # outer border. We can then use flood fill from this neighbor to detect rest of the cells
            # on the outer border using flood fill with the condition.
            def flood_fill_outer_border(start_coord, visited=None):
                if visited is None:
                    visited = set()
                visited.add(self.get_cell(start_coord))
                for empty_neighbour in self.get_empty_neighbors(start_coord):
                    if len(self.get_occupied_neighbors(empty_neighbour.coord)) > 0 and empty_neighbour not in visited:
                        flood_fill_outer_border(empty_neighbour.coord, visited)
                return visited

            def flood_fill_freedom_to_move_border(start_coord, visited=None):
                if visited is None:
                    visited = set()
                visited.add(self.get_cell(start_coord))
                for empty_neighbour in self.get_empty_neighbors(start_coord):
                    if (len(self.get_occupied_neighbors(empty_neighbour.coord)) > 0 and
                        self.freedom_to_move(start_coord, empty_neighbour.coord) and
                        empty_neighbour not in visited):
                        flood_fill_freedom_to_move_border(empty_neighbour.coord, visited)
                return visited

            # Pick the furthest empty neighbor of furthest cell - this should pick the cell on outer border
            distance = 0
            empty_cell_on_outer_border = self.get_empty_neighbors(furthest_cell.coord)[0]
            for empty_neighbor in self.get_empty_neighbors(furthest_cell.coord):
                if GridCoordinates.distance(empty_neighbor.coord, furthest_cell.coord) > distance:
                    distance = GridCoordinates.distance(empty_neighbor.coord, furthest_cell.coord)
                    empty_cell_on_outer_border = empty_neighbor

            if empty_cell_on_outer_border is None:
                raise KeyError(f"Game reached end of active board - board is too small for this game.")
            if require_freedom_to_move:
                return flood_fill_freedom_to_move_border(empty_cell_on_outer_border.coord)
            else:
                return flood_fill_outer_border(empty_cell_on_outer_border.coord)

    # def get_playable_border(self, coord):
    #     playable_border = self.get_outer_border(require_freedom_to_move=True)
    #     empty_neighbors = self.get_empty_neighbors(coord)
    #     border_reachable = False
    #     # Playable border for piece in bank is outer border with freedom to move rule
    #     if coord is None:
    #         return playable_border
    #     #FIXME This shouldn't be probably here and it should be managed by each piece by doing
    #     # flood fill and checking if they can move to the next cell.
    #     for neighbor in empty_neighbors:
    #         if neighbor in playable_border:
    #             # Remove cells that would end up having no occupied neighbor after moving the piece
    #             if len(self.get_occupied_neighbors(neighbor.coord)) == 1:
    #                 playable_border.remove(neighbor)
    #             # Check that we can reach playable border and not violate freedom to move rule
    #             else:
    #                 if self.freedom_to_move(coord, neighbor.coord):
    #                     border_reachable = True
    #
    #     if border_reachable:
    #         return playable_border
    #     else:
    #         return []

    def has_neighbours_of_same_color(self, coord, piece):
        neighbours = self.get_occupied_neighbors(coord)
        for neighbour in neighbours:
            if neighbour.get_top_piece().color != piece.color:
                return False
        return True

    def get_possible_placements(self, piece):
        # First move
        if self.white_turn and (self.round_counter == 1):
            return [self.get_cell(GridCoordinates(0, 0, 0))]
        # Second move
        elif (not self.white_turn) and (self.round_counter == 1):
            return self.get_neighbors(GridCoordinates(0, 0, 0))
        # Any other move
        else:
            possible_placements = []
            for tested_piece in self.get_piece_bank(piece.color).values():
                for neighbor in self.get_empty_neighbors(tested_piece.coord):
                    if self.has_neighbours_of_same_color(neighbor.coord, tested_piece):
                        if neighbor not in possible_placements:
                            possible_placements.append(neighbor)
            return possible_placements

    def is_placement_legal(self,coord, piece):
        if piece.coord is not None:
            self.logs.warning(f"Piece {piece} is already on the board.")
            return False
        board_cell = self.get_cell(coord)
        if board_cell is None:
            self.logs.error(f"Coordinates {coord} are not on the board.")
            return False
        outer_border = self.get_outer_border()
        #If not first move
        if len(outer_border) !=0:
            if board_cell not in self.get_outer_border():
                self.logs.warning(f"Cannot place {piece} at this position because it would create separate island.")
                return False
        #If cell empty
        if board_cell.has_piece():
            self.logs.warning(f"Piece {piece.type} can be placed only on empty cell. Cell {coord} is occupied")
            return False
        #If cell has no neighbours of other colour
        if (not self.has_neighbours_of_same_color(coord, piece)) and (self.round_counter != 1):
            self.logs.warning(f"Can place piece only at cells that don't touch other player's pieces")
            return False
        #Queen hasn't been placed until round 4
        if ((piece.color == Piece.PieceColour.WHITE) and (piece.type != Piece.PieceType.QUEEN) and
                (not self.white_queen_placed) and (self.round_counter == 4)):
            self.logs.warning(f"Queen has to be placed in first four moves. Place queen.")
            return False
        #TODO Check if it is 3 or 4
        #Queen hasn't been placed until round 4
        if ((piece.color == Piece.PieceColour.BLACK) and (piece.type != Piece.PieceType.QUEEN) and
                (not self.black_queen_placed) and (self.round_counter == 4)):
            self.logs.warning(f"Queen has to be placed in first four moves. Place queen.")
            return False
        if (piece.type == Piece.PieceType.QUEEN) and (self.round_counter == 1):
            self.logs.warning(f"Queen Cannot be placed in the first move.")
            return False
        return True

    # In case make copy of a game object, and we want to be able to retrieve
    # the correct piece and cells in the new game object
    def copy_move_object(self, game_copy, move):
        piece = None
        if move.current_coord is None:
            piece_bank = game_copy.get_piece_bank(move.piece.color)
            selected_piece = None
            for p in piece_bank.values():
                if p.type == move.piece.type and p.coord is None:
                    selected_piece = p
            if selected_piece is None:
                self.logs.debug(f"Copy move: piece {move.piece.type} not in the bank. Enter the move again.")
                return False
            piece = selected_piece
        # Locate piece on the board (don't do checks if it is on top - this is done later)
        else:
            for p in game_copy.get_cell(move.current_coord).get_pieces():
                if p.type == move.piece.type and p.color == move.piece.color:
                    piece = p
        return Move(move.current_coord, move.final_coord, piece)

    def piece_movable(self, piece):
        coord = piece.coord
        piece_cell = self.get_cell(coord)

        # If piece in bank, check if it can be placed somewhere on the board
        if coord is None:
            if len(self.get_possible_placements(piece)) == 0:
                return False
            else:
                return True

        # Check if piece is on top of the cell stack
        if piece_cell.get_top_piece() != piece:
            return False

        #FIXME This is probably not working or is not used
        # Queen cannot be placed during the first move
        if self.round_counter == 1 and piece.type == Piece.PieceType.QUEEN:
            return False

        #TODO Implement the rule that pieces can't move before the queen was placed
        # queen_placed = self.white_queen_placed if self.white_turn else self.black_queen_placed
        # if not queen_placed and self.round_counter<=4:
        #     return False

        # Queen has to be placed between moves 2 - 4
        if piece.type != Piece.PieceType.QUEEN and self.round_counter <= 4:
            if self.white_turn and not self.white_queen_placed:
                self.logs.warning(f"Queen has to be placed until round 4!")
                return False
            if not self.white_turn and not self.black_queen_placed:
                self.logs.warning(f"Queen has to be placed until round 4!")
                return False

        self.get_cell(coord).remove_piece(piece)
        if not self.is_valid_state():
            valid_state = False
        else:
            valid_state = True
        self.get_cell(coord).add_piece(piece)

        return valid_state

    # This is only low level function - to move pieces use make_move()
    def _move_piece(self, move, testing=False):
        current_cell = self.get_cell(move.current_coord)
        new_cell = self.get_cell(move.final_coord)
        #Placing piece on the board
        if (current_cell is None) and (new_cell is not None):
            new_cell.add_piece(move.piece)
            if move.piece.type == Piece.PieceType.QUEEN:
                if move.piece.color == Piece.PieceColour.WHITE:
                    self.white_queen_placed = True
                if move.piece.color == Piece.PieceColour.BLACK:
                    self.black_queen_placed = True
            if not testing:
                self.logs.info(f"Piece {move.piece} is now on the board at {move.final_coord}.")
            return True
        #Making move
        elif (current_cell is not None) and (new_cell is not None):
            current_cell.remove_piece(move.piece)
            new_cell.add_piece(move.piece)
            if not testing:
                self.logs.info(f"Piece {move.piece} moved from {move.current_coord} to {move.final_coord}.")
            return True
        #Moving piece back to bank - this shouldn't be possible in normal game - just for AI to explore the game
        elif (current_cell is not None) and (new_cell is None):
            current_cell.remove_piece(move.piece)
            if move.piece.type == Piece.PieceType.QUEEN:
                if move.piece.color == Piece.PieceColour.WHITE:
                    self.white_queen_placed = False
                if move.piece.color == Piece.PieceColour.BLACK:
                    self.black_queen_placed = False
            return True
        else:
            self.logs.error(f"You are trying to do {move} and that is not possible. Coordinates not on board.")
            return False

    # Only works for moves on the board (not moves from the bank). It is intended for testing moves by
    # individual pieces and for checking of the rules. Not supposed to be used by Player.
    def _move_piece_backwards(self, move):
        move_backwards = Move(move.final_coord, move.current_coord, move.piece)
        return self._move_piece(move_backwards, testing=True)

    def make_move(self, move):
        move_success = self._move_piece(move)
        self.update_stats()
        message = self.check_win()
        if self.check_win():
            self.logs.info(message)
        return move_success

    def list_all_possible_moves(self, player_color):
        if player_color == Piece.PieceColour.BLACK:
            piece_bank = self.piece_bank["black"]
            queen_placed = self.black_queen_placed
        elif player_color == Piece.PieceColour.WHITE:
            piece_bank = self.piece_bank["white"]
            queen_placed = self.white_queen_placed
        else:
            raise ValueError(f"Player has some weird colour - should be BLACK or WHITE")

        moves_list = []
        if not queen_placed:
            if self.round_counter == 1:
                for piece_type, piece in piece_bank.items():
                    if piece_type != "queen":
                        possible_placements = piece.get_possible_moves(self)
                        for placement in possible_placements:
                            moves_list.append(Move(piece.coord, placement.coord, piece))
            elif self.round_counter == 4:
                piece = piece_bank["queen"]
                possible_placements = piece.get_possible_moves(self)
                for placement in possible_placements:
                    moves_list.append(Move(piece.coord, placement.coord, piece))
            else:
                for piece in piece_bank.values():
                    if piece.coord is None:
                        possible_placements = piece.get_possible_moves(self)
                        for placement in possible_placements:
                            moves_list.append(Move(piece.coord, placement.coord, piece))
        else:
            for piece in piece_bank.values():
                possible_placements = None
                if piece.coord is None:
                    if possible_placements is None:
                        possible_placements = piece.get_possible_moves(self)
                    for placement in possible_placements:
                        moves_list.append(Move(piece.coord, placement.coord, piece))
                else:
                    if self.is_piece_on_top(piece):
                        if self.piece_can_be_lifted(piece):
                            possible_placements = piece.get_possible_moves(self)
                            for placement in possible_placements:
                                moves_list.append(Move(piece.coord, placement.coord, piece))
        return moves_list