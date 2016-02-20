from math import sqrt
from sudokuio import board_string

DEFAULT_OPTIONS = set('123456789')

class Sudoku:
    def __init__(self, board, options = DEFAULT_OPTIONS):
        self.boxlen = int(sqrt(len(options)))
        self.board = [
            [c if type(c) == str and c not in ('',' ') else options.copy() for c in line]
            for line in board
        ]

    def __repr__(self): return board_string(self.board)

    def related(self, x, y):
        boxx = x / self.boxlen * self.boxlen
        boxy = y / self.boxlen * self.boxlen
        return self.board[x] + [line[y] for line in self.board] + [
            self.board[bx][by]
            for by in xrange(boxy, boxy + self.boxlen)
            for bx in xrange(boxx, boxx + self.boxlen)
        ]

    def reduce(self, x, y):
        point = self.board[x][y]
        relations = self.related(x, y)
        point -= set(i for i in relations if type(i) != set)
        if len(point) == 1:
            point = point.pop()
            self.board[x][y] = point
            for i in relations:
                if type(i) == set: i.discard(point)
            return True
        return False

    def solve(self):
        progress = True
        while progress:
            progress = False
            for x, line in enumerate(self.board):
                for y, point in enumerate(line):
                    if type(point) == set and self.reduce(x, y):
                        progress = True
