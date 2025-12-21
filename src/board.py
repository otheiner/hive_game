import numpy as np
from src.cell import Cell, GridCoordinates

class Board:
    # They are ordered in mathematically positive sense - starting on "x-axis"
    HEX_DIRECTIONS = [
        (+1, 0, -1),
        (0, +1, -1),
        (-1, +1, 0),
        (-1, 0, +1),
        (0, -1, +1),
        (+1, -1, 0)]

    def __init__(self, halfwidth):
        self.halfwidth = halfwidth
        self.board_size = 2 * self.halfwidth + 1
        #Make sure that I really don't miss the array
        #self.board = np.zeros((self.board_size, self.board_size, self.board_size))
        self.cells = {}  # key = (q,r,s), value = Cell

        for i in range(self.board_size):
            for j in range(self.board_size):
                for k in range(self.board_size):
                    try:
                        coord = self.array_to_coord(i, j, k)
                        self.cells[(coord.q, coord.r, coord.s)] = Cell(coord)
                    except:
                        pass

    def coord_to_array(self, coord):
        if (abs(coord.q)*2+1 > self.board_size or
            abs(coord.r)*2+1 > self.board_size or
            abs(coord.s)*2+1 > self.board_size):
            raise ValueError('Coordinates out of active board!')
        i = self.halfwidth + coord.q
        j = self.halfwidth + coord.r
        k = self.halfwidth + coord.s
        return i, j, k

    def array_to_coord(self, i, j ,k):
        if i < 0 or j <0 or k < 0:
            raise ValueError('Array indices has to be positive!')
        if i + 1 >  self.board_size or j + 1 > self.board_size or k + 1 > self.board_size:
            raise ValueError('Array indices out of active board!')
        q = i - self.halfwidth
        r = j - self.halfwidth
        s = k - self.halfwidth
        coord = GridCoordinates(q, r, s)
        return coord

    def get_cell(self, coord):
        if coord is None:
            return None
        else:
            cell = self.cells.get((coord.q, coord.r, coord.s))
            if cell is None:
                print(f"Coordinates {coord} are not on the board.")
            return cell