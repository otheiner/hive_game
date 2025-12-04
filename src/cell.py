class GridCoordinates:
    def __init__(self, q, r, s = None):
        # If s not given - we assume user provided axial coordinates and s is computed
        # If s is given - we assume user provided cube coordinates, and it has to hold q + r + s = 0
        if s is None:
            s = -q -r
        if (q + r + s) != 0:
            raise ValueError("Invalid cell: q+r+s!=0")
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, other):
        return isinstance(other, GridCoordinates) and \
               (self.q, self.r, self.s) == (other.q, other.r, other.s)

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __repr__(self):
        return f"coord({self.q}, {self.r}, {self.s})"

class Cell():
    def __init__(self, coord):
        self.coord = coord
        self.pieces = []

    def __eq__(self, other):
        return isinstance(other, Cell) and self.coord == other.coord

    def __hash__(self):
        return hash(self.coord)

    def print_cell(self):
        print(f"({self.coord,q}, {self.coord.r}, {self.coord.s}), pieces: {self.pieces}")

    # def coordinates(self):
    #     return self.q, self.r, self.s

    def add_piece(self, added_piece):
        added_piece.coord = self.coord
        self.pieces.append(added_piece)

    def remove_piece(self, removed_piece):
        removed_piece.coord = None
        self.pieces.remove(removed_piece)

    def get_pieces(self):
        return self.pieces

    def get_top_piece(self):
        if len(self.pieces) > 0:
            return self.pieces[-1]
        else:
            return None

    def has_piece(self):
        if len(self.pieces) > 0:
            return True
        else:
            return False