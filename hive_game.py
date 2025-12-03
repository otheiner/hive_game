import sys
sys.path.append("src")

from game_engine import Game
from player import HumanPlayer, Player
from ui import MatplotlibGUI


def main():
    game = Game(7)
    ui = MatplotlibGUI(game,1.3, 40, 40)
    players = [HumanPlayer(Player.PlayerColor.WHITE,ui), HumanPlayer(Player.PlayerColor.BLACK,ui)]
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