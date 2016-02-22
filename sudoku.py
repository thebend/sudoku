'''
2D list of either values, or sets of possible values.
Relationships are computed each pass and
points reduced based on related values and possible values
'''
from math import sqrt
from itertools import chain

DEFAULT_OPTIONS = set('123456789')
def solve(board, options = DEFAULT_OPTIONS):
    boxlen = int(sqrt(len(options)))
    board = [
        [c if type(c) == str and c not in ('',' ') else options.copy() for c in line]
        for line in board
    ]
    
    def row(x): return list(board[x])
    def col(y): return [line[y] for line in board]
    def box(x, y):
        boxx = x / boxlen * boxlen
        boxy = y / boxlen * boxlen
        return [
            board[bx][by]
            for by in xrange(boxy, boxy + boxlen)
            for bx in xrange(boxx, boxx + boxlen)
        ]
    
    def known(point): return type(point) != set
    def unknown(point): return type(point) == set

    def resolve(x, y, options, relations):
        if len(options) == 1:
            board[x][y] = options.pop()
            for i in relations:
                if type(i) == set: i.discard(board[x][y])
            return True
    
    def reduce(x, y):
        point = board[x][y]
        
        def notpoint(i): return i is not point
        relrow = filter(notpoint, row(x))
        relcol = filter(notpoint, col(y))
        relbox = filter(notpoint, box(x, y))
        relations = relrow + relcol + relbox
        
        if resolve(x, y, point, relations): return True

        choices = len(point) # track if we narrow down choices
        point -= set(filter(known, relations))
        if resolve(x, y, point, relations): return True

        # must be what nothing else can be
        for group in relrow, relcol, relbox:
            unique_options = point - set(chain(*filter(unknown, group)))
            if resolve(x, y, unique_options, relations): return True

        if choices > len(point): return True

    progress = True
    while progress:
        progress = False
        for x, line in enumerate(board):
            for y, point in enumerate(line):
                if type(point) == set and reduce(x, y):
                    progress = True
    return board