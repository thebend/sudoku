import sudoku
data = sudoku.get_puzzle('puzzles/1.txt')
sudoku.print_puzzle(data)
while sudoku.reduce_pass(data):
    print
    print
    sudoku.print_puzzle(data)