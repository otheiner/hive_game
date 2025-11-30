from board import Board
import copy

class Game(Board):
    def __init__(self, halfwidth):
        super().__init__(halfwidth)

    @staticmethod
    def print_cells(cells):
        for cell in cells:
            cell.print_cell()

    def get_neighbours(self, cell):
        neighbours = [self.cells[(cell.q + 1, cell.r - 1, cell.s    )],
                      self.cells[(cell.q + 1, cell.r    , cell.s - 1)],
                      self.cells[(cell.q - 1, cell.r + 1, cell.s    )],
                      self.cells[(cell.q - 1, cell.r    , cell.s + 1)],
                      self.cells[(cell.q    , cell.r + 1, cell.s - 1)],
                      self.cells[(cell.q    , cell.r - 1, cell.s + 1)]]
        return neighbours

    def get_occupied_cells(self):
        occupied_cells = []
        for cell in self.cells.values():
            if cell.has_piece():
                occupied_cells.append(cell)
        return occupied_cells

    def get_occupied_neighbours(self, cell):
        board_cell = self.get_cell(cell.q, cell.r, cell.s)
        neighbours = self.get_neighbours(board_cell)
        occupied_neighbours = []
        for neighbour in neighbours:
            if neighbour.has_piece():
                occupied_neighbours.append(neighbour)
        return occupied_neighbours

    def get_empty_neighbours(self, cell):
        board_cell = self.get_cell(cell.q, cell.r, cell.s)
        neighbours = self.get_neighbours(board_cell)
        empty_neighbours = []
        for neighbour in neighbours:
            if not neighbour.has_piece():
                empty_neighbours.append(neighbour)
        return empty_neighbours

    #TODO Maybe problem with different pointers/objects that is being worked with and that is inputted
    def get_connected_cells(self, start_cell, visited=None):
        if visited is None:
            visited = set()
        visited.add(start_cell)
        for neighbour in self.get_occupied_neighbours(start_cell):
            if neighbour not in visited:
                self.get_connected_cells(neighbour, visited)
        return visited

    def is_valid_state(self):
        occupied_cells = self.get_occupied_cells()
        print(occupied_cells)
        if len(occupied_cells) == len(self.get_connected_cells(occupied_cells[0])):
            return True
        else:
            return False

    def get_outer_border(self):
        outer_border = []
        occupied_cells = self.get_occupied_cells()
        for occupied_cell in occupied_cells:
            neighbours = self.get_neighbours(occupied_cell)
            for neighbour in neighbours:
                if not neighbour.has_piece():
                    not_in_outer_border = True
                    for cell in outer_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        outer_border.append(neighbour)
        return outer_border

    def get_playable_border(self, cell):
        playable_border = []
        occupied_cells = self.get_occupied_cells()
        occupied_cells.remove(cell)
        for occupied_cell in occupied_cells:
            neighbours = self.get_neighbours(occupied_cell)
            for neighbour in neighbours:
                if not neighbour.has_piece():
                    not_in_outer_border = True
                    for cell in playable_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        playable_border.append(neighbour)
        return playable_border

    def place_piece(self,cell, piece):
        board_cell = self.cells[(cell.q, cell.r, cell.s)]
        if not board_cell.has_piece():
            board_cell.add_piece(piece)
            return True
        else:
            print(f"Piece {piece.type} can be place only on empty cell. Cell {cell.coordinates()} is occupied")
            return False

    def is_move_legal(self, current_cell, new_cell, piece):
        #Check if the piece is on the top of the cell
        current_board_cell = self.get_cell(current_cell.q, current_cell.r, current_cell.s)
        if current_board_cell.get_top_piece() != piece:
            print(f"Warning: {piece.type} is not at cell {current_board_cell.coordinates()} or "
                  f"is not at the top of the cell.")
            return False

        # Let's now do the test with copy of the game
        game_copy = copy.deepcopy(self)
        current_board_cell = game_copy.get_cell(current_cell.q, current_cell.r, current_cell.s)
        new_board_cell = game_copy.get_cell(new_cell.q, new_cell.r, new_cell.s)
        #Check if the move follows movement rules of the piece
        if not new_board_cell in piece.get_possible_moves(current_cell, game_copy):
            print(f"Warning: {piece.type} at cell {current_cell.coordinates()} cannot move to cell "
                  f"{new_cell.coordinates()}. This would violate movement pattern.")
            return False

        #Check if movement doesn't results in disconnected island
        game_copy.move_piece(current_board_cell, new_board_cell, piece)
        if not game_copy.is_valid_state():
            print(f"Warning: {piece.type} at cell {current_cell.coordinates()} cannot move to cell "
                  f"{new_cell.coordinates()}. This would result in disconnect island.")
            return False

        #By removing the piece completely we check if the island doesn't get disconnected during the move
        #We already moved the piece, so we remove it from new location
        game_copy.remove_piece(new_board_cell, piece)
        if not game_copy.is_valid_state():
            print(f"Warning: {piece.type} at cell {current_cell.coordinates()} cannot move to cell "
                  f"{new_cell.coordinates()}. This would result in disconnect island.")
            return False
        else:
            return True

    def remove_piece(self, cell, piece):
        current_board_cell = self.get_cell(cell.q, cell.r, cell.s)
        if current_board_cell.get_top_piece().type != piece.type:
            print(f"Top piece {current_board_cell.get_top_piece()}, desired piece {piece}.")
            print("Can't remove piece: Cell doesn't contain given piece, or the piece is not on top.")
            return False
        current_board_cell.remove_piece(current_board_cell.get_top_piece())
        return True

    #TODO Make sure that this works with pieces that can move on top of others
    def move_piece(self, current_cell, new_cell, piece):
        current_board_cell = self.get_cell(current_cell.q, current_cell.r, current_cell.s)
        new_board_cell = self.get_cell(new_cell.q, new_cell.r, new_cell.s)
        if current_board_cell.get_top_piece() != piece:
            print(f"Top piece {current_board_cell.get_top_piece()}, desired piece {piece}.")
            print("Invalid move: Cell doesn't contain given piece, or the piece is not on top.")
            return False
        if new_board_cell.get_top_piece() is not None:
            print("Invalid move: Target cell is not empty.")
            return False
        print(f"Moving piece {piece.type} from {current_cell.coordinates()} to {new_cell.coordinates()}.")
        current_board_cell.remove_piece(piece)
        new_board_cell.add_piece(piece)
        return True