import sys

from src.cell import GridCoordinates
from src.ui import PygameGUI

#sys.path.append("src")

from src.game_engine import Game, Logbook, Log
from src.player import HumanPlayer, Player, RandomAIPlayer
from src.ui import MatplotlibGUI
from src.move import Move

def main():
    game = Game(30)
    #ui = MatplotlibGUI(game,1.3, 40, 40)
    ui = PygameGUI(game, 28, 1200, 750, Log.DebugLevel.INFO)
    #players = [HumanPlayer(Player.PlayerColor.WHITE,ui), HumanPlayer(Player.PlayerColor.BLACK,ui)]
    players = [HumanPlayer(Player.PlayerColor.WHITE,ui), RandomAIPlayer(Player.PlayerColor.BLACK,ui)]

    # This is game for testing
    # ui.game.make_move(Move(None, GridCoordinates(0, 0), ui.game.piece_bank_white["queen"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -1), ui.game.piece_bank_black["ant1"]))
    # ui.game.make_move(Move(None, GridCoordinates(-1, 1), ui.game.piece_bank_white["ant1"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["ant2"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, 1), ui.game.piece_bank_white["grasshopper1"]))
    # ui.game.make_move(Move(None, GridCoordinates(1, -2), ui.game.piece_bank_black["queen"]))
    # ui.game.make_move(Move(None, GridCoordinates(-1, 2), ui.game.piece_bank_white["ant3"]))
    # ui.game.make_move(Move(None, GridCoordinates(1, -3), ui.game.piece_bank_black["beetle1"]))
    # ui.game.make_move(Move(None, GridCoordinates(1, 0), ui.game.piece_bank_white["beetle1"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -3), ui.game.piece_bank_black["spider1"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, 2), ui.game.piece_bank_white["spider1"]))
    #ui.game.make_move(Move(None, GridCoordinates(1, 1), ui.game.piece_bank_white["mosquito"]))
    #ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank_black["queen"]))
    #ui.game.make_move(Move(GridCoordinates(0, 1), GridCoordinates(-1, -0), ui.game.piece_bank_white["ant1"]))

    # FIXME This "NOT" is a hot fix and it shouldn't be here -check player turns logic
    # Not seems a bit counterintuitive (maybe fix it) but correct
    # Player maybe changes when placement is unsuccessful
    current_player_index = int(not game.white_turn)
    ui.clear_canvas()
    ui.draw_board(show_coords=False)
    ui.draw_stats()
    ui.draw_piece_banks()
    ui.show_canvas()

    while not game.winning_state:
        player = players[current_player_index]
        if len(game.list_all_possible_moves(player.color)) == 0:
            ui.game.logs.info(f"No possible moves for {player.color}. Other player's turn.")
            ui.game.update_stats()
            pass
        if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
            ui.show_canvas()
        move = player.get_move(game)
        if move is None:
            return
        if ui.game.make_move(move):
            if ui.game.winning_state:
                ui.game.logs.info(f"Player {player.color} wins!")
                return
            ui.clear_canvas()
            ui.draw_board(show_coords=False)
            ui.draw_stats()
            ui.draw_piece_banks()
            if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
                ui.show_canvas()
            current_player_index = 1 - current_player_index
        else:
            ui.game.logs.info(f"Enter move for this player again.")

if __name__ == "__main__":
    main()