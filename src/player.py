import random
import numpy as np

import src.ui as UI

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
            t1 = time.perf_counter()
            my_possible_moves = len(game.list_all_possible_moves(self.color))
            t2 = time.perf_counter()

            pieces_around_my_queen = game.piece_bank[self.color]["queen"].occupied_neighbors(game)
            opponent_possible_moves = len(game.list_all_possible_moves(self.opponent_color))
            pieces_around_opponents_queen = game.piece_bank[self.opponent_color]["queen"].occupied_neighbors(game)

            pieces_around_my_queen = 100000 if pieces_around_my_queen == 6 else pieces_around_my_queen
            pieces_around_opponents_queen = 100000 if pieces_around_opponents_queen == 6 else pieces_around_opponents_queen

            game_eval = (my_possible_moves - opponent_possible_moves +
                        100 * (-pieces_around_my_queen + pieces_around_opponents_queen))
            #print(f"possible moves: {t2 - t1} s")
            return game_eval
        elif strategy == 2:
            t1 = time.perf_counter()
            pieces_around_my_queen = self.ui.game.piece_bank[self.color]["queen"].occupied_neighbors(game)
            t2 = time.perf_counter()
            pieces_around_my_queen = 100000 if (pieces_around_my_queen == 6) else (100 * pieces_around_my_queen)
            my_movable_pieces = 0
            t3 = time.perf_counter()
            for piece in game.piece_bank[self.color].values():
                if piece.coord is not None:
                    if game.piece_can_be_lifted(piece):
                        my_movable_pieces += 1
            t4 = time.perf_counter()

            pieces_around_opponents_queen = game.piece_bank[self.opponent_color]["queen"].occupied_neighbors(game)
            pieces_around_opponents_queen = 100000 if (pieces_around_opponents_queen == 6) else (100 * pieces_around_opponents_queen)
            opponents_movable_pieces = 0
            for piece in self.ui.game.piece_bank[self.opponent_color].values():
                if piece.coord is not None:
                    if self.ui.game.piece_can_be_lifted(piece):
                        opponents_movable_pieces += 1

            game_eval = (-pieces_around_my_queen + pieces_around_opponents_queen +
                         my_movable_pieces - opponents_movable_pieces)
            print(f"pieces around queen: {t2 - t1} s, movable pieces: {t4 - t3} s")
            return game_eval
        elif strategy == 3:
            t1 = time.perf_counter()
            my_possible_moves = len(game.list_all_possible_moves(self.color))
            t2 = time.perf_counter()

            pieces_around_my_queen = game.piece_bank[self.color]["queen"].occupied_neighbors(game)
            opponent_possible_moves = len(game.list_all_possible_moves(self.opponent_color))
            pieces_around_opponents_queen = game.piece_bank[self.opponent_color]["queen"].occupied_neighbors(game)

            pieces_around_my_queen = 100000 if pieces_around_my_queen == 6 else pieces_around_my_queen
            pieces_around_opponents_queen = 100000 if pieces_around_opponents_queen == 6 else pieces_around_opponents_queen

            game_eval = (my_possible_moves - opponent_possible_moves +
                        100 * (-pieces_around_my_queen + pieces_around_opponents_queen))
            #print(f"possible moves: {t2 - t1} s")
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
