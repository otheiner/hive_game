import importlib
import board as board_lib
import piece as piece_lib
importlib.reload(board_lib)
importlib.reload(piece_lib)
from board import Board
from piece import Piece, Ant, Queen, Spider, Grasshopper, Beetle, Mosquito, Ladybug
import copy

class Game(Board):
    def __init__(self, halfwidth):
        super().__init__(halfwidth)
        self.winning_state = False
        #TODO Write checking for winning state
        self.white_turn = True
        self.round_counter = 1
        self.piece_bank_white = {"queen" : Queen(Piece.PieceColour.WHITE),
                                 "spider1" : Spider(Piece.PieceColour.WHITE),
                                 "spider2": Spider(Piece.PieceColour.WHITE),
                                 "beetle1" : Beetle(Piece.PieceColour.WHITE),
                                 "beetle2" : Beetle(Piece.PieceColour.WHITE),
                                 "grasshopper1" : Grasshopper(Piece.PieceColour.WHITE),
                                 "grasshopper2" : Grasshopper(Piece.PieceColour.WHITE),
                                 "grasshopper3" : Grasshopper(Piece.PieceColour.WHITE),
                                 "ant1" : Ant(Piece.PieceColour.WHITE),
                                 "ant2" : Ant(Piece.PieceColour.WHITE),
                                 "ant3" : Ant(Piece.PieceColour.WHITE),
                                 "mosquito" : Mosquito(Piece.PieceColour.WHITE),
                                 "ladybug" : Ladybug(Piece.PieceColour.WHITE)}
        self.piece_bank_black = {"queen" :Queen(Piece.PieceColour.BLACK),
                                 "spider1" :Spider(Piece.PieceColour.BLACK),
                                 "spider2" :Spider(Piece.PieceColour.BLACK),
                                 "beetle1" : Beetle(Piece.PieceColour.BLACK),
                                 "beetle2" : Beetle(Piece.PieceColour.BLACK),
                                 "grasshopper1" : Grasshopper(Piece.PieceColour.BLACK),
                                 "grasshopper2" : Grasshopper(Piece.PieceColour.BLACK),
                                 "grasshopper3" : Grasshopper(Piece.PieceColour.BLACK),
                                 "ant1" : Ant(Piece.PieceColour.BLACK),
                                 "ant2" : Ant(Piece.PieceColour.BLACK),
                                 "ant3" : Ant(Piece.PieceColour.BLACK),
                                 "mosquito" : Mosquito(Piece.PieceColour.BLACK),
                                 "ladybug" : Ladybug(Piece.PieceColour.BLACK)}

    @staticmethod
    def print_cells(cells):
        for cell in cells:
            cell.print_cell()

    def get_neighbours(self, coord):
        neighbours = [self.cells[(coord.q + 1, coord.r - 1, coord.s    )],
                      self.cells[(coord.q + 1, coord.r    , coord.s - 1)],
                      self.cells[(coord.q - 1, coord.r + 1, coord.s    )],
                      self.cells[(coord.q - 1, coord.r    , coord.s + 1)],
                      self.cells[(coord.q    , coord.r + 1, coord.s - 1)],
                      self.cells[(coord.q    , coord.r - 1, coord.s + 1)]]
        return neighbours

    def update_stats(self):
        self.white_turn = not self.white_turn
        if self.white_turn:
            self.round_counter += 1

    def get_occupied_cells(self):
        occupied_cells = []
        for cell in self.cells.values():
            if cell.has_piece():
                occupied_cells.append(cell)
        return occupied_cells

    def get_occupied_neighbours(self, coord):
        neighbours = self.get_neighbours(coord)
        occupied_neighbours = []
        for neighbour in neighbours:
            if neighbour.has_piece():
                occupied_neighbours.append(neighbour)
        return occupied_neighbours

    def get_empty_neighbours(self, coord):
        neighbours = self.get_neighbours(coord)
        empty_neighbours = []
        for neighbour in neighbours:
            if not neighbour.has_piece():
                empty_neighbours.append(neighbour)
        return empty_neighbours

    #TODO Maybe problem with different pointers/objects that is being worked with and that is inputted
    def get_connected_cells(self, start_coord, visited=None):
        if visited is None:
            visited = set()
        visited.add(self.get_cell(start_coord))
        for neighbour in self.get_occupied_neighbours(start_coord):
            if neighbour not in visited:
                self.get_connected_cells(neighbour.coord, visited)
        return visited

    def is_valid_state(self):
        occupied_cells = self.get_occupied_cells()
        #print(occupied_cells)
        if len(occupied_cells) == len(self.get_connected_cells(occupied_cells[0].coord)):
            return True
        else:
            return False

    def get_outer_border(self):
        outer_border = []
        occupied_cells = self.get_occupied_cells()
        for occupied_cell in occupied_cells:
            neighbours = self.get_neighbours(occupied_cell.coord)
            for neighbour in neighbours:
                if not neighbour.has_piece():
                    not_in_outer_border = True
                    for cell in outer_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        outer_border.append(neighbour)
        return outer_border

    def get_playable_border(self, coord):
        playable_border = []
        occupied_cells = self.get_occupied_cells()
        occupied_cells.remove(self.get_cell(coord))
        for occupied_cell in occupied_cells:
            neighbours = self.get_neighbours(occupied_cell.coord)
            for neighbour in neighbours:
                if not neighbour.has_piece():
                    not_in_outer_border = True
                    for cell in playable_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        playable_border.append(neighbour)
        return playable_border

    def place_piece(self,coord, piece):
        if piece.coord is not None:
            print(f"Piece {piece} is already on the board.")
            return False
        board_cell = self.cells[(coord.q, coord.r, coord.s)]
        outer_border = self.get_outer_border()
        #If not first move
        if len(outer_border) !=0:
            if board_cell not in self.get_outer_border():
                print(f"Cannot place {piece} at this position because it would create separate island.")
                return False
        if not board_cell.has_piece():
            board_cell.add_piece(piece)
            piece.coord = board_cell.coord
            self.update_stats()
            print(f"Piece {piece} is now on the board at {coord}.")
            return True
        else:
            print(f"Piece {piece.type} can be place only on empty cell. Cell {coord} is occupied")
            return False

    def is_move_legal(self, move):
        #TODO Implement validation of initial piece placement and beginning of the game
        move = copy.deepcopy(move)
        game_copy = copy.deepcopy(self)
        if move.current_coord is None:
            # Let's now do the test with copy of the game
            return game_copy.place_piece(move.final_coord, move.piece)
        else:
            #Check if the piece is on the top of the cell
            piece = move.piece
            current_cell = self.get_cell(move.current_coord)
            if current_cell.get_top_piece() != piece:
                print(f"Warning: {piece.type} is not at cell {current_cell.coord} or "
                      f"is not at the top of the cell.")
                return False

            # Let's now do the test with copy of the game
            new_cell = game_copy.get_cell(move.final_coord)
            #Check if the move follows movement rules of the piece
            if not new_cell in piece.get_possible_moves(move.current_coord, game_copy):
                print(f"Warning: {piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would violate movement pattern.")
                return False

            #Check if movement doesn't result in disconnected island
            game_copy.move_piece(move.current_coord, move.final_coord, piece)
            if not game_copy.is_valid_state():
                print(f"Warning: {piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would result in disconnect island.")
                return False

            #By removing the piece completely we check if the island doesn't get disconnected during the move
            #We already moved the piece, so we remove it from new location
            game_copy.remove_piece(move.final_coord, piece)
            if not game_copy.is_valid_state():
                print(f"Warning: {piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would result in disconnect island.")
                return False
            else:
                return True

    def remove_piece(self, coord, piece):
        current_board_cell = self.get_cell(coord)
        if current_board_cell.get_top_piece().type != piece.type:
            print(f"Top piece {current_board_cell.get_top_piece()}, desired piece {piece}.")
            print("Can't remove piece: Cell doesn't contain given piece, or the piece is not on top.")
            return False
        current_board_cell.remove_piece(current_board_cell.get_top_piece())
        piece.coord = None
        return True

    #TODO Make sure that this works with pieces that can move on top of others
    def move_piece(self, current_coord, new_coord, piece):
        #TODO Check that the move is legal
        current_cell = self.get_cell(current_coord)
        new_cell = self.get_cell(new_coord)
        if current_cell.get_top_piece() != piece:
            print(f"ERROR: Can't move. Top piece is {current_cell.get_top_piece()}, desired piece is {piece}.")
            return False
        if new_cell.get_top_piece() is not None:
            print("ERROR: Invalid move. Target cell is not empty.")
            return False
        print(f"Moving {piece} from {current_coord} to {new_coord}.")
        current_cell.remove_piece(piece)
        new_cell.add_piece(piece)
        piece.coord = new_cell.coord
        self.update_stats()
        return True

    def make_move(self, move):
        start_position = move.current_coord
        end_position = move.final_coord
        piece = move.piece

        #TODO This might be written better, I think
        if self.is_move_legal(move):
            if move.current_coord is None:
                return self.place_piece(end_position, piece)
            else:
                return self.move_piece(start_position, end_position, piece)
        else:
            print(f"Cannot make move {move}.")
            return False
