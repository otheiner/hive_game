import numpy as np
from cell import Cell
from piece import Piece

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
        self.cells = {}  # key = (q,r,s), value = Cell

        for i in range(self.board_size):
            for j in range(self.board_size):
                for k in range(self.board_size):
                    try:
                        q, r, s = self.array_to_board(i, j, k)
                        self.cells[(q, r, s)] = Cell(q, r, s)
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
        return q, r, s

    def get_cell(self, q, r, s):
        try:
            return self.cells[(q, r, s)]
        except KeyError:
            raise ValueError('Cell is not on the board: q={}, r={}, s={}'.format(q, r, s))