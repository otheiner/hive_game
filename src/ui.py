import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import math

import importlib
import cell as cell_lib
import board as board_lib
import piece as piece_lib
import texture as texture_lib
importlib.reload(cell_lib)
importlib.reload(piece_lib)
importlib.reload(board_lib)
importlib.reload(texture_lib)
from piece import Piece, Ant, Queen, Spider, Grasshopper, Beetle
from texture import Texture
from cell import Cell, GridCoordinates
from board import Board

class UI:
    def __init__(self, game_state, cell_size = 1,  canvas_size_x = 20, canvas_size_y = 20):
        self.game = game_state
        self.cell_size = cell_size
        self.canvas_size_x = canvas_size_x
        self.canvas_size_y = canvas_size_y

    #This is method that has to be implemented for different UI's
    def draw_cell(self, coord, cell_texture = Texture.TextureType.NO_TEXTURE):
        raise NotImplementedError

    # This is method that has to be implemented for different UI's
    def draw_stats(self):
        raise NotImplementedError

    def draw_cells(self, cells, cell_texture = Texture.TextureType.NO_TEXTURE):
        for cell in cells:
            self.draw_cell(cell.coord, cell_texture=cell_texture)
        return

    def draw_board(self):
        for cell in self.game.cells.values():
            top_piece = cell.get_top_piece()
            if top_piece is None:
                self.draw_cell(cell.coord, cell_texture=Texture.TextureType.NO_TEXTURE)
            else:
                self.draw_cell(cell.coord, cell_texture=top_piece.texture)

    def draw_outer_border(self):
        outer_border = self.game.get_outer_border()
        self.draw_cells(outer_border, cell_texture=Texture.TextureType.HIGHLIGHTED_CELL)

    def place_piece(self,cell, piece_type):
        return self.game.place_piece(cell, piece_type)

    def move_piece(self,current_cell, new_cell, piece):
        return self.game.move_piece(current_cell, new_cell, piece)

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


#To display what is drawn, show_canvas() has to be called in this class
class MatplotlibGUI(UI):
    def __init__(self, game_state, cell_size = 1,  canvas_size_x = 20, canvas_size_y = 20):
        super().__init__(game_state, cell_size, canvas_size_x, canvas_size_y)
        self.ax = None

    def _ensure_ax(self):
        """Internal method to create a shared Axes if it doesn't exist."""
        if self.ax is None:
            fig, self.ax = plt.subplots(figsize=(15,15), facecolor='white')
            self.ax.set_xlim(0, self.canvas_size_x)
            self.ax.set_ylim(0, self.canvas_size_y)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
        return self.ax

    def draw_cell(self, coord, cell_texture = Texture.TextureType.NO_TEXTURE):
        ax = self._ensure_ax()
        cx = self.cube_to_cartesian(coord.q, coord.r, coord.s)[0]
        cy = self.cube_to_cartesian(coord.q, coord.r, coord.s)[1]
        centre_x = self.canvas_size_x / 2
        centre_y = self.canvas_size_x / 2

        fill_alpha_bkg = 1
        fill_alpha_circle = 1
        border_color = 'black'
        white_piece = (1.0, 0.99, 0.82) #cream colour
        black_piece = 'black'
        if cell_texture == Texture.TextureType.NO_TEXTURE:
            piece_color = 'white'
            fill_color = 'white'
            fill_alpha_bkg = 0
            fill_alpha_circle = 0
        elif cell_texture == Texture.TextureType.HIGHLIGHTED_CELL:
            piece_color = 'white'
            fill_color = 'grey'
            fill_alpha_bkg = 0.7
            fill_alpha_circle = 0
        elif cell_texture == Texture.TextureType.WHITE_QUEEN:
            piece_color = 'yellow'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_SPIDER:
            piece_color = 'brown'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_GRASSHOPPER:
            piece_color = 'green'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_BEETLE:
            piece_color = 'purple'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_ANT:
            piece_color = 'blue'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_LADYBUG:
            piece_color = 'red'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.WHITE_MOSQUITTO:
            piece_color = 'grey'
            fill_color = white_piece
        elif cell_texture == Texture.TextureType.BLACK_QUEEN:
            piece_color = 'yellow'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_SPIDER:
            piece_color = 'brown'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_GRASSHOPPER:
            piece_color = 'green'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_BEETLE:
            piece_color = 'purple'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_ANT:
            piece_color = 'blue'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_LADYBUG:
            piece_color = 'red'
            fill_color = black_piece
        elif cell_texture == Texture.TextureType.BLACK_MOSQUITTO:
            piece_color = 'grey'
            fill_color = black_piece
        else:
            print(f"Warning: {cell_texture} is unknown, or not implemented in this GUI. "
                  f"Setting turquoise.")
            fill_color = 'turquoise'
            piece_color = 'turquoise'

        rgba_fill = mcolors.to_rgba(fill_color, fill_alpha_bkg)
        hexagon = patches.Polygon(self.cell_corners(centre_x + cx, centre_y + cy),
                          closed=True, edgecolor=border_color, facecolor=rgba_fill)
        ax.add_patch(hexagon)
        rgba_fill = mcolors.to_rgba(piece_color, fill_alpha_circle)
        circle = patches.Circle((centre_x + cx, centre_y + cy), radius=self.cell_size/3,
                                facecolor=rgba_fill)
        ax.add_patch(circle)
        return ax

    def draw_stats(self):
        ax = self._ensure_ax()
        if self.game.white_turn:
            text_turn = 'White Turn'
        else:
            text_turn = 'Black Turn'
        text_round_no = self.game.round_counter
        ax.text(0.8*self.canvas_size_x, 0.93*self.canvas_size_y,
                f"{text_turn}\nRound: {text_round_no}", fontsize=20, color='black')

    def show_canvas(self):
        if self.ax is None:
            self._ensure_ax()
        plt.show()