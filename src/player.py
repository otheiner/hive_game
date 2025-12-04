import ui as UI

class Player:
    class PlayerColor:
        WHITE = "white"
        BLACK = "black"

    def __init__(self, color, ui):
        self.color = color
        self.ui = ui
        if color == Player.PlayerColor.WHITE:
            self.piece_bank = ui.game.piece_bank_white
        elif color == Player.PlayerColor.BLACK:
            self.piece_bank = ui.game.piece_bank_black
        else:
            raise ValueError(f"Invalid player color: {color}.")

    def get_move(self, game):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, color, ui):
        #TODO Add here new human controlled UIs to following condition
        if not isinstance(ui, UI.MatplotlibGUI):
            raise ValueError(f"Human player cannot use {ui.__class__} UI.")
        super().__init__(color, ui)

    def get_move(self, game):
        move = self.ui.wait_for_user_input(self.color)
        return move