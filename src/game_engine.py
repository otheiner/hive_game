import importlib
import board as board_lib
import piece as piece_lib
from src.cell import GridCoordinates
from src.move import Move

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
        self.white_queen_placed = False
        self.black_queen_placed = False
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

    def get_piece_bank(self, piece_color):
        if piece_color == Piece.PieceColour.BLACK:
            return self.piece_bank_black
        elif piece_color == Piece.PieceColour.WHITE:
            return self.piece_bank_white
        else:
            raise ValueError(f"Piece has some weird colour - should be BLACK or WHITE")

    def get_neighbors(self, coord):
        neighbors = []
        for dq, dr, ds in Board.HEX_DIRECTIONS:
            key = (coord.q + dq, coord.r + dr, coord.s + ds)
            cell = self.cells.get(key)
            if cell is not None:
                neighbors.append(cell)
        return neighbors

    def update_stats(self):
        self.white_turn = not self.white_turn
        if self.white_turn:
            self.round_counter += 1

    def get_occupied_cells(self):
        occupied_cells = []
        for cell in self.cells.values():
            if cell.has_piece():
                #TODO is this the fix?
                occupied_cells.append(cell)
        return occupied_cells

    def get_occupied_neighbours(self, coord):
        neighbours = self.get_neighbors(coord)
        occupied_neighbours = []
        for neighbour in neighbours:
            if neighbour.has_piece():
                occupied_neighbours.append(neighbour)
        return occupied_neighbours

    def get_empty_neighbors(self, coord):
        neighbours = self.get_neighbors(coord)
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
            neighbours = self.get_neighbors(occupied_cell.coord)
            for neighbour in neighbours:
                if not neighbour.has_piece():
                    not_in_outer_border = True
                    for cell in outer_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        outer_border.append(neighbour)
        return outer_border

    #TODO Implement 'freedom to move' rule here
    def get_playable_border(self, coord):
        playable_border = []
        occupied_cells = self.get_occupied_cells()
        if not coord is None:
            occupied_cells.remove(self.get_cell(coord))
        print(f"Occupied cells: {occupied_cells}")
        for occupied_cell in occupied_cells:
            neighbors = self.get_neighbors(occupied_cell.coord)
            print(f"Neighbouring cell: {neighbors}")
            for neighbour in neighbors:
                if not neighbour.has_piece():
                    #FIXME This won't work for hole in the island - check if each cell in  the border has
                    # more than 1 cell connected to it - this should be freedom to move rule
                    not_in_outer_border = True
                    for cell in playable_border:
                        if cell.coord == neighbour.coord:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        playable_border.append(neighbour)

        return playable_border

    def has_neighbours_of_same_color(self, coord, piece):
        neighbours = self.get_occupied_neighbours(coord)
        # This should happen only during the first move
        # if len(neighbours) == 0:
        #     return True
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
            piece_color = piece.color
            playable_border = self.get_playable_border(None)
            for cell in playable_border:
                occupied_neighbours = self.get_occupied_neighbours(cell.coord)
                include_cell = True
                for occupied_neighbour in occupied_neighbours:
                    if occupied_neighbour.get_top_piece().color != piece_color:
                        include_cell = False
                if include_cell:
                    possible_placements.append(cell)
            return possible_placements

    def is_placement_legal(self,coord, piece):
        if piece.coord is not None:
            print(f"Piece {piece} is already on the board.")
            return False
        board_cell = self.get_cell(coord)
        if board_cell is None:
            print(f"Coordinates {coord} are not on the board.")
            return False
        outer_border = self.get_outer_border()
        #If not first move
        if len(outer_border) !=0:
            if board_cell not in self.get_outer_border():
                print(self.get_outer_border())
                print(f"Cannot place {piece} at this position because it would create separate island.")
                return False
        #If cell empty
        if board_cell.has_piece():
            print(f"Piece {piece.type} can be placed only on empty cell. Cell {coord} is occupied")
            return False
        #If cell has no neighbours of other colour
        if (not self.has_neighbours_of_same_color(coord, piece)) and (self.round_counter != 1):
            print(f"Can place piece only at cells that don't touch other player's pieces")
            return False
        #TODO Check if it is 3 or 4
        #Queen hasn't been placed until round 4
        if (piece.color == Piece.PieceColour.WHITE) and (not self.white_queen_placed) and (self.round_counter == 4):
            print(f"Queen has to be placed in first four moves. Place queen.")
            return False
        #TODO Check if it is 3 or 4
        #Queen hasn't been placed until round 4
        if (piece.color == Piece.PieceColour.BLACK) and (not self.black_queen_placed) and (self.round_counter == 4):
            print(f"Queen has to be placed in first four moves. Place queen.")
            return False
        return True

    # In case make copy of a game object, and we want to be able to retrieve
    # the correct piece and cells in the new game object
    @staticmethod
    def copy_move_object(game_copy, move):
        piece = None
        if move.current_coord is None:
            piece_bank = game_copy.get_piece_bank(move.piece.color)
            selected_piece = None
            for p in piece_bank.values():
                if p.type == move.piece.type and p.coord is None:
                    selected_piece = p
            if selected_piece is None:
                print(f"Piece {move.piece.type} not in the bank. Enter the move again.")
                return False
            piece = selected_piece
        # Locate piece on the board (don't do checks if it is on top - this is done later)
        else:
            for p in game_copy.get_cell(move.current_coord).get_pieces():
                if p.type == move.piece.type:
                    piece = p
        return Move(move.current_coord, move.final_coord, piece)

    def is_move_legal(self, move):
        game_copy = copy.deepcopy(self)
        move = self.copy_move_object(game_copy, move)

        #If current coord is none, take piece from the bank and try placing it
        if move.current_coord is None:
            return game_copy.is_placement_legal(move.final_coord, move.piece)
        else:
            #Check if the piece is on the top of the cell
            top_piece = game_copy.get_cell(move.current_coord).get_top_piece()
            current_cell = self.get_cell(move.current_coord)
            if current_cell is None:
                print(f"Coordinates {move.current_coord} are not on the board.")
                return False
            if top_piece != move.piece:
                print(f"Warning: {move.piece.type} is not at cell {current_cell.coord} or "
                      f"is not at the top of the cell.")
                return False

            # Let's now do the test with copy of the game
            new_cell = game_copy.get_cell(move.final_coord)
            if new_cell is None:
                print(f"Coordinates {move.final_coord} are not on the board.")
                return False
            #Check if the move follows movement rules of the piece
            if not new_cell in move.piece.get_possible_moves(game_copy):
                print(f"Warning: {move.piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would violate movement pattern.")
                return False

            #Check if movement doesn't result in disconnected island
            game_copy._move_piece(move)
            if not game_copy.is_valid_state():
                print(f"Warning: {move.piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would result in disconnect island.")
                return False

            #By removing the piece completely we check if the island doesn't get disconnected during the move
            #We already moved the piece, so we remove it from new location
            new_cell.remove_piece(move.piece)
            if not game_copy.is_valid_state():
                print(f"Warning: {move.piece.type} at cell {move.current_coord} cannot move to cell "
                      f"{move.final_coord}. This would result in disconnect island.")
                return False
            else:
                return True

    # This is only low level function - to move pieces use make_move()
    def _move_piece(self, move):
        current_cell = self.get_cell(move.current_coord)
        new_cell = self.get_cell(move.final_coord)
        #Placing piece on the board
        if (current_cell is None) and not (new_cell is None):
            new_cell.add_piece(move.piece)
            self.update_stats()
            print(f"Piece {move.piece} is now on the board at {move.final_coord}.")
            return True
        #Making move
        elif not (current_cell is None) and not (new_cell is None):
            current_cell.remove_piece(move.piece)
            new_cell.add_piece(move.piece)
            self.update_stats()
            return True
        else:
            print(f"You are trying to do {move} and that is not possible. Coordinates not on board.")
            return False

    def make_move(self, move):
        if self.is_move_legal(move):
            return self._move_piece(move)
        else:
            print(f"Cannot make move {move}. Illegal move (or poorly implemented rules haha).")
            return False
