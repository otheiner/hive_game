class Move:
    def __init__(self, start_coord, end_coord, piece):
        #TODO Check objects types entered (coord, coord, piece)
        self.current_coord = start_coord
        self.final_coord = end_coord
        self.piece = piece

    def __repr__(self):
        return f"{self.piece.PieceColour} {self.piece.PieceType} from {self.current_coord} to {self.final_coord}"