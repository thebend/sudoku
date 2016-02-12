from timeit import timeit
import sudoku
import sudokuclass
import sudokun


# OPTIONS = set('123456789ABCDEFG')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

board = sudoku.get_board('puzzles/1.txt')
print sudoku.board_string(board)

puzzle = sudoku.get_board('puzzles/1.txt')
sudoku.solve(puzzle)
print sudoku.board_string(puzzle)

puzzle = sudokuclass.Sudoku('puzzles/1.txt')
puzzle.solve()
print puzzle

puzzle = sudokun.Sudoku('puzzles/1.txt')
puzzle.solve()
print puzzle

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