class Sudoku:
    OPTIONS = ('1','2','3','4','5','6','7','8','9')
    PUZZLE_SIZE = len(OPTIONS)
    BOX_SIZE = PUZZLE_SIZE / 3

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.get_puzzle(file_path)

    def get_options(self):
        return set(self.OPTIONS)

    def get_puzzle(self, file_path):
        return [
            [self.get_options() if c == ' ' else c for c in l]
            for l in open(file_path,'r').read().split('\n')
        ]

    def puzzle_string(self):
        return '\n'.join(
            ' '.join(col if type(col) != set else ' ' for col in row)
            for row in self.data
        )

    @staticmethod
    def knowns(data):
        return (i for i in data if type(i) != set)

    @staticmethod
    def unknowns(data):
        return (i for i in data if type(i) == set)

    def row(self, row):
        return (i for i in self.data[row])

    def col(self, col):
        return (self.data[i][col] for i in xrange(len(self.data)))

    def box(self, row, col):
        row = (row / self.BOX_SIZE) * self.BOX_SIZE
        col = (col / self.BOX_SIZE) * self.BOX_SIZE
        for x in xrange(row, row + self.BOX_SIZE):
            for y in xrange(col, col + self.BOX_SIZE):
                yield self.data[x][y]

    def related(self, x, y):
        for i in self.row(x): yield i
        for i in self.col(y): yield i
        for i in self.box(x, y): yield i

    def reduce(self, x, y):
        point = self.data[x][y]
        relations = self.related(x, y)
        # remove known values from the list of possibilities
        point -= set(Sudoku.knowns(relations))
        # if only one value left, we've solved that point
        if len(point) == 0:
            print self.puzzle_string()
            raise ValueError('Point {}, {} appears to have no possible options'.format(x, y))
        if len(point) == 1:
            point = point.pop()
            # save value to point in stead of set of options
            self.data[x][y] = point
            # remove that value as an option from other related unknowns
            for i in Sudoku.unknowns(relations):
                i.discard(point)
            return True
        return False

    def reduce_pass(self):
        progress = False
        for x in xrange(len(self.data)):
            for y in xrange(len(self.data[x])):
                if type(self.data[x][y]) == set:
                    if self.reduce(x, y):
                        progress = True
        return progress

    def solve(self):
        while self.reduce_pass():
            pass