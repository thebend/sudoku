from math import sqrt

DEFAULT_OPTIONS = set('123456789')

class Tile:
    def __init__(self, val, options):
        self.options = options.copy() if val == ' ' else set(val)

    def __repr__(self):
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
                r.reduce(iter(self.options).next())

class Sudoku:
    def __repr__(self):
        return '\n'.join(
            ' '.join(map(str, line))
            for line in self.board
        )

    def related(self, x, y):
        boxx = (x / self.boxlen) * self.boxlen
        boxy = (y / self.boxlen) * self.boxlen
        box = [
            self.board[bx][by]
            for by in xrange(boxy, boxy + self.boxlen)
            for bx in xrange(boxx, boxx + self.boxlen)
        ]
        row = [line[y] for line in self.board]
        col = self.board[x]
        return row + col + box

    def __init__(self, file_path, options = DEFAULT_OPTIONS):
        self.boxlen = int(sqrt(len(options)))
        self.board = [
            [Tile(c, options) for c in line]
            for line in open(file_path, 'r').read().split('\n')
        ]

        for x, line in enumerate(self.board):
            for y, p in enumerate(line):
                p.unknown_relatives = \
                    set(i for i in self.related(x, y) if not i.known())
                p.unknown_relatives.discard(p) # not relative of self!

    def solve(self):
        for line in self.board:
            for point in line:
                point.solve()
