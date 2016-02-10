OPTIONS = ('1','2','3','4','5','6','7','8','9')
PUZZLE_SIZE = len(OPTIONS)
BOX_SIZE = PUZZLE_SIZE / 3

def get_options():
    return set(OPTIONS)

def get_puzzle(file_path):
    return [
        [get_options() if c == ' ' else c for c in l]
        for l in open(file_path,'r').read().split('\n')
    ]

def print_puzzle(data):
    for row in data:
        for col in row:
            print (col if type(col) != set else ' '),
        print

def knowns(data):
    return (i for i in data if type(i) != set)

def unknowns(data):
    return (i for i in data if type(i) == set)

def row(data, row):
    return (i for i in data[row])

def col(data, col):
    return (data[i][col] for i in xrange(len(data)))

def box(data, row, col):
    row = (row / BOX_SIZE) * BOX_SIZE
    col = (col / BOX_SIZE) * BOX_SIZE
    for x in xrange(row, row + BOX_SIZE):
        for y in xrange(col, col + BOX_SIZE):
            yield data[x][y]

def related(data, x, y):
    for i in row(data, x): yield i
    for i in col(data, y): yield i
    for i in box(data, x, y): yield i

def reduce(data, x, y):
    point = data[x][y]
    relations = related(data, x, y)
    # remove known values from the list of possibilities
    point -= set(knowns(relations))
    # if only one value left, we've solved that point
    if len(point) == 0:
        print_puzzle(data)
        raise ValueError('Point {}, {} appears to have no possible options'.format(x, y))
    if len(point) == 1:
        point = point.pop()
        print '{},{} is {}'.format(x, y, point)
        # save value to point in stead of set of options
        data[x][y] = point
        # remove that value as an option from other related unknowns
        for i in unknowns(relations):
            i.discard(point)
        return True
    return False

def reduce_pass(data):
    progress = False
    for x in xrange(len(data)):
        for y in xrange(len(data[x])):
            if type(data[x][y]) == set:
                if reduce(data, x, y):
                    progress = True
    return progress

data = get_puzzle('puzzles/1.txt')
print_puzzle(data)
while reduce_pass(data):
    print
    print
    print_puzzle(data)