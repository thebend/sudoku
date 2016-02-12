from math import sqrt

DEFAULT_OPTIONS = set('123456789')

class Sudoku:
    def __init__(self, file_path, options = DEFAULT_OPTIONS):
        self.boxlen = int(sqrt(len(options)))
        self.board = [
            [options.copy() if val == ' ' else val for val in line]
            for line in open(file_path,'r').read().split('\n')
        ]

    def __repr__(self):
        return '\n'.join(
            ' '.join(col if type(col) != set else ' ' for col in row)
            for row in self.board
        )

    def related(self, x, y):
        boxx = (x / self.boxlen) * self.boxlen
        boxy = (y / self.boxlen) * self.boxlen
        box = [
            self.board[bx][by] # box
            for by in xrange(boxy, boxy + self.boxlen)
            for bx in xrange(boxx, boxx + self.boxlen)
        ]
        row = [self.board[i][y] for i in xrange(len(self.board))]
        col = [i for i in self.board[x]]
        return row + col + box

    def reduce(self, x, y):
        point = self.board[x][y]
        relations = self.related(x, y)
        knowns = (i for i in relations if type(i) != set)
        unknowns = (i for i in relations if type(i) == set)
        point -= set(knowns)
        if len(point) == 1:
            point = point.pop()
            self.board[x][y] = point
            for i in unknowns:
                i.discard(point)
            return True
        return False

    def solve(self):
        progress = True
        while progress:
            progress = False
            for x in xrange(len(self.board)):
                for y in xrange(len(self.board[x])):
                    if type(self.board[x][y]) == set:
                        if self.reduce(x, y):
                            progress = True
