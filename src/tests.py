import time
from game_engine import Game
from player import Player
from move import Move
from cell import GridCoordinates
from game_engine import Log

game = Game(15)
game.logs.log_level = Log.DebugLevel.ERROR
game.make_move(Move(None, GridCoordinates(0, 0), game.piece_bank["white"]["ant1"]))
game.make_move(Move(None, GridCoordinates(0, -1), game.piece_bank["black"]["ant1"]))
# game.make_move(Move(None, GridCoordinates(-1, 1), game.piece_bank["white"]["ant2"]))
# game.make_move(Move(None, GridCoordinates(0, -2), game.piece_bank["black"]["ant2"]))
# game.make_move(Move(None, GridCoordinates(1, 0), game.piece_bank["white"]["ant3"]))
# game.make_move(Move(None, GridCoordinates(0, -3), game.piece_bank["black"]["beetle1"]))

NODES = 0
def perftest(game_state, depth):
    global NODES
    if depth == 0:
        # NODES += 1
        # if NODES % 1000 == 0:
        #     print("Visited nodes:", NODES)
        return 1
    count = 0
    odd_move = (depth % 2 == 0)
    player_color = Player.PlayerColor.WHITE if not odd_move else Player.PlayerColor.BLACK
    for move in game_state.list_all_possible_moves(player_color):
        game_state._move_piece(move)
        game_state.update_stats()
        game_state.update_stats(backwards=True)
        count += perftest(game_state, depth - 1)
        #print(count)
        game_state._move_piece_backwards(move)
    return count

start = time.time()
nodes = perftest(game, 4)
print("Nodes:", nodes)
print("nps:", nodes / (time.time() - start))
print("time:", (time.time() - start))

