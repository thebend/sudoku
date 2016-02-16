from math import sqrt
from collections import deque
from copy import deepcopy

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

    # print ' '.join(c if type(c) != set else ' ' for c in (related(board, 0, 0)))
    
    def invalid(board):
        for x, line in enumerate(board):
            for y, point in enumerate(line):
                if type(point) != set and point in related(board, x, y): return True
        return False

    def solve_point(board, x, y, val):
        board[x][y] = val
        for i in related(board, x, y):
            if type(i) == set: i.discard(val)

    def next_boards(board):
        # track coordinates of all points with
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
        for x, y in guess_points:
            for option in board[x][y]:
                b2 = deepcopy(board)
                # should solve entire board as best as possible
                # with traditional algorithm
                solve_point(b2, x, y, option)
                if invalid(b2): continue
                yield b2

    def solved(board):
        for line in board:
            for point in line:
                if type(point) == set: return False
        return True

    # what happens when I make a bad guess?
    # something will have zero options?
    # But will solve when it hits one assuming all is good

    # bfs
    node_queue = deque((board,))
    visited_nodes = []
    while node_queue:
        node = node_queue.popleft()
        if node in visited_nodes: continue
        visited_nodes.append(node)
        print board_string(node)
        if solved(node): return node
        node_queue.extend(next_boards(node))
    return False
   
board = get_board('puzzles/1.txt')
board = subfs.solve(board)
print subfs.board_string(board)
