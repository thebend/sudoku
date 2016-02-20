import itertools
from math import sqrt

DEFAULT_OPTIONS = set('123456789')

def get_board(file_path, options = DEFAULT_OPTIONS): return [
    [options.copy() if c == ' ' else c for c in line]
    for line in open(file_path, 'r').read().split('\n')
]

def board_string(board): return '\n'.join(
    ' '.join(c if type(c) != set else ' ' for c in line)
    for line in board
)

def solve(board, options = DEFAULT_OPTIONS):
    boxlen = int(sqrt(len(options)))
    
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
        return False
    
    def reduce(x, y):
        point = board[x][y]
        
        def notpoint(i): return i is not point
        rowr = filter(notpoint, row(x))
        colr = filter(notpoint, col(y))
        boxr = filter(notpoint, box(x, y))
        relations = rowr + colr + boxr
        
        if resolve(x, y, point, relations): return True

        choices = len(point) # track if we narrow down choices
        point -= set(filter(known, relations))
        if resolve(x, y, point, relations): return True

        # must be what nothing else can be
        for group in rowr, colr, boxr:
            unique_options = point - set(itertools.chain(*filter(unknown, group)))
            if resolve(x, y, unique_options, relations): return True

        if choices > len(point): return True

    progress = True
    while progress:
        progress = False
        for x, line in enumerate(board):
            for y, point in enumerate(line):
                if type(point) == set and reduce(x, y):
                    progress = True
