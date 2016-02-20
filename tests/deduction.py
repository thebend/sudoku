from timeit import timeit
import sudoku, sudokuio

path = 'puzzles/dec-deduction-1.txt'
OPTIONS = set('123456789')
# OPTIONS = set('0123456789ABCDEF')
# OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

board = sudokuio.get_board(path)
print sudokuio.board_string(board)
print
board = sudoku.solve(board, OPTIONS)
print sudokuio.board_string(board)
print
print timeit(
    "sudoku.solve(sudokuio.get_board('puzzles/dec-deduction-1.txt'))",
    setup='import sudoku, sudokuio',
    number=1000
)
