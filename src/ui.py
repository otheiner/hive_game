import time
from itertools import dropwhile

import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib
import math

import importlib
import src.cell as cell_lib
import src.board as board_lib
import src.piece as piece_lib
import src.texture as texture_lib
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.player import Player
#from src.player import Player

#from player import Player, HumanPlayer, Move
importlib.reload(cell_lib)
importlib.reload(piece_lib)
importlib.reload(board_lib)
importlib.reload(texture_lib)
from src.texture import Texture
from src.cell import Cell, GridCoordinates
from src.move import Move
import pygame

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

    def cell_corners(self, cx, cy, flat_top = False):
        corners = []
        if flat_top:
            offset = 0
        else:
            offset = 30
        for i in range(6):
            angle = math.radians(60 * i - offset)  # pointy-top
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

    def cartesian_to_axial(self, x, y):
        r = 2/3 * y * 1/self.cell_size
        q = 1/self.cell_size * (x/math.sqrt(3) - y/3)
        return q, r

    def cube_to_cartesian(self, q, r, s):
        x = (math.sqrt(3) * self.cell_size * self.cube_to_axial(q, r, s)[0] +
             math.sqrt(3) / 2 * self.cell_size * self.cube_to_axial(q, r, s)[1])
        y = 3 / 2 * self.cell_size * self.cube_to_axial(q, r, s)[1]
        return x, y

    @staticmethod
    def round_half_up(x):
        if x >= 0:
            return int(x + 0.5)
        else:
            return int(x - 0.5)

    def cartesian_to_cube(self, x, y):
        q, r = self.cartesian_to_axial(x, y)
        s = -q -r

        rounded_q = self.round_half_up(q)
        rounded_r = self.round_half_up(r)
        rounded_s = self.round_half_up(s)

        # Compute the difference after rounding
        dq = abs(q - rounded_q)
        dr = abs(r - rounded_r)
        ds = abs(s - rounded_s)

        # Fix the coordinate that changed the most such that q+r+s=0
        if dq > dr and dq > ds:
            rounded_q = -rounded_r -rounded_s
        if dr > ds:
            rounded_r = -rounded_q -rounded_s
        else:
            rounded_s = -rounded_q -rounded_r

        return rounded_q, rounded_r, rounded_s

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

        #FIXME This import is hotfix - solve circular imports
        from src.player import Player

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

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece, image, x, y):
        super().__init__()
        self.piece = piece
        self.image = image
        self.rect = image.get_rect(center=(x, y))

class MouseProxy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

