import sys

from src.cell import GridCoordinates

sys.path.append("src")

from game_engine import Game
from player import HumanPlayer, Player
from ui import MatplotlibGUI
from move import Move

def main():
    game = Game(5)
    ui = MatplotlibGUI(game,1.3, 40, 40)
    players = [HumanPlayer(Player.PlayerColor.WHITE,ui), HumanPlayer(Player.PlayerColor.BLACK,ui)]

    # This is game for testing
    ui.game.make_move(Move(None, GridCoordinates(0, 0), ui.game.piece_bank_white["queen"]))
    ui.game.make_move(Move(None, GridCoordinates(0, -1), ui.game.piece_bank_black["ant1"]))
    ui.game.make_move(Move(None, GridCoordinates(0, 1), ui.game.piece_bank_white["ant1"]))
    ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["ant2"]))
    ui.game.make_move(Move(None, GridCoordinates(0, 2), ui.game.piece_bank_white["grasshopper1"]))
    ui.game.make_move(Move(None, GridCoordinates(0, -3), ui.game.piece_bank_black["mosquito"]))
    ui.game.make_move(Move(None, GridCoordinates(1, 1), ui.game.piece_bank_white["mosquito"]))
    #ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["queen"]))
    #ui.game.make_move(Move(GridCoordinates(0, 1), GridCoordinates(-1, -0), ui.game.piece_bank_white["ant1"]))

    current_player_index = 0
    ui.draw_board(show_grid=True, show_coords=True)
    ui.draw_stats()
    ui.draw_piece_banks()
    ui.show_canvas()

    while not game.winning_state:
        player = players[current_player_index]
        move = player.get_move(game)
        if move is None:
            return
        if ui.game.make_move(move):
            print(move)
            if ui.game.winning_state:
                print(f"Player {player.color} wins!")
                return
            ui.draw_board(show_grid=True, show_coords=True)
            ui.draw_stats()
            ui.draw_piece_banks()
            if isinstance(ui, MatplotlibGUI):
                ui.show_canvas()
            current_player_index = 1 - current_player_index
        else:
            print(f"Enter move for this player again.")

if __name__ == "__main__":
    main()