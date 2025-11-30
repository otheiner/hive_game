import piece

class Cell:
    def __init__(self, q, r, s):
        if (q + r + s) != 0:
            raise ValueError("Invalid cell: q+r+s!=0")
        self.q = q
        self.r = r
        self.s = s
        self.pieces = []

    def __eq__(self, other):
        return isinstance(other, Cell) and (self.q, self.r, self.s) == (other.q, other.r, other.s)

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def print_cell(self):
        print("({}, {}, {}), pieces: ".format(self.q, self.r, self.s, self.pieces))

    def coordinates(self):
        return self.q, self.r, self.s

    def add_piece(self, added_piece):
        self.pieces.append(added_piece)

    def remove_piece(self, removed_piece):
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