class PygameGUI(UI):
    def __init__(self, game_state, cell_size = 1,  screen_width = 1000, screen_height = 750):
        super().__init__(game_state, cell_size, canvas_size_x=screen_width, canvas_size_y=screen_height)
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.BANK_WIDTH = self.screen_width * 0.1
        self.BANK_HEIGHT = self.screen_height
        self.white_bank_surface = pygame.Surface((self.BANK_WIDTH, self.BANK_HEIGHT))
        self.black_bank_surface = pygame.Surface((self.BANK_WIDTH, self.BANK_HEIGHT))
        self.white_bank_surface.fill((255, 255, 255))
        self.black_bank_surface.fill((255, 255, 255))
        self.white_bank_rectangle = pygame.Rect(self.screen_width - self.BANK_WIDTH, 0, self.BANK_WIDTH, self.BANK_HEIGHT)
        self.black_bank_rectangle = pygame.Rect(0, 0, self.BANK_WIDTH, self.BANK_HEIGHT)
        self.white_bank_sprites = pygame.sprite.Group()
        self.black_bank_sprites = pygame.sprite.Group()

        self.VIEWPORT_WIDTH = self.screen_width - 2 * self.BANK_WIDTH
        self.VIEWPORT_HEIGHT = self.screen_height
        self.viewport_surface = pygame.Surface((self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT), pygame.SRCALPHA)
        self.viewport_surface.fill((255, 255, 255))
        self.viewport_rectangle = pygame.Rect(self.BANK_WIDTH, 0, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)

        pygame.display.set_caption("Hive Game")

        self.textures = {Texture.TextureType.WHITE_PIECE: pygame.image.load("assets/textures/white_piece.png").convert_alpha(),
                         Texture.TextureType.BLACK_PIECE: pygame.image.load("assets/textures/black_piece.png").convert_alpha(),
                         Texture.TextureType.QUEEN: pygame.image.load("assets/textures/queen.png").convert_alpha(),
                         Texture.TextureType.ANT: pygame.image.load("assets/textures/ant.png").convert_alpha(),
                         Texture.TextureType.BEETLE: pygame.image.load("assets/textures/beetle.png").convert_alpha(),
                         Texture.TextureType.GRASSHOPPER: pygame.image.load("assets/textures/grasshopper.png").convert_alpha(),
                         Texture.TextureType.LADYBUG: pygame.image.load("assets/textures/ladybug.png").convert_alpha(),
                         Texture.TextureType.MOSQUITTO: pygame.image.load("assets/textures/mosquito.png").convert_alpha(),
                         Texture.TextureType.PILLBUG: pygame.image.load("assets/textures/pillbug.png").convert_alpha(),
                         Texture.TextureType.SPIDER: pygame.image.load("assets/textures/spider.png").convert_alpha(),
                         Texture.TextureType.HIGHLIGHTED_CELL: pygame.image.load("assets/textures/highlighted_cell.png").convert_alpha(),
                         Texture.TextureType.SUGGESTED_MOVE: pygame.image.load("assets/textures/suggested_move.png").convert_alpha(),
                         Texture.TextureType.UNKNOWN: pygame.image.load("assets/textures/unknown_texture.png").convert_alpha()
                         }

        #Scale textures properly
        scale = int(self.cell_size * 1.98)
        for key, texture in self.textures.items():
            self.textures[key] = pygame.transform.smoothscale(texture, (0.865*scale, scale))

    def handle_click_on_board(self, origin_x = None, origin_y = None):
        if (origin_x is None) or (origin_y is None):
            origin_x = self.screen_centre_x
            origin_y = self.screen_centre_y
        mx, my = pygame.mouse.get_pos()
        x = mx - origin_x
        y = my - origin_y
        q, r, s = self.cartesian_to_cube(x, y)
        return q, r, s

    def wait_for_user_input(self, player_color):
        start_q, start_r, start_s = None, None, None
        end_q, end_r, end_s = None, None, None
        start_cell_selected = False
        end_cell_selected = False
        print(f"Player color: {player_color}")
        print("Click the start of the move:")
        while not start_cell_selected:
            time.sleep(0.01)        # This is to save CPU
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.white_bank_rectangle.collidepoint(mouse_pos):
                        clicked_sprite = pygame.sprite.spritecollideany(MouseProxy(mouse_pos),
                                                                        self.white_bank_sprites)
                        if clicked_sprite:
                            piece = clicked_sprite.piece
                            start_coord = None
                            print(f"Selected {piece}")
                            start_cell_selected = True
                        else:
                            print(f"Select cell with a piece")
                            self.clear_canvas()
                            self.draw_board()
                            self.draw_stats()
                            return self.wait_for_user_input(player_color)
                    elif self.black_bank_rectangle.collidepoint(mouse_pos):
                        clicked_sprite = pygame.sprite.spritecollideany(MouseProxy(mouse_pos),
                                                                        self.black_bank_sprites)
                        if clicked_sprite:
                            piece = clicked_sprite.piece
                            start_coord = None
                            print(f"Selected {piece}")
                            start_cell_selected = True
                        else:
                            print(f"Select cell with a piece")
                            self.clear_canvas()
                            self.draw_board()
                            self.draw_stats()
                            return self.wait_for_user_input(player_color)
                    else:
                        start_q, start_r, start_s = self.handle_click_on_board()
                        print(f"Clicked start cell: {start_q}, {start_r}, {start_s}")
                        start_cell = self.game.get_cell(GridCoordinates(start_q, start_r, start_s))
                        if not start_cell.has_piece():
                            print(f"Select cell with a piece")
                            self.clear_canvas()
                            self.draw_board()
                            self.draw_stats()
                            return self.wait_for_user_input(player_color)
                        piece = start_cell.get_top_piece()
                        start_coord = start_cell.coord
                        print(f"Selected {piece}.")
                        self.draw_cell(start_cell.coord, cell_texture=Texture.TextureType.HIGHLIGHTED_CELL)
                        start_cell_selected = True

        if piece.color == player_color:
            self.show_canvas()
        else:
            print(f"Select piece of {player_color} player.")
            self.clear_canvas()
            self.draw_board()
            self.draw_stats()
            return self.wait_for_user_input(player_color)

        possible_moves = piece.get_possible_moves(self.game)
        print(f"Possible moves: {possible_moves}")
        self.draw_cells(possible_moves, cell_texture = Texture.TextureType.SUGGESTED_MOVE)
        self.draw_piece_banks()
        self.show_canvas()

        print(f"Click end of the move:")
        while not end_cell_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    end_q, end_r, end_s = self.handle_click_on_board()
                    print(f"Clicked end cell: {end_q}, {end_r}, {end_s}")
                    end_cell_selected = True

        end_cell = self.game.get_cell(GridCoordinates(end_q, end_r, end_s))
        end_coord = end_cell.coord
        if end_cell not in possible_moves:
            print(f"Select only cells from allowed moves.")
            self.draw_board()
            self.draw_piece_banks()
            self.draw_stats()
            return self.wait_for_user_input(player_color)

        return Move(start_coord, end_coord, piece)

    def draw_cell(self, coord, cell_texture=Texture.TextureType.NO_TEXTURE,
                  show_coords=False, show_border=True):
        cx = self.cube_to_cartesian(coord.q, coord.r, coord.s)[0]
        cy = self.cube_to_cartesian(coord.q, coord.r, coord.s)[1]
        self.draw_piece(cx, cy, cell_texture, show_border=show_border)

        # screen = self._ensure_screen()

        if show_coords:
            font = pygame.font.Font(None, 15)
            text_surface = font.render(f"{coord.q, coord.r}", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.VIEWPORT_WIDTH/2 + cx - self.cell_size * 0,
                                                      self.VIEWPORT_HEIGHT/2 + cy))
            self.viewport_surface.blit(text_surface, text_rect)
        return

    def draw_piece(self, cx, cy, piece_texture=Texture.TextureType.NO_TEXTURE,
                   show_border=True, surface = None, center_offset = True, flat_top = False):
        if surface is None:
            surface = self.viewport_surface

        if center_offset:
            draw_x = surface.get_width() // 2 + cx
            draw_y = surface.get_height() // 2 + cy
        else:
            draw_x = cx
            draw_y = cy

        textures_stack = []
        if piece_texture == Texture.TextureType.NO_TEXTURE:
            textures_stack = []
        elif piece_texture == Texture.TextureType.HIGHLIGHTED_CELL:
            textures_stack.append(self.textures[Texture.TextureType.HIGHLIGHTED_CELL])
        elif piece_texture == Texture.TextureType.SUGGESTED_MOVE:
            textures_stack.append(self.textures[Texture.TextureType.SUGGESTED_MOVE])
        elif piece_texture == Texture.TextureType.WHITE_QUEEN:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.QUEEN])
        elif piece_texture == Texture.TextureType.WHITE_SPIDER:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.SPIDER])
        elif piece_texture == Texture.TextureType.WHITE_GRASSHOPPER:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.GRASSHOPPER])
        elif piece_texture == Texture.TextureType.WHITE_BEETLE:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.BEETLE])
        elif piece_texture == Texture.TextureType.WHITE_ANT:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.ANT])
        elif piece_texture == Texture.TextureType.WHITE_LADYBUG:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.LADYBUG])
        elif piece_texture == Texture.TextureType.WHITE_MOSQUITTO:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.MOSQUITTO])
        elif piece_texture == Texture.TextureType.WHITE_PILLBUG:
            textures_stack.append(self.textures[Texture.TextureType.WHITE_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.PILLBUG])
        elif piece_texture == Texture.TextureType.BLACK_QUEEN:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.QUEEN])
        elif piece_texture == Texture.TextureType.BLACK_SPIDER:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.SPIDER])
        elif piece_texture == Texture.TextureType.BLACK_GRASSHOPPER:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.GRASSHOPPER])
        elif piece_texture == Texture.TextureType.BLACK_BEETLE:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.BEETLE])
        elif piece_texture == Texture.TextureType.BLACK_ANT:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.ANT])
        elif piece_texture == Texture.TextureType.BLACK_LADYBUG:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.LADYBUG])
        elif piece_texture == Texture.TextureType.BLACK_MOSQUITTO:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.MOSQUITTO])
        elif piece_texture == Texture.TextureType.BLACK_PILLBUG:
            textures_stack.append(self.textures[Texture.TextureType.BLACK_PIECE])
            textures_stack.append(self.textures[Texture.TextureType.PILLBUG])
        else:
            textures_stack.append(self.textures[Texture.TextureType.UNKNOWN])
            print(f"Warning: {piece_texture} is unknown, or not implemented in this GUI. "
                  f"Setting turquoise.")

        for texture in textures_stack:
            rect = texture.get_rect(center=(draw_x, draw_y))
            if flat_top:
                texture = pygame.transform.rotate(texture, 30)
            surface.blit(texture, rect)
        return surface

    def draw_stats(self):
        #screen = self._ensure_screen()
        font = pygame.font.SysFont("Comic Sans", 25)
        if self.game.white_turn:
            line1 = "White turn"
        else:
            line1 = "Black turn"
        line2 = f"  Round: {self.game.round_counter}"
        text_surface1 = font.render(line1, True, (0, 0, 0))
        text_surface2 = font.render(line2, True, (0, 0, 0))

        x = 0.45 * self.VIEWPORT_HEIGHT
        y = 0.07 * self.VIEWPORT_HEIGHT
        self.viewport_surface.blit(text_surface1, (x, y))
        self.viewport_surface.blit(text_surface2, (x, y + text_surface1.get_height() + 2))  # 2px spacing

        return

    @staticmethod
    def rgba_to_pygame(rgba):
        r, g, b, a = rgba
        return int(r * 255), int(g * 255), int(b * 255), int(a * 255)

    #FIXME This has to be implemented
    def draw_piece_banks(self):
        indent_x = self.BANK_WIDTH/2
        indent_y = 0
        piece_separation = self.cell_size * 0.8

        # Draw white bank
        piece_no = 0
        for piece in self.game.piece_bank_white.values():
            piece_no += 1
            if piece.coord is None:
                self.draw_piece(indent_x, indent_y + piece_no * (self.cell_size + piece_separation),
                                piece_texture=piece.texture, surface=self.white_bank_surface, center_offset=False,
                                flat_top=True)
                sprite = PieceSprite(piece, self.textures[Texture.TextureType.WHITE_PIECE],
                                     indent_x + (self.screen_width - self.BANK_WIDTH), indent_y + piece_no * (self.cell_size + piece_separation))
                self.white_bank_sprites.add(sprite)

        # Draw black bank
        piece_no = 0
        for piece in self.game.piece_bank_black.values():
            piece_no += 1
            if piece.coord is None:
                self.draw_piece(indent_x, indent_y + piece_no * (self.cell_size + piece_separation),
                                piece_texture=piece.texture, surface=self.black_bank_surface, center_offset=False,
                                flat_top=True)
                sprite = PieceSprite(piece, self.textures[Texture.TextureType.BLACK_PIECE],
                                     indent_x, indent_y + piece_no * (self.cell_size + piece_separation))
                self.black_bank_sprites.add(sprite)

        return

    # This should draw only placed pieces, not empty cells
    def draw_board(self, show_coords=False, show_grid=False):
        #self.clear_canvas()
        white_pieces = self.game.piece_bank_white
        black_pieces = self.game.piece_bank_black
        # Draw only pieces that are on top and not in bank
        for bank in (white_pieces, black_pieces):
            for piece in bank.values():
                if piece.coord is not None:
                    piece_on_top = (self.game.get_cell(piece.coord).get_top_piece() == piece)
                    if piece_on_top:
                        self.draw_cell(piece.coord, cell_texture=piece.texture,
                                        show_coords=show_coords, show_border=True)

    def show_canvas(self):
        self.screen.blit(self.viewport_surface, (self.BANK_WIDTH, 0))
        self.screen.blit(self.white_bank_surface, (self.screen_width - self.BANK_WIDTH, 0))
        self.screen.blit(self.black_bank_surface, (0,0))
        pygame.display.flip()
        return

    def clear_canvas(self):
        if self.screen is None:
            return
        self.viewport_surface.fill((255, 255, 255))
        self.white_bank_surface.fill((255, 255, 255))
        self.black_bank_surface.fill((255, 255, 255))
        return