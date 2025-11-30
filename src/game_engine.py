import importlib
import cell
import board
import piece
importlib.reload(cell)
importlib.reload(piece)
importlib.reload(board)
from piece import Piece, Ant
from cell import Cell
from board import Board

import math
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

class Game(Board):
    def __init__(self, halfwidth, cell_size = 1,  canvas_size = 20):
        super().__init__(halfwidth)
        self.cell_size = cell_size      #TODO to UI
        self.canvas_size = canvas_size  #TODO to UI

    # TODO to UI
    def _ensure_ax(self):
        """Internal method to create a shared Axes if it doesn't exist."""
        if self.ax is None:
            fig, self.ax = plt.subplots(figsize=(15,15), facecolor='white')
            self.ax.set_xlim(0, self.canvas_size)
            self.ax.set_ylim(0, self.canvas_size)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
        return self.ax

    # TODO to UI
    def cell_corners(self, cx, cy):
        corners = []
        for i in range(6):
            angle = math.radians(60 * i - 30)  # pointy-top
            x = cx + self.cell_size * math.cos(angle)
            y = cy + self.cell_size * math.sin(angle)
            corners.append((x, y))
        return corners

    # TODO to UI
    @staticmethod
    def cube_to_axial(q, r, s):
        return q, r

    # TODO to UI
    @staticmethod
    def axial_to_cube(q, r):
        s = -q - r
        return q, r, s

    @staticmethod
    def print_cells(cells):
        for cell in cells:
            cell.print_cell()

    # TODO to UI
    def cube_to_cartesian(self, q, r ,s):
        x = (math.sqrt(3) * self.cell_size * self.cube_to_axial(q, r, s)[0] +
             math.sqrt(3)/2 * self.cell_size * self.cube_to_axial(q, r, s)[1])
        y = 3/2 * self.cell_size * self.cube_to_axial(q, r, s)[1]
        return x, y

    #TODO to UI
    def draw_cell(self, cell, show = False, border_color='black',
                  fill_color='white', fill_alpha=1):
        ax = self._ensure_ax()
        cx = self.cube_to_cartesian(cell.q, cell.r, cell.s)[0]
        cy = self.cube_to_cartesian(cell.q, cell.r, cell.s)[1]
        centre = self.canvas_size/2
        rgba_fill = mcolors.to_rgba(fill_color, fill_alpha)
        hexagon = Polygon(self.cell_corners(centre  + cx, centre + cy),
                          closed=True, edgecolor=border_color, facecolor=rgba_fill)
        ax.add_patch(hexagon)
        if show:
            plt.show()
            return 0
        else:
            return ax

    # TODO to UI
    def draw_cells(self,cells, show = False, border_color='black', fill_color='white', fill_alpha=1):
        for cell in cells:
            self.draw_cell(cell,show = show, border_color = border_color,
                           fill_color = fill_color,fill_alpha = fill_alpha)
        return

    # TODO to UI
    def draw_board(self):
        for cell in self.cells.values():
            top_piece = cell.get_top_piece()
            if top_piece is None:
                self.draw_cell(cell, fill_color='white', fill_alpha=0)
            else:
                if top_piece.type == Piece.PieceType.ANT:
                    self.draw_cell(cell, fill_color='blue')
                if top_piece.type == Piece.PieceType.QUEEN:
                    self.draw_cell(cell, fill_color='yellow')
                if top_piece.type == Piece.PieceType.SPIDER:
                    self.draw_cell(cell, fill_color='brown')
                if top_piece.type == Piece.PieceType.GRASSHOPPER:
                    self.draw_cell(cell, fill_color='green')
                if top_piece.type == Piece.PieceType.BEETLE:
                    self.draw_cell(cell, fill_color='purple')

    # TODO to UI
    def show_canvas(self):
        if self.ax is None:
            self._ensure_ax()
        plt.show()

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

    #TODO MAybe problem with different pointers/objects that is being worked with and that is inputted
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

    #TODO Check if I can place piece (if it is not occupied - maybe duplicit
    #     with move(?))
    def place_piece(self,cell, piece_type):
        board_cell = self.cells[(cell.q, cell.r, cell.s)]
        board_cell.add_piece(piece_type)
        #(self.cells[(cell.q, cell.r, cell.s)].get_top_piece().type)
        return

    #TODO implement using copy
    # def is_move_legal(self, current_cell, new_cell, piece):
    #     return


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

    # #TODO Fix logic in this function - it is probably almost correct. Redo this using copy, but I first need to separate UI
    # def piece_movable(self, cell, piece):
    #     board_cell = self.get_cell(cell.q, cell.r, cell.s)
    #
    #     if board_cell.get_top_piece() != piece:
    #         raise Exception("Invalid move: Cell doesn't contain given piece "
    #                         "or the piece is not on top.")
    #
    #     occupied_cells = self.get_occupied_cells()
    #     #occupied_cells_wo_piece = [c for c in occupied_cells
    #     #                 if not (c.q == cell_to_remove.q and c.r == cell_to_remove.r and c.s == cell_to_remove.s)]
    #     occupied_cells_wo_piece = []
    #     for occupied_cell in occupied_cells:
    #         if occupied_cell != board_cell:
    #             occupied_cells_wo_piece.append(occupied_cell)
    #     self.print_cells(occupied_cells_wo_piece)
    #
    #     # If no occupied cells remain, continuity is trivially preserved
    #     if not occupied_cells_wo_piece:
    #         return True
    #
    #     connected = self.get_connected_cells(occupied_cells_wo_piece[0])
    #     print("connected cells")
    #     self.print_cells(connected)
    #     if len(occupied_cells_wo_piece) == len(connected):
    #         return True
    #     else:
    #         return False