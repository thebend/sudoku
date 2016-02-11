OPTIONS = set(('1','2','3','4','5','6','7','8','9'))
BOX_SIZE = len(OPTIONS) / 3

def unknowns(data):
    return (i for i in data if not i.known())

class Tile:
    def __init__(self, val):
        self.options = OPTIONS.copy() if val == ' ' else set(val)

    def val(self):
        return ' ' if len(self.options) > 1 else iter(self.options).next()

    def known(self):
        return len(self.options) == 1

    def reduce(self, option):
        if option not in self.options:
            return # don't process options already eliminated
        self.options.discard(option)
        self.solve()

    def solve(self):
        if self.known():
            for r in self.unknown_relatives:
                r.unknown_relatives.discard(self)
            for r in self.unknown_relatives:
                r.reduce(self.val())

class Sudoku:
    def __repr__(self):
        return '\n'.join(
            ' '.join(point.val() for point in line)
            for line in self.board
        )

    def row(self, row):
        return (i for i in self.board[row])

    def col(self, col):
        return (self.board[i][col] for i in xrange(len(self.board)))

    def box(self, row, col):
        row = (row / BOX_SIZE) * BOX_SIZE
        col = (col / BOX_SIZE) * BOX_SIZE
        for x in xrange(row, row + BOX_SIZE):
            for y in xrange(col, col + BOX_SIZE):
                yield self.board[x][y]

    def related(self, x, y):
        for i in self.row(x): yield i
        for i in self.col(y): yield i
        for i in self.box(x, y): yield i

    def __init__(self, file_path):
        self.board = [
            [Tile(c) for c in line]
            for line in open(file_path, 'r').read().split('\n')
        ]

        for x, line in enumerate(self.board):
            for y, p in enumerate(line):
                p.unknown_relatives = set(unknowns(self.related(x, y)))
                p.unknown_relatives.discard(p) # not relative of self!

    def solve(self):
        for line in self.board:
            for point in line:
                point.solve()
