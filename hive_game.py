import sys

from src.cell import GridCoordinates
from src.ui import PygameGUI

#sys.path.append("src")

from src.game_engine import Game
from src.player import HumanPlayer, Player
from src.ui import MatplotlibGUI
from src.move import Move

def main():
    game = Game(20)
    #ui = MatplotlibGUI(game,1.3, 40, 40)
    ui = PygameGUI(game, 25, 1000, 750)
    players = [HumanPlayer(Player.PlayerColor.WHITE,ui), HumanPlayer(Player.PlayerColor.BLACK,ui)]
    print(f"n cells: {len(game.cells)}")

    # This is game for testing
    ui.game.make_move(Move(None, GridCoordinates(0, 0), ui.game.piece_bank_white["queen"]))
    ui.game.make_move(Move(None, GridCoordinates(0, -1), ui.game.piece_bank_black["ant1"]))
    ui.game.make_move(Move(None, GridCoordinates(-1, 1), ui.game.piece_bank_white["ant1"]))
    ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["ant2"]))
    ui.game.make_move(Move(None, GridCoordinates(0, 1), ui.game.piece_bank_white["grasshopper1"]))
    ui.game.make_move(Move(None, GridCoordinates(1, -2), ui.game.piece_bank_black["queen"]))
    ui.game.make_move(Move(None, GridCoordinates(-1, 2), ui.game.piece_bank_white["ant3"]))
    #ui.game.make_move(Move(None, GridCoordinates(1, 1), ui.game.piece_bank_white["mosquito"]))
    #ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["queen"]))
    #ui.game.make_move(Move(GridCoordinates(0, 1), GridCoordinates(-1, -0), ui.game.piece_bank_white["ant1"]))

    # FIXME This "NOT" is a hot fix and it shouldn't be here -check player turns logic
    # Not seems a bit counterintuitive (maybe fix it) but correct
    # Player maybe changes when placement is unsuccessful
    current_player_index = int(not game.white_turn)
    print(f"current_player_index: {current_player_index}")
    print(f"white_turn: {game.white_turn}")
    ui.draw_board(show_grid=True, show_coords=True)
    ui.draw_stats()
    ui.draw_piece_banks()
    ui.show_canvas()

    while not game.winning_state:
        print(f"current_player_index: {current_player_index}")
        print(f"white_turn: {game.white_turn}")
        player = players[current_player_index]
        move = player.get_move(game)
        if move is None:
            return
        if ui.game.make_move(move):
            print(move)
            if ui.game.winning_state:
                print(f"Player {player.color} wins!")
                return
            ui.draw_board(show_coords=True)
            ui.draw_stats()
            #ui.draw_piece_banks()
            if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
                ui.show_canvas()
            current_player_index = 1 - current_player_index
        else:
            print(f"Enter move for this player again.")

if __name__ == "__main__":
    main()