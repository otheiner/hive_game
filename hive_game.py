from src.ui import PygameGUI

from src.game_engine import Game, Logbook, Log
from src.player import HumanPlayer, Player, RandomAI, MinimaxAI
from src.ui import MatplotlibGUI

def main():
    game = Game()
    #ui = MatplotlibGUI(game,1.3, 40, 40)
    ui = PygameGUI(game, 28, 1200, 750, Log.DebugLevel.INFO)

    if isinstance(ui, PygameGUI):
        if ui.game_setup() == -1:
            return
        elif ui.game_setup() == 1:
           players = [HumanPlayer(Player.PlayerColor.WHITE, ui), RandomAI(Player.PlayerColor.BLACK, ui)]
        elif ui.game_setup() == 2:
           players = [HumanPlayer(Player.PlayerColor.WHITE, ui), MinimaxAI(Player.PlayerColor.BLACK, ui)]
        elif ui.game_setup() == 3:
           players = [HumanPlayer(Player.PlayerColor.WHITE, ui), HumanPlayer(Player.PlayerColor.BLACK, ui)]
        else:
           raise ValueError("Invalid game setup")
    else:
        players = [HumanPlayer(Player.PlayerColor.WHITE, ui), MinimaxAI(Player.PlayerColor.BLACK, ui)]

    # This is game for testing
    # ui.game.make_move(Move(None, GridCoordinates(0, 0), ui.game.piece_bank["white"]["ant1"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -1), ui.game.piece_bank["black"]["ant1"]))
    # ui.game.make_move(Move(None, GridCoordinates(-1, 1), ui.game.piece_bank["white"]["ant2"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -2), ui.game.piece_bank["black"]["ant2"]))
    # ui.game.make_move(Move(None, GridCoordinates(1, 0), ui.game.piece_bank["white"]["ant3"]))
    # ui.game.make_move(Move(None, GridCoordinates(0, -3), ui.game.piece_bank["black"]["beetle1"]))

    # "not" seems a bit counterintuitive (maybe fix it) but it is correct
    # Player maybe changes when placement is unsuccessful
    show_coordinates_switch = False
    current_player_index = int(not game.white_turn)
    ui.clear_canvas()
    ui.draw_board(show_coords=show_coordinates_switch)
    ui.draw_stats()
    ui.draw_piece_banks()
    ui.show_canvas()

    while not game.winning_state:
        player = players[current_player_index]
        if len(game.list_all_possible_moves(player.color)) == 0:
            ui.game.logs.info(f"No possible moves for {player.color}. Other player's turn.")
            ui.game.update_stats()
            ui.clear_canvas()
            ui.draw_board(show_coords=show_coordinates_switch)
            ui.draw_stats()
            ui.draw_piece_banks()
            if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
                ui.show_canvas()
            current_player_index = 1 - current_player_index
        else:
            if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
                ui.show_canvas()
            move = player.get_move(game)
            if move is None:
                return
            if ui.game.make_move(move):
                ui.clear_canvas()
                ui.draw_board(show_coords=show_coordinates_switch)
                ui.draw_stats()
                ui.draw_piece_banks()
                if isinstance(ui, MatplotlibGUI) or isinstance(ui, PygameGUI):
                    ui.show_canvas()
                if ui.game.winning_state:
                    #FIXME The message who wins is not shown correctly (if white loses when he makes move to make him lose
                    ui.game.logs.info(f"Player {player.color} wins!")
                    ui.show_message(f"Player {player.color} wins!")
                    return
                current_player_index = 1 - current_player_index
            else:
                ui.game.logs.info(f"Enter move for this player again.")

if __name__ == "__main__":
    main()