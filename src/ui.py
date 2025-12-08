import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib
import math

import importlib
import cell as cell_lib
import board as board_lib
import piece as piece_lib
import texture as texture_lib
from src.player import Player

#from player import Player, HumanPlayer, Move
importlib.reload(cell_lib)
importlib.reload(piece_lib)
importlib.reload(board_lib)
importlib.reload(texture_lib)
from piece import Piece, Ant, Queen, Spider, Grasshopper, Beetle
from texture import Texture
from cell import Cell, GridCoordinates
from move import Move
from board import Board

class UI:
    def __init__(self, game_state, cell_size = 1,  canvas_size_x = 20, canvas_size_y = 20):
        self.game = game_state
        self.cell_size = cell_size
        self.canvas_size_x = canvas_size_x
        self.canvas_size_y = canvas_size_y
        self.screen_centre_x = self.canvas_size_x / 2
        self.screen_centre_y = self.canvas_size_y / 2

    #This is method that has to be implemented for different UI's
    def draw_cell(self, coord, cell_texture = Texture.TextureType.NO_TEXTURE,
                  show_coords= False, show_border= True):
        raise NotImplementedError

    # This is method that has to be implemented for different UI's
    def draw_piece(self, cx, cy, piece_texture=Texture.TextureType.NO_TEXTURE,
                   show_border=True):
        raise NotImplementedError

    # This is method that has to be implemented for different UI's
    def draw_stats(self):
        raise NotImplementedError

    # This is method that has to be implemented for different UI's
    def draw_piece_banks(self):
        raise NotImplementedError

    def draw_cells(self, cells, cell_texture = Texture.TextureType.NO_TEXTURE, show_grid = False):
        for cell in cells:
            self.draw_cell(cell.coord, cell_texture=cell_texture, show_border = show_grid)
        return

    def draw_board(self, show_coords = False, show_grid = False):
        for cell in self.game.cells.values():
            top_piece = cell.get_top_piece()
            if top_piece is None:
                self.draw_cell(cell.coord, cell_texture=Texture.TextureType.NO_TEXTURE,
                               show_coords=show_coords, show_border = show_grid)
            else:
                self.draw_cell(cell.coord, cell_texture=top_piece.texture,
                               show_coords=show_coords, show_border=True)

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
        matplotlib.use("TkAgg")
        plt.ion()
        self.ax = None

    def _ensure_ax(self):
        """Internal method to create a shared Axes if it doesn't exist."""
        if self.ax is None:
            fig, self.ax = plt.subplots(figsize=(10,10), facecolor='white')
            self.ax.set_xlim(0, self.canvas_size_x)
            self.ax.set_ylim(0, self.canvas_size_y)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
        return self.ax

    def draw_piece(self, cx, cy, piece_texture = Texture.TextureType.NO_TEXTURE,
                   show_border= True):
        ax = self._ensure_ax()

        fill_alpha_bkg = 1
        fill_alpha_circle = 1
        border_color = 'black'
        if show_border:
            border_alpha = 1
        else:
            border_alpha = 0
        white_piece = (1.0, 0.99, 0.82)  # cream colour
        black_piece = 'black'
        if piece_texture == Texture.TextureType.NO_TEXTURE:
            piece_color = 'white'
            fill_color = 'white'
            fill_alpha_bkg = 0
            fill_alpha_circle = 0
        elif piece_texture == Texture.TextureType.HIGHLIGHTED_CELL:
            piece_color = 'white'
            fill_color = 'grey'
            fill_alpha_bkg = 0.2
            fill_alpha_circle = 0
        elif piece_texture == Texture.TextureType.WHITE_QUEEN:
            piece_color = 'yellow'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_SPIDER:
            piece_color = 'brown'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_GRASSHOPPER:
            piece_color = 'green'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_BEETLE:
            piece_color = 'purple'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_ANT:
            piece_color = 'blue'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_LADYBUG:
            piece_color = 'red'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_MOSQUITTO:
            piece_color = 'grey'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.WHITE_PILLBUG:
            piece_color = 'turquoise'
            fill_color = white_piece
        elif piece_texture == Texture.TextureType.BLACK_QUEEN:
            piece_color = 'yellow'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_SPIDER:
            piece_color = 'brown'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_GRASSHOPPER:
            piece_color = 'green'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_BEETLE:
            piece_color = 'purple'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_ANT:
            piece_color = 'blue'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_LADYBUG:
            piece_color = 'red'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_MOSQUITTO:
            piece_color = 'grey'
            fill_color = black_piece
        elif piece_texture == Texture.TextureType.BLACK_PILLBUG:
            piece_color = 'turquoise'
            fill_color = black_piece
        else:
            print(f"Warning: {piece_texture} is unknown, or not implemented in this GUI. "
                  f"Setting turquoise.")
            fill_color = 'turquoise'
            piece_color = 'turquoise'

        rgba_fill = mcolors.to_rgba(fill_color, fill_alpha_bkg)
        rgba_border = mcolors.to_rgba(border_color, border_alpha)
        hexagon = patches.Polygon(self.cell_corners(self.screen_centre_x + cx, self.screen_centre_y + cy),
                                  closed=True, edgecolor=rgba_border, facecolor=rgba_fill)
        ax.add_patch(hexagon)
        rgba_fill = mcolors.to_rgba(piece_color, fill_alpha_circle)
        circle = patches.Circle((self.screen_centre_x + cx, self.screen_centre_y + cy),
                                radius=self.cell_size / 3, facecolor=rgba_fill)
        ax.add_patch(circle)
        self.ax.figure.canvas.draw_idle()
        return ax

    def draw_cell(self, coord, cell_texture = Texture.TextureType.NO_TEXTURE,
                  show_coords= False, show_border= True):
        cx = self.cube_to_cartesian(coord.q, coord.r, coord.s)[0]
        cy = self.cube_to_cartesian(coord.q, coord.r, coord.s)[1]
        self.draw_piece(cx, cy, cell_texture, show_border=show_border)

        ax = self._ensure_ax()
        centre_x = self.canvas_size_x / 2
        centre_y = self.canvas_size_x / 2

        if show_coords:
            ax.text(self.screen_centre_x + cx - self.cell_size*0.7,
                    self.screen_centre_y + cy,f"{coord.q, coord.r}",
                    fontsize=8, color='red')
        return ax

    def draw_stats(self):
        ax = self._ensure_ax()
        if self.game.white_turn:
            text_turn = 'White Turn'
        else:
            text_turn = 'Black Turn'
        text_round_no = self.game.round_counter
        ax.text(0.4*self.canvas_size_x, 0.93*self.canvas_size_y,
                f"{text_turn}\nRound: {text_round_no}", fontsize=12, color='black')

    def draw_piece_banks(self):
        indent_x = 0.45
        indent_y = - 0.48
        piece_separation = self.cell_size*1.2
        bottom_y = self.canvas_size_x  * indent_y
        black_x = -1* self.canvas_size_x  * indent_x
        white_x =  self.canvas_size_x *   indent_x

        #Draw white bank
        piece_no = 0
        for piece in self.game.piece_bank_white.values():
            piece_no += 1
            if piece.coord is None:
                self.draw_piece(white_x, bottom_y + piece_no*(self.cell_size + piece_separation),
                                piece.texture)

        #Draw black bank
        piece_no = 0
        for piece in self.game.piece_bank_black.values():
            piece_no += 1
            if piece.coord is None:
                self.draw_piece(black_x, bottom_y + piece_no*(self.cell_size + piece_separation),
                                piece.texture)

    def draw_board(self, show_coords = False, show_grid = False):
        self.clear_canvas()
        for cell in self.game.cells.values():
            top_piece = cell.get_top_piece()
            if top_piece is None:
                self.draw_cell(cell.coord, cell_texture=Texture.TextureType.NO_TEXTURE,
                               show_coords=show_coords, show_border = show_grid)
            else:
                self.draw_cell(cell.coord, cell_texture=top_piece.texture,
                               show_coords=show_coords, show_border=True)

    def show_canvas(self):
        if self.ax is None:
            self._ensure_ax()
        plt.draw()
        plt.pause(0.1)
        return

    def clear_canvas(self):
        if self.ax is None:
            return
        self._ensure_ax().clear()
        self.ax.set_xlim(0, self.canvas_size_x)
        self.ax.set_ylim(0, self.canvas_size_y)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        return

    # TODO This should maybe only process input but shouldn't do the logis about occupied cells,...
    # TODO Think about idea above because the same checks will have to be done for mouse input
    # TODO just type of input will be different but logic will be the same.
    def wait_for_user_input(self, player_color):
        print(f"----- Player {player_color}, round {self.game.round_counter} -----")

        if player_color == Player.PlayerColor.WHITE:
            piece_bank = self.game.piece_bank_white
        elif player_color == Player.PlayerColor.BLACK:
            piece_bank = self.game.piece_bank_black
        else:
            raise ValueError(f"Invalid player color: {player_color}")
        print(f" piece bank: {piece_bank}")

        # Enter piece and coordinates to be able to see possible placements
        piece_name = input("Enter name of piece \n(or 'quit' to end game): ")
        if piece_name == 'quit':
            return None
        start_move = input("Enter q r (s) of start \n(or 'quit' to end game): ")
        if start_move == 'quit':
            return None

        # Process start coordinates input
        # Check if we are picking piece from board or from bank
        if start_move.strip() == "bank":
            start_coord = None
        else:
            entered_start_coord = []
            for coord in start_move.split(" "):
                coord = coord.strip()
                if coord.lstrip("+-").isdigit():
                    entered_start_coord.append(int(coord))
                else:
                    print(f"Invalid starting coordinates. Enter the move again again.")
                    return self.wait_for_user_input(player_color)
            if len(entered_start_coord) == 2:
                start_coord = GridCoordinates(entered_start_coord[0], entered_start_coord[1])
            else:
                print(f"Staring coordinates need to have two components")
                return self.wait_for_user_input(player_color)

        # Process piece input
        # Check if piece is on given coordinates on top of the piece stack
        if start_coord is not None:
            top_piece = self.game.cells[(start_coord.q, start_coord.r, start_coord.s)].get_top_piece()
            if top_piece is not None:
                if (top_piece.type == piece_name) and (top_piece.color == player_color):
                    # TODO I think there is problem with pointers
                    selected_piece = top_piece
                else:
                    print(f"Piece {piece_name} is not at starting coordinates. Enter move again.")
                    return self.wait_for_user_input(player_color)
            else:
                print("There is no piece on given coordinates. Enter move again.")
                return self.wait_for_user_input(player_color)
        # If piece is not on board check if it is in piece bank
        else:
            selected_piece = None
            for piece in piece_bank.values():
                if piece.type == piece_name and piece.coord is None:
                    selected_piece = piece
            if selected_piece is None:
                print(f"Piece {piece_name} not in the bank. Enter the move again.")
                return self.wait_for_user_input(player_color)

        # Highlight possible moves before picking where to go
        highlighted_cells = selected_piece.get_possible_moves(self.game)
        print(f"Highlighted cells: {highlighted_cells}")
        print(f"Cel (1 0): {self.game.get_cell(GridCoordinates(1, 0))}")
        self.draw_board(show_grid=True, show_coords=True)
        self.draw_cells(highlighted_cells, cell_texture = Texture.TextureType.HIGHLIGHTED_CELL)
        self.draw_stats()
        self.draw_piece_banks()
        self.show_canvas()

        # Process end coordinates input
        end_move = input("Enter q r (s) of end \n(or 'a' to abandon this piece, or 'quit' to end game): ")
        if end_move == 'quit':
            return None
        if end_move == 'a':
            # Show board but don't highlight any cells
            self.draw_board(show_grid=True, show_coords=True)
            self.draw_stats()
            self.draw_piece_banks()
            self.show_canvas()
        entered_end_coord = []
        for coord in end_move.split(" "):
            coord = coord.strip()
            if coord.lstrip("+-").isdigit():
                entered_end_coord.append(int(coord))
            else:
                print(f"Invalid destination coordinates. Enter the move again.")
                return self.wait_for_user_input(player_color)
        if len(entered_end_coord) == 2:
            end_coord = GridCoordinates(entered_end_coord[0], entered_end_coord[1])
        else:
            print(f"Destination coordinates need to have two components")
            return self.wait_for_user_input(player_color)

        return Move(start_coord, end_coord, selected_piece)