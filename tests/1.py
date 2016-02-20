from timeit import timeit
import sudoku
import sudokuclass
import sudokun

path = 'puzzles/6.txt'
# OPTIONS = set('0123456789ABCDEF')
OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

board = sudoku.get_board(path, OPTIONS)
print sudoku.board_string(board)
print
sudoku.solve(board, OPTIONS)
print sudoku.board_string(board)
print
puzzle = sudokuclass.Sudoku(path, OPTIONS)
puzzle.solve()
print puzzle
print
puzzle = sudokun.Sudoku(path, OPTIONS)
puzzle.solve()
print puzzle
print

print timeit(
    "sudoku.solve(sudoku.get_board('puzzles/1.txt'))",
    setup='import sudoku',
    number=1000
)
print timeit(
    "sudokuclass.Sudoku('puzzles/1.txt').solve()",
    setup='import sudokuclass',
    number=1000
)
print timeit(
    "sudokun.Sudoku('puzzles/1.txt').solve()",
    setup='import sudokun',
    number=1000
)
print
print timeit(
    "sudoku.solve(sudoku.get_board('puzzles/3.txt', set('0123456789ABCDEF')), set('0123456789ABCDEF'))",
    setup='import sudoku',
    number=100
)
print timeit(
    "sudokuclass.Sudoku('puzzles/3.txt', set('0123456789ABCDEF')).solve()",
    setup='import sudokuclass',
    number=100
)
print timeit(
    "sudokun.Sudoku('puzzles/3.txt', set('0123456789ABCDEF')).solve()",
    setup='import sudokun',
    number=100
)

print
print timeit(
    "sudoku.solve(sudoku.get_board('puzzles/6.txt', set('ABCDEFGHIJKLMNOPQRSTUVWXY')), set('ABCDEFGHIJKLMNOPQRSTUVWXY'))",
    setup='import sudoku',
    number=100
)
print timeit(
    "sudokuclass.Sudoku('puzzles/6.txt', set('ABCDEFGHIJKLMNOPQRSTUVWXY')).solve()",
    setup='import sudokuclass',
    number=100
)
print timeit(
    "sudokun.Sudoku('puzzles/6.txt', set('ABCDEFGHIJKLMNOPQRSTUVWXY')).solve()",
    setup='import sudokun',
    number=100
)
