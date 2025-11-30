from board import Board
from cell import Cell

import math
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

class Game(Board):
    def __init__(self, halfwidth, cell_size = 1,  canvas_size = 20):
        super().__init__(halfwidth)
        self.cell_size = cell_size
        self.canvas_size = canvas_size

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

    @staticmethod
    def print_cells(cells):
        for cell in cells:
            cell.print_cell()

    def cube_to_cartesian(self, q, r ,s):
        x = (math.sqrt(3) * self.cell_size * self.cube_to_axial(q, r, s)[0] +
             math.sqrt(3)/2 * self.cell_size * self.cube_to_axial(q, r, s)[1])
        y = 3/2 * self.cell_size * self.cube_to_axial(q, r, s)[1]
        return x, y

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

    def draw_cells(self,cells, border_color='black', fill_color='white', fill_alpha=1):
        for cell in cells:
            self.draw_cell(cell,border_color = border_color, fill_color = fill_color,
                           fill_alpha = fill_alpha)
        return

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                for k in range(self.board_size):
                    if self.board[i, j, k] != 0:
                        cell = self.array_to_board(i, j, k)
                        if self.board[i, j, k] == 1:
                            self.draw_cell(cell, fill_alpha=0)
                        if self.board[i, j, k] == 2:
                            self.draw_cell(cell, fill_color='orange')
                        if self.board[i, j, k] == 3:
                            self.draw_cell(cell, fill_color='yellow')
                        if self.board[i, j, k] == 4:
                            self.draw_cell(cell, fill_color='blue')

    def show_board(self):
        if self.ax is None:
            self._ensure_ax()
        plt.show()

    def has_piece(self, cell):
        i, j, k = self.board_to_array(cell)
        if self.board[i, j, k] > 1:
            return True
        else:
            return False


    @staticmethod
    def get_neighbours(cell):
        neighbours = [Cell(cell.q + 1, cell.r - 1, cell.s    ),
                      Cell(cell.q + 1, cell.r    , cell.s - 1),
                      Cell(cell.q - 1, cell.r + 1, cell.s    ),
                      Cell(cell.q - 1, cell.r    , cell.s + 1),
                      Cell(cell.q    , cell.r + 1, cell.s - 1),
                      Cell(cell.q    , cell.r - 1, cell.s + 1)]
        return neighbours

    def get_occupied_cells(self):
        occupied_cells = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                for k in range(self.board_size):
                    if self.board[i, j, k] > 1:
                        occupied_cells.append(self.array_to_board(i, j, k))
        return occupied_cells

    def get_occupied_neighbours(self, cell):
        neighbours = self.get_neighbours(cell)
        occupied_neighbours = []
        for neighbour in neighbours:
            if self.has_piece(neighbour):
                occupied_neighbours.append(neighbour)
        return occupied_neighbours

    def get_empty_neighbours(self, cell):
        neighbours = self.get_neighbours(cell)
        empty_neighbours = []
        for neighbour in neighbours:
            if not self.has_piece(neighbour):
                empty_neighbours.append(neighbour)
        return empty_neighbours

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
                if not self.has_piece(neighbour):
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
                if not self.has_piece(neighbour):
                    not_in_outer_border = True
                    for cell in playable_border:
                        if cell == neighbour:
                            not_in_outer_border = False
                    if not_in_outer_border:
                        playable_border.append(neighbour)
        return playable_border

    #TODO Fix logic in this function - it is probably almost correct
    def move_preserves_continuity(self, cell_to_remove):
        occupied_cells = self.get_occupied_cells()
        occupied_cells_wo_piece = [c for c in occupied_cells
                          if not (c.q == cell_to_remove.q and c.r == cell_to_remove.r and c.s == cell_to_remove.s)]
        print("test")
        self.print_cells(occupied_cells_wo_piece)

        # If no occupied cells remain, continuity is trivially preserved
        if not occupied_cells_wo_piece:
            return True

        connected = self.get_connected_cells(occupied_cells_wo_piece[0])
        if len(occupied_cells) - 1 == len(connected):
            return True
        else:
            return False