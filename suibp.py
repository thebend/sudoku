'''
Board class, point class

Neither BFS nor DFS
Ordered queue by influence
Popping most recently added items off end (LIFO)
Should consider deque so I'm pulling recent additions
'''

from math import sqrt
from itertools import chain
from collections import defaultdict, namedtuple
from copy import deepcopy
import sudokuio

Point = namedtuple('Point', 'x y')

class Board(object):
    __slots__ = ('board','options','boxlen')
    
    DEFAULT_OPTIONS = set('123456789')
    def __init__(self, board, options = DEFAULT_OPTIONS):
        self.boxlen = int(sqrt(len(options)))
        self.options = options
        self.board = [
            [c if type(c) == str and c not in ('',' ') else options.copy() for c in line]
            for line in board
        ]

    def row(self, point):
        row = self.board[point.x]
        return row[:point.y] + row[point.y + 1:]

    def col(self, point):
        rows = self.board[:point.x] + self.board[point.x + 1:]
        return [row[point.y] for row in rows]

    def box(self, point):
        boxx = (x / self.boxlen) * self.boxlen
        boxy = (y / self.boxlen) * self.boxlen
        return [
            self.board[bx][by]
            for by in xrange(boxy, boxy + self.boxlen) if by != point.y
            for bx in xrange(boxx, boxx + self.boxlen) if bx != point.x
        ]

    def related(self, point): return self.row(point) + self.col(point) + self.box(point)

    def __len__(self):
        print "Len called"
        return len(self.board) ** 2
    
    def __iter__(self):
        print "Iter called"
        return self
    
    def next(self):
        print "next called"
        for x, line in enumerate(self.board):
            for y, node in enumerate(line):
                yield (Point(x, y), node)
    
    @staticmethod
    def known(node): return type(node) != set
    @staticmethod
    def unknown(node): return not Board.known(node)
        
    def solved(self): return set not in map(type, chain(*self.board))

    def invalid(self):
        for point, node in filter(self.known, self):
            if node in self.related(point): return True
        
    def resolve(self, point, options, relations):
        if len(options) == 1:
            self.board[point.x][point.y] = node = options.pop()
            for i in filter(self.unknown, relations): i.discard(node)
            return True

    def solve_point(self, point, val):
        self.board[point.x][point.y] = val
        for i in filter(self.unknown, self.related(point)): i.discard(val)

    def reduce(self, point):
        node = self.board[point.x][point.y]
        
        relrow = self.row(point)
        relcol = self.col(point)
        relbox = self.box(point)
        relations = relrow + relcol + relbox
        
        if self.resolve(point, node, relations): return True
        
        choices = len(node)
        node -= set(filter(self.known, relations))
        if self.resolve(point, node, relations): return True
        
        for group in relrow, relcol, relbox:
            unique_options = node - set(chain(*filter(self.unknown, group)))
            if self.resolve(point, unique_options, relations): return True

        if choices > len(point): return True

    def solve_board(self):
        progress = True
        print "Solving!"
        while progress:
            progress = False
            for point, node in filter(self.unknown, self):
                print point
                if self.reduce(point): progress = True

    def next_options(self):
        # get coordinates of all points with
        # fewest number of guesses to choose from
        min_guesses = 1000000 # max int
        for point, node in filter(self.unknown, self):
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
                influence = len([i for i in filter(self.unknown, self.related(point)) if option in i])        
                options[influence].append((point, option, board))
        return options

    def __repr__(self): return '\n'.join(
        ' '.join(c if type(c) == str and len(c) == 1 else ' ' for c in line)
        for line in self.board
    )


def get_next_board(queue):
    ''' wrong data structure for this!  Shouldn't have to sort every time '''
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
    
def solve(board):
    print board
    # Order of traversal based on size of impact to board of next guess
    visited_boards = []
    board.solve_board()
    board_queue = defaultdict(list)
    while not board.solved():
        visited_boards.append(board)
        print board
        print
        add_options(board_queue, board.next_options())
        while board in visited_boards:
            board = get_next_board(board_queue)
            if not board: return False
    return board
