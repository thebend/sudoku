import sudoku
data = sudoku.get_puzzle('puzzles/1.txt')
print sudoku.puzzle_string(data)
while sudoku.reduce_pass(data):
    print
    print
    print sudoku.puzzle_string(data)