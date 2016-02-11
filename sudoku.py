OPTIONS = set(('1','2','3','4','5','6','7','8','9'))
BOX_SIZE = len(OPTIONS) / 3

def get_puzzle(file_path):
    return [
        [OPTIONS.copy() if c == ' ' else c for c in l]
        for l in open(file_path,'r').read().split('\n')
    ]

def puzzle_string(board):
    return '\n'.join(
        ' '.join(val if type(val) != set else ' ' for val in line)
        for line in board
    )

def knowns(points):
    return (i for i in points if type(i) != set)

def unknowns(points):
    return (i for i in points if type(i) == set)

def row(board, row):
    return (i for i in board[row])

def col(board, col):
    return (board[i][col] for i in xrange(len(board)))

def box(board, row, col):
    row = (row / BOX_SIZE) * BOX_SIZE
    col = (col / BOX_SIZE) * BOX_SIZE
    for x in xrange(row, row + BOX_SIZE):
        for y in xrange(col, col + BOX_SIZE):
            yield board[x][y]

def related(board, x, y):
    for i in row(board, x): yield i
    for i in col(board, y): yield i
    for i in box(board, x, y): yield i

def reduce(board, x, y):
    point = board[x][y]
    relations = related(board, x, y)
    point -= set(knowns(relations)) # remove known values from possibilities
    if len(point) == 1:
        point = point.pop()
        board[x][y] = point
        for i in unknowns(relations):
            i.discard(point)
        return True
    return False

def reduce_pass(board):
    progress = False
    for x in xrange(len(board)):
        for y in xrange(len(board[x])):
            if type(board[x][y]) == set:
                if reduce(board, x, y):
                    progress = True
    return progress

def solve(board):
    while reduce_pass(board):
        pass
