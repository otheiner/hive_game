import random
import numpy as np
from src.piece import Piece

class ZobristHashing():
    def __init__(self, game):
        random.Random(42)
        self.STACK_HEIGHT_LIMIT = 6
        self.BOARD_RADIUS_LIMIT = 25
        self.hash = 0

        self.coord_to_index = {}
        self.piece_to_index = {}
        self.hash_table = None
        self.init_hash_table(game.piece_bank)
        self.compute_game_hash(game)

    def init_hash_table(self, piece_banks):
        radius = self.BOARD_RADIUS_LIMIT
        i = 0
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                if abs(q + r) <= radius:
                    self.coord_to_index[(q, r)] = i
                    i += 1
        self.coord_to_index[None] = i

        j = 0
        for piece_color in Piece.PieceColour:
            for piece_type in Piece.PieceType:
                piece_key = (piece_type.value, piece_color.value)
                self.piece_to_index[piece_key] = j
                j += 1
        print(self.piece_to_index)

        seed = 0
        self.hash_table = np.zeros((len(self.coord_to_index), len(self.piece_to_index),
                                    self.STACK_HEIGHT_LIMIT), dtype=object)
        for position in self.coord_to_index.values():
            for piece in self.piece_to_index.values():
                for stack_position in range(self.STACK_HEIGHT_LIMIT):
                    random.Random(seed)
                    self.hash_table[position][piece][stack_position] = random.getrandbits(64)
                    seed += 1

    def compute_game_hash(self, game):
        for color_bank in game.piece_bank.values():
            for piece in color_bank.values():
                piece_index = self.piece_to_index[(piece.type.value, piece.color.value)]
                position_key = (piece.coord.q, piece.coord.r) if piece.coord is not None else None
                position_index = self.coord_to_index[position_key]
                stack_position = game.piece_stack_position(piece)
                self.hash ^= self.hash_table[position_index][piece_index][stack_position]

    def update_hash(self, move, stack_position_start, stack_position_end):
        piece_index = self.piece_to_index[(move.piece.type.value, move.piece.color.value)]
        position_key_from = (move.current_coord.q, move.current_coord.r) if move.current_coord is not None else None
        position_index_from = self.coord_to_index[position_key_from]
        position_key_to = (move.final_coord.r, move.final_coord.r) if move.final_coord is not None else None
        position_index_to = self.coord_to_index[position_key_to]
        self.hash ^= self.hash_table[position_index_from][piece_index][stack_position_start]
        self.hash ^= self.hash_table[position_index_to][piece_index][stack_position_end]
        #print("hash", self.hash)