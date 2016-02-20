from math import sqrt
from collections import deque, defaultdict
from copy import deepcopy
from itertools import chain

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
 
    def related(board, x, y):
        boxx = (x / boxlen) * boxlen
        boxy = (y / boxlen) * boxlen
        return \
            board[x][:y] + board[x][y+1:] + \
            [line[y] for line in board[:x] + board[x+1:]] + [
                board[bx][by]
                for by in xrange(boxy, boxy + boxlen) if by != y
                for bx in xrange(boxx, boxx + boxlen) if bx != x
            ]

    def solved(board):
        for line in board:
            for point in line:
                if type(point) == set: return False
        return True

    def valid(board):
        for x, line in enumerate(board):
            for y, point in enumerate(line):
                if type(point) != set and point in related(board, x, y): return False
        return True

    def solve_point(board, x, y, val):
        board[x][y] = val
        for i in related(board, x, y):
            if type(i) == set: i.discard(val)

    def reduce(board, x, y):
        relations = related(board, x, y)
        board[x][y] -= set(i for i in relations if type(i) != set)
        if len(board[x][y]) == 1:
            solve_point(board, x, y, board[x][y].pop())
            return True
        return False

    def solve_board(board):
        progress = True
        while progress:
            progress = False
            for x, line in enumerate(board):
                for y, point in enumerate(line):
                    if type(point) == set and reduce(board, x, y):
                        progress = True

    def next_boards(board):
        # get coordinates of all points with
        # fewest number of guesses to choose from
        min_guesses = 1000000 # max int
        for x, line in enumerate(board):
            for y, point in enumerate(line):
                if type(point) != set: continue
                opt_count = len(point)
                if opt_count < min_guesses:
                    min_guesses = opt_count
                    guess_points = [(x,y)]
                elif opt_count == min_guesses:
                    guess_points.append((x,y))
        
        # yield clones of board with each point guessed each way
        # some kind of heuristic involved?
        # Order suggestions in the most impactful way possible?
        # how many set-type relatives exist for the point?
        points = defaultdict(list)
        for x, y in guess_points:
            influence = len([i for i in related(board, x, y) if type(i) == set])        
            points[influence].append((x,y))

        for x, y in chain(*[points[k] for k in reversed(sorted(points))]):
        # for x, y in guess_points:
            for option in board[x][y]:
                b2 = deepcopy(board)
                solve_point(b2, x, y, option)
                if not valid(b2): continue
                solve_board(b2)
                yield b2
        '''
        for k, v in reversed(sorted(points)):
            for x, y in v:
                for option in board[x][y]:
                    b2 = deepcopy(board)
                    solve_point(b2, x, y, option)
                    if not valid(b2): continue
                    solve_board(b2)
                    yield b2
        '''

    # bfs
    solve_board(board)
    node_queue = deque((board,))
    visited_nodes = []
    while node_queue:
        node = node_queue.popleft()
        if node in visited_nodes: continue
        visited_nodes.append(node)
        if solved(node): return node
        node_queue.extend(next_boards(node))
    return False
