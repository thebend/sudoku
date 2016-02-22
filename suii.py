'''
Neither BFS nor DFS
Ordered queue by influence
Popping most recently added items off end (LIFO)
Should consider deque so I'm pulling recent additions

Desperately want to clean this up.  Do I need a Point class?  Node class?
Should I use __slots__?
'''

from math import sqrt
from itertools import chain
from collections import defaultdict, namedtuple
from copy import deepcopy
import sudokuio

# Point = namedtuple('Point', 'x y')
class Point(object):
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self): return '({}, {})'.format(self.x, self.y)

# Try making a version with this
class Node(Point):
    __slots__ = ('point','value')

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def known(self): return type(self.value) != set
    def unknown(self): return not self.known()

DEFAULT_OPTIONS = set('123456789')
def solve(board, options = DEFAULT_OPTIONS):
    boxlen = int(sqrt(len(options)))
    board = [
        [
            Node(x, y, c) if type(c) == str and c not in ('',' ')
            else Node(x, y, options.copy())
            for y, c in enumerate(line)
        ]
        for x, line in enumerate(board)
    ]

    def row(board, point):
        row = board[point.x]
        return row[:point.y] + row[point.y + 1:]

    def col(board, point):
        rows = board[:point.x] + board[point.x + 1:]
        return [row[point.y] for row in rows]

    def box(board, point):
        boxx = (point.x / boxlen) * boxlen
        boxy = (point.y / boxlen) * boxlen
        return [
            board[bx][by]
            for by in xrange(boxy, boxy + boxlen) if by != point.y
            for bx in xrange(boxx, boxx + boxlen) if bx != point.x
        ]
    
    def related(board, point): return row(board, point) + col(board, point) + box(board, point)

    def solved(board): return set not in map(type, chain(*board))

    def invalid(board):
        for point, node in knowns(board):
            if node in related(board, point): return True

    def resolve(board, point, options, relations):
        if len(options) == 1:
            board[point.x][point.y] = node = options.pop()
            for i in filter(unknown, relations): i.discard(node)
            return True
    
    def solve_point(board, point, val):
        board[point.x][point.y] = val
        for i in filter(unknown, related(board, point)): i.discard(val)

    def knowns(board):
        for x, line in enumerate(board):
            for y, node in enumerate(line):
                if known(node): yield (Point(x, y), node)

    def unknowns(board):
        for x, line in enumerate(board):
            for y, node in enumerate(line):
                if unknown(node): yield (Point(x, y), node)

    def reduce(board, point, node):
        relrow = row(board, point)
        relcol = col(board, point)
        relbox = box(board, point)
        relations = relrow + relcol + relbox

        if resolve(board, point, node, relations): return True

        choices = len(point) # track if we narrow down choices
        node -= set(filter(known, relations))
        if resolve(board, point, node, relations): return True

        # must be what nothing else can be
        for group in relrow, relcol, relbox:
            unique_options = node - set(chain(*filter(unknown, group)))
            if resolve(board, point, node, relations): return True

        if choices > len(node): return True

    def solve_board(board):
        progress = True
        while progress:
            progress = False
            for point, node in unknowns(board):
                if reduce(board, point, node): progress = True

    ''' wrong data structure for this!  Shouldn't have to sort every time '''
    def get_next_board(queue):
        for influence in reversed(sorted(queue)):
            options = queue[influence]
            while options:
                point, option, board = options.pop()
                b2 = deepcopy(board)
                solve_point(b2, point, option)
                if invalid(b2): continue
                solve_board(b2)
                return b2

    def add_options(queue, additions):
        for influence, options in additions.iteritems():
            queue[influence].extend(options)

    def next_options(board):
        # get coordinates of all points with
        # fewest number of guesses to choose from
        min_guesses = 1000000 # max int
        for point, node in unknowns(board):
            opt_count = len(point)
            if opt_count < min_guesses:
                min_guesses = opt_count
                guess_points = [point]
            elif opt_count == min_guesses:
                guess_points.append(point)
        
        # yield clones of board with each point guessed each way
        # prioritize by exploring most impactful guesses first
        options = defaultdict(list)
        for point in guess_points:
            for option in board[point.x][point.y]:
                influence = len([i for i in filter(unknown, related(board, point)) if option in i])        
                options[influence].append((point, option, board))
        return options

    # Order of traversal based on size of impact to board of next guess
    visited_boards = []
    solve_board(board)
    board_queue = defaultdict(list)
    while not solved(board):
        visited_boards.append(board)
        print sudokuio.board_string(board)
        print
        add_options(board_queue, next_options(board))
        while board in visited_boards:
            board = get_next_board(board_queue)
            if not board: return False
    return board
