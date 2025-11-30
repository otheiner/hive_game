class Cell:
    def __init__(self, q, r, s):
        if (q + r + s) != 0:
            raise ValueError("Invalid cell: q+r+s!=0")
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, other):
        return isinstance(other, Cell) and (self.q, self.r, self.s) == (other.q, other.r, other.s)

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def print_cell(self):
        print("({}, {}, {})".format(self.q, self.r, self.s))