import random
import numpy as np
from pygame.transform import average_surfaces

import src.ui as UI
from src.cell import GridCoordinates


class Player:
    class PlayerColor():
        WHITE = "white"
        BLACK = "black"

    def __init__(self, color, ui):
        self.color = color
        self.ui = ui
        if color == Player.PlayerColor.WHITE:
            self.piece_bank = ui.game.piece_bank["white"]
        elif color == Player.PlayerColor.BLACK:
            self.piece_bank = ui.game.piece_bank["black"]
        else:
            raise ValueError(f"Invalid player color: {color}.")

    @property
    def opponent_color(self):
        return Player.PlayerColor.BLACK if self.color is Player.PlayerColor.WHITE else Player.PlayerColor.WHITE

    def get_move(self, game):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, color, ui):
        #TODO Add here new human controlled UIs to following condition
        if isinstance(ui, UI.MatplotlibGUI) or isinstance(ui, UI.PygameGUI):
            super().__init__(color, ui)
        else:
            raise ValueError(f"Human player cannot use {ui.__class__} UI.")

    def get_move(self, game):
        move = self.ui.wait_for_user_input(self.color)
        return move

class AI(Player):
    def __init__(self, color, ui):
        #TODO Add here new AI controlled UIs to following condition
        if isinstance(ui, UI.MatplotlibGUI) or isinstance(ui, UI.PygameGUI):
            super().__init__(color, ui)
        else:
            raise ValueError(f"AI player cannot use {ui.__class__} UI.")

    def get_move(self, game):
        return self.select_move(game)

   #Implement this for different AI players
    def select_move(self, game):
        raise NotImplementedError()


class RandomAI(AI):
    def __init__(self, color, ui):
        super().__init__(color, ui)

    def select_move(self, game):
        possible_moves = self.ui.game.list_all_possible_moves(self.color)
        self.ui.game.logs.debug(f"Possible moves: {possible_moves}")
        move_number = random.randrange(0, len(possible_moves))
        return possible_moves[move_number]

class MinimaxAI(AI):
    def __init__(self, color, ui):
        super().__init__(color, ui)

    # TODO Come up with better evaluation functions
    def evaluate_state(self, game, strategy=1):
        import time
        if strategy == 1:
            my_possible_moves = len(game.list_all_possible_moves(self.color))

            pieces_around_my_queen = game.piece_bank[self.color]["queen"].occupied_neighbors(game)
            opponent_possible_moves = len(game.list_all_possible_moves(self.opponent_color))
            pieces_around_opponents_queen = game.piece_bank[self.opponent_color]["queen"].occupied_neighbors(game)

            pieces_around_my_queen = 100000 if pieces_around_my_queen == 6 else pieces_around_my_queen
            pieces_around_opponents_queen = 100000 if pieces_around_opponents_queen == 6 else pieces_around_opponents_queen

            game_eval = (my_possible_moves - opponent_possible_moves +
                        100 * (-pieces_around_my_queen + pieces_around_opponents_queen))
            return game_eval
        elif strategy == 2:
            my_possible_moves = len(game.list_all_possible_moves(self.color))

            pieces_around_my_queen = game.piece_bank[self.color]["queen"].occupied_neighbors(game)
            opponent_possible_moves = len(game.list_all_possible_moves(self.opponent_color))
            pieces_around_opponents_queen = game.piece_bank[self.opponent_color]["queen"].occupied_neighbors(game)

            distance_from_my_queen = 0
            opponents_pieces_on_board = 0
            my_queen_coord = game.piece_bank[self.color]["queen"].coord
            for piece in game.piece_bank[self.opponent_color]:
                if piece.coord is not None and my_queen_coord is not None:
                    distance_from_my_queen += GridCoordinates(piece.coord, my_queen_coord)
                    opponents_pieces_on_board += 1
            if opponents_pieces_on_board != 0:
                average_distance_from_my_queen = distance_from_my_queen / opponents_pieces_on_board
            else:
                average_distance_from_my_queen = 100

            distance_from_opponents_queen = 0
            my_pieces_on_board = 0
            opponents_queen_coord = game.piece_bank[self.opponent_color]["queen"].coord
            for piece in game.piece_bank[self.color]:
                if piece.coord is not None and opponents_queen_coord is not None:
                    distance_from_opponents_queen += GridCoordinates(piece.coord, opponents_queen_coord)
                    my_pieces_on_board += 1
            if my_pieces_on_board != 0:
                average_distance_from_opponents_queen = distance_from_opponents_queen / my_pieces_on_board
            else:
                average_distance_from_opponents_queen = 100

            pieces_around_my_queen = 1000000 if pieces_around_my_queen == 6 else pieces_around_my_queen
            pieces_around_opponents_queen = 1000000 if pieces_around_opponents_queen == 6 else pieces_around_opponents_queen

            game_eval = (10 * (1 / average_distance_from_opponents_queen - 0.6*1 / average_distance_from_my_queen) +
                          10 * (my_possible_moves - 0.6*opponent_possible_moves) +
                          100 * (-pieces_around_my_queen + 0.6*pieces_around_opponents_queen))
            return game_eval
        else:
            raise ValueError(f"Unknown evaluation strategy for AI player")

    NO_OF_EVALS = 0
    def minimax(self, game_state, depth=1, evaluation_strategy=1):
        depth_limit = 2
        odd_move = (depth % 2 == 0)
        player_color = self.color if not odd_move else self.opponent_color

        if depth == depth_limit:
            self.NO_OF_EVALS += 1
            #print(f"Eval no: {self.NO_OF_EVALS}")
            return self.evaluate_state(game_state, strategy=evaluation_strategy), None

        best_node_value = 1 * np.inf if odd_move else -1* np.inf
        best_move = None

        for move in game_state.list_all_possible_moves(player_color):
            game_state._move_piece(move,testing=True)
            current_node_value = self.minimax(game_state, depth + 1, evaluation_strategy=evaluation_strategy)[0]
            if odd_move:
                if current_node_value <= best_node_value:
                    if current_node_value == best_node_value:
                        if random.random() < 0.5:
                            best_node_value = current_node_value
                            best_move = move
                    else:
                        best_node_value = current_node_value
                        best_move = move
            else:
                if current_node_value >= best_node_value:
                    if current_node_value == best_node_value:
                        if random.random() < 0.5:
                            best_node_value = current_node_value
                            best_move = move
                    else:
                        best_node_value = current_node_value
                        best_move = move
            game_state._move_piece_backwards(move)

        return best_node_value, best_move

    def select_move(self, game):
        score, best_move = self.minimax(game, evaluation_strategy=1)
        self.NO_OF_EVALS = 0
        return best_move
