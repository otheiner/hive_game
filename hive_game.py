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
        ax = ui._ensure_ax()
        ax.clear()  # <<< CLEAR OLD DRAWING
        ax.set_xlim(0, ui.canvas_size_x)
        ax.set_ylim(0, ui.canvas_size_y)
        ax.set_aspect("equal")
        ax.axis("off")
        if move:
            print(move)
            ui.game.make_move(move)
            ui.draw_board(show_grid=True, show_coords=True)
            ui.draw_stats()
            ui.draw_piece_banks()
            ui.show_canvas()
            current_player_index = 1 - current_player_index

if __name__ == "__main__":
    main()