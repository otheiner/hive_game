from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import math

import importlib
import cell as cell_lib
import board as board_lib
import piece as piece_lib
importlib.reload(cell_lib)
importlib.reload(piece_lib)
importlib.reload(board_lib)
from piece import Piece, Ant
from cell import Cell
from board import Board

class GUI:
    def __init__(self, game_state, cell_size = 1,  canvas_size = 20):
        self.game = game_state
        self.cell_size = cell_size
        self.canvas_size = canvas_size
        self.ax = None

    def _ensure_ax(self):
        """Internal method to create a shared Axes if it doesn't exist."""
        if self.ax is None:
            fig, self.ax = plt.subplots(figsize=(15,15), facecolor='white')
            self.ax.set_xlim(0, self.canvas_size)
            self.ax.set_ylim(0, self.canvas_size)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
        return self.ax

    def cell_corners(self, cx, cy):
        corners = []
        for i in range(6):
            angle = math.radians(60 * i - 30)  # pointy-top
            x = cx + self.cell_size * math.cos(angle)
            y = cy + self.cell_size * math.sin(angle)
            corners.append((x, y))
        return corners

    @staticmethod
    def cube_to_axial(q, r, s):
        return q, r

    @staticmethod
    def axial_to_cube(q, r):
        s = -q - r
        return q, r, s

    def cube_to_cartesian(self, q, r, s):
        x = (math.sqrt(3) * self.cell_size * self.cube_to_axial(q, r, s)[0] +
             math.sqrt(3) / 2 * self.cell_size * self.cube_to_axial(q, r, s)[1])
        y = 3 / 2 * self.cell_size * self.cube_to_axial(q, r, s)[1]
        return x, y

    def draw_cell(self, cell, show=False, border_color='black',
                  fill_color='white', fill_alpha=1):
        ax = self._ensure_ax()
        cx = self.cube_to_cartesian(cell.q, cell.r, cell.s)[0]
        cy = self.cube_to_cartesian(cell.q, cell.r, cell.s)[1]
        centre = self.canvas_size / 2
        rgba_fill = mcolors.to_rgba(fill_color, fill_alpha)
        hexagon = Polygon(self.cell_corners(centre + cx, centre + cy),
                          closed=True, edgecolor=border_color, facecolor=rgba_fill)
        ax.add_patch(hexagon)
        if show:
            plt.show()
            return 0
        else:
            return ax

    def draw_cells(self, cells, show=False, border_color='black', fill_color='white', fill_alpha=1):
        for cell in cells:
            self.draw_cell(cell, show=show, border_color=border_color,
                           fill_color=fill_color, fill_alpha=fill_alpha)
        return

    def draw_board(self):
        for cell in self.game.cells.values():
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

    def draw_outer_border(self):
        outer_border = self.game.get_outer_border()
        self.draw_cells(outer_border, fill_color='grey', fill_alpha=0.7)

    def show_canvas(self):
        if self.ax is None:
            self._ensure_ax()
        plt.show()

    def place_piece(self,cell, piece_type):
        return self.game.place_piece(cell, piece_type)

    def move_piece(self,current_cell, new_cell, piece):
        return self.game.move_piece(current_cell, new_cell, piece)