from timeit import timeit
import sudoku

path = 'puzzles/dec-deduction-1.txt'
OPTIONS = set('123456789')
# OPTIONS = set('0123456789ABCDEF')
# OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

board = sudoku.get_board(path, OPTIONS)
print sudoku.board_string(board)
print
sudoku.solve(board, OPTIONS)
print sudoku.board_string(board)
print
print timeit(
    "sudoku.solve(sudoku.get_board('puzzles/dec-deduction-1.txt'))",
    setup='import sudoku',
    number=1000
)
