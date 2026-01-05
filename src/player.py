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
            pieces_around_my_queen = game.get_cell(game.piece_bank[self.color]["queen"].coord).get_occupied_neighbors()
            opponent_possible_moves = len(game.list_all_possible_moves(self.opponent_color))
            pieces_around_opponents_queen = game.get_cell(game.piece_bank[self.opponent_color]["queen"].coord).get_occupied_neighbors()

            pieces_around_my_queen = 10 if pieces_around_my_queen == 6 else pieces_around_my_queen
            pieces_around_opponents_queen = 10 if pieces_around_opponents_queen == 6 else pieces_around_opponents_queen

            game_eval = (0.9*my_possible_moves - opponent_possible_moves +
                         (-10**pieces_around_my_queen + 0.9*10**pieces_around_opponents_queen))
            #game_eval = (- opponent_possible_moves + 100 * (pieces_around_opponents_queen))
            return game_eval
        elif strategy == 2:
            my_possible_moves = game.list_all_possible_moves(self.color)
            count_my_possible_moves = len(my_possible_moves)
            if game.white_queen_placed and game.black_queen_placed:
                pieces_around_my_queen = len(game.get_occupied_neighbors(game.piece_bank[self.opponent_color]["queen"].coord))
                pieces_around_opponents_queen = len(game.get_occupied_neighbors(game.piece_bank[self.opponent_color]["queen"].coord))
            else:
                pieces_around_my_queen = 0
                pieces_around_opponents_queen = 0

            opponent_possible_moves = game.list_all_possible_moves(self.opponent_color)
            count_opponent_possible_moves = len(opponent_possible_moves)

            #Possible queen moves of my queen
            opponent_queen_dodges = 0
            my_queen_dodges = 0
            for move in opponent_possible_moves:
                if move.piece == game.piece_bank[self.opponent_color]["queen"]:
                    opponent_queen_dodges += 1
                if move.piece == game.piece_bank[self.color]["queen"]:
                    my_queen_dodges += 1

            #Count possible moves towards opponents queen
            empty_cells_around_opponents_queen = game.get_empty_neighbors(game.piece_bank[self.opponent_color]["queen"].coord)
            for move in my_possible_moves:
                if game.get_cell(move.final_coord) in empty_cells_around_opponents_queen:
                    pieces_around_opponents_queen += 1
                    break

            if pieces_around_my_queen == 6:
                return -10000000
            if pieces_around_opponents_queen == 6:
                return 10000000

            game_eval = ((pieces_around_my_queen + pieces_around_opponents_queen) / 12 *
                         ((count_my_possible_moves - count_opponent_possible_moves) +
                         -10000*pieces_around_my_queen * (6 - my_queen_dodges) +
                          10000 * pieces_around_opponents_queen * (6 - opponent_queen_dodges)))

            return game_eval
        else:
            raise ValueError(f"Unknown evaluation strategy for AI player")

    NO_OF_EVALS = 0
    def minimax(self, game_state, depth=1, evaluation_strategy=1):
        depth_limit = 2
        odd_move = (depth % 2 == 0)
        player_color = self.color if not odd_move else self.opponent_color

        #FIXME This is a bit weird - should be written with check winning state
        if game_state.white_queen_placed and game_state.black_queen_placed:
            pieces_around_my_queen = len(game_state.get_occupied_neighbors(game_state.piece_bank[self.color]["queen"].coord))
            pieces_around_opponents_queen = len(game_state.get_occupied_neighbors(game_state.piece_bank[self.opponent_color]["queen"].coord))
            if pieces_around_my_queen == 6 and pieces_around_opponents_queen != 6:
                return -20000000, None
            elif pieces_around_opponents_queen == 6 and pieces_around_my_queen != 6:
                return 20000000, None
            elif pieces_around_opponents_queen == 6 and pieces_around_my_queen == 6:
                return 10000000, None


        if depth == depth_limit:
            self.NO_OF_EVALS += 1
            print(f"Eval no: {self.NO_OF_EVALS}")
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
        score, best_move = self.minimax(game, evaluation_strategy=2)
        self.NO_OF_EVALS = 0
        return best_move
