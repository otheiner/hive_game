class Move:
    def __init__(self, start_coord, end_coord, piece):
        #TODO Check objects types entered (coord, coord, piece)
        self.current_coord = start_coord
        self.final_coord = end_coord
        self.piece = piece
        #This shouldn't happen but just in case
        if self.final_coord is None:
            raise ValueError(f"Move has to have final coordinates!")
        if self.piece is None:
            raise ValueError(f"Move has to have piece!")

    def __repr__(self):
        return f"{self.piece} from {self.current_coord} to {self.final_coord}"