from math import sqrt

# OPTIONS = set('123456789')
OPTIONS = set('123456789ABCDEFG')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')
BOX_SIZE = int(sqrt(len(OPTIONS)))

def knowns(data):
    return (i for i in data if type(i) != set)

def unknowns(data):
    return (i for i in data if type(i) == set)

class Sudoku:
    def __init__(self, file_path):
        self.board = [
            [OPTIONS.copy() if val == ' ' else val for val in line]
            for line in open(file_path,'r').read().split('\n')
        ]

    def __repr__(self):
        return '\n'.join(
            ' '.join(col if type(col) != set else ' ' for col in row)
            for row in self.board
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

    def reduce(self, x, y):
        point = self.board[x][y]
        relations = self.related(x, y)
        point -= set(knowns(relations)) # remove known values from possibilities
        if len(point) == 1:
            point = point.pop()
            self.board[x][y] = point
            for i in unknowns(relations):
                i.discard(point)
            return True
        return False

    def reduce_pass(self):
        progress = False
        for x in xrange(len(self.board)):
            for y in xrange(len(self.board[x])):
                if type(self.board[x][y]) == set:
                    if self.reduce(x, y):
                        progress = True
        return progress

    def solve(self):
        while self.reduce_pass(): pass
