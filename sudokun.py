'''
Tiles notify relatives when solved,
recursively solving each other
'''

from math import sqrt

DEFAULT_OPTIONS = set('123456789')
class Tile:
    def __init__(self, val, options):
        self.options = options.copy() if val == ' ' else set(val)

    def __repr__(self):
        return ' ' if self.unknown() 1 else iter(self.options).next()

    def unknown(self): return len(self.options) > 1

    def reduce(self, option):
        if option not in self.options: return # stop if already eliminated
        self.options.discard(option)
        self.solve()

    def solve(self):
        if not self.unknown():
            for i in self.dependents: i.dependents.discard(self)
            for i in self.dependents: i.reduce(iter(self.options).next())

class Sudoku:
    def __repr__(self): return '\n'.join(
            ' '.join(map(str, line)) for line in self.board
        )

    def related(self, x, y):
        boxx = x / self.boxlen * self.boxlen
        boxy = y / self.boxlen * self.boxlen
        return self.board[x] + [line[y] for line in self.board] + [
            self.board[bx][by]
            for by in xrange(boxy, boxy + self.boxlen)
            for bx in xrange(boxx, boxx + self.boxlen)
        ]

    def __init__(self, file_path, options = DEFAULT_OPTIONS):
        self.boxlen = int(sqrt(len(options)))
        self.board = [
            [Tile(c, options) for c in line]
            for line in open(file_path, 'r').read().split('\n')
        ]

        for x, line in enumerate(self.board):
            for y, p in enumerate(line):
                p.dependents = set(filter(Tile.unknown, self.related(x, y)))
                p.dependents.discard(p)

    def solve(self):
        for line in self.board:
            for point in line: point.solve()
