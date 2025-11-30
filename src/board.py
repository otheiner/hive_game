import numpy as np
from cell import Cell

# # cell = 0 - out of board
# # cell = 1 - board
# # cell > 1 - piece
# # different pieces should be 10 100 1000 .... to be able to differentiate when they are stacked

class Board:
    #TODO Maybe it is possible to represent board using sparse matrices
    def __init__(self, halfwidth):
        self.halfwidth = halfwidth
        self.board_size = 2 * self.halfwidth + 1
        self.board = np.zeros((self.board_size, self.board_size, self.board_size))
        self.ax = None

        for i in range(self.board_size):
            for j in range(self.board_size):
                for k in range(self.board_size):
                    try:
                        self.array_to_board(i, j, k)
                        self.board[i, j, k] = 1
                    except:
                        pass

    def board_to_array(self, cell):
        if (abs(cell.q)*2+1 > self.board_size or
            abs(cell.r)*2+1 > self.board_size or
            abs(cell.s)*2+1 > self.board_size):
            raise ValueError('Coordinates out of active board!')
        i = self.halfwidth + cell.q
        j = self.halfwidth + cell.r
        k = self.halfwidth + cell.s
        return i, j, k

    def array_to_board(self, i, j ,k):
        if i < 0 or j <0 or k < 0:
            raise ValueError('Array indices has to be positive!')
        if i + 1 >  self.board_size or j + 1 > self.board_size or k + 1 > self.board_size:
            raise ValueError('Array indices out of active board!')
        q = i - self.halfwidth
        r = j - self.halfwidth
        s = k - self.halfwidth
        if q + r + s != 0:
            raise ValueError('Invalid cell: q+r+s!=0')
        cell = Cell(q, r, s)
        return cell

    def get_cell_value(self, cell):
        i, j, k = self.board_to_array(cell)
        return self.board[i, j, k]

    #TODO Check if I can place piece (if it is not occupied - maybe duplicit with move)
    def place_piece(self,cell, piece_value):
        i, j, k = self.board_to_array(cell)
        self.board[i, j, k] += piece_value
        return

    def remove_piece(self,cell, piece_value = 2):
        i, j, k = self.board_to_array(cell)
        self.board[i, j, k] -= piece_value
        return

    #TODO Make sure that this works with pieces that can move on top of others
    def move_piece(self, current_cell, new_cell, piece_value):
        if self.get_cell_value(current_cell) != piece_value + 1:
            print("Invalid move: Cell doesn't contain piece.")
            return False
        if self.get_cell_value(new_cell) != 1:
            print("Invalid move: Target cell is not empty.")
            return False
        i1, j1, k1 = self.board_to_array(current_cell)
        self.board[i1, j1, k1] -= piece_value
        i2, j2, k2 = self.board_to_array(new_cell)
        self.board[i2, j2, k2] += piece_value
        return True