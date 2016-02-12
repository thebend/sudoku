from math import sqrt

DEFAULT_OPTIONS = set('123456789')

def get_board(file_path, options = DEFAULT_OPTIONS):
    return [
        [options.copy() if c == ' ' else c for c in line]
        for line in open(file_path,'r').read().split('\n')
    ]

def board_string(board):
    return '\n'.join(
        ' '.join(c if type(c) != set else ' ' for c in line)
        for line in board
    )

def solve(board, options = DEFAULT_OPTIONS):
    boxlen = int(sqrt(len(options)))
    
    def related(board, x, y):
        boxx = (x / boxlen) * boxlen
        boxy = (y / boxlen) * boxlen
        box = [
            board[bx][by]
            for by in xrange(boxy, boxy + boxlen)
            for bx in xrange(boxx, boxx + boxlen)
        ]
        row = [line[y] for line in board]
        col = board[x]
        return row + col + box

    def reduce(board, x, y):
        point = board[x][y]
        relations = related(board, x, y)
        knowns = (i for i in relations if type(i) != set)
        unknowns = (i for i in relations if type(i) == set)
        point -= set(knowns)
        if len(point) == 1:
            point = point.pop()
            board[x][y] = point
            for i in unknowns:
                i.discard(point)
            return True
        return False

    progress = True
    while progress:
        progress = False
        for x in xrange(len(board)):
            for y in xrange(len(board[x])):
                if type(board[x][y]) == set:
                    if reduce(board, x, y):
                        progress = True
