from timeit import timeit
import sudoku
import sudokuclass
import sudokun

board = sudoku.get_puzzle('puzzles/3.txt')
print sudoku.puzzle_string(board)
print

puzzle = sudoku.get_puzzle('puzzles/3.txt')
sudoku.solve(puzzle)
print sudoku.puzzle_string(puzzle)
print

puzzle = sudokuclass.Sudoku('puzzles/3.txt')
puzzle.solve()
print puzzle
print

puzzle = sudokun.Sudoku('puzzles/3.txt')
puzzle.solve()
print puzzle

print timeit(
    "sudoku.solve(sudoku.get_puzzle('puzzles/3.txt'))",
    setup='import sudoku',
    number=100
)
print timeit(
    "sudokuclass.Sudoku('puzzles/3.txt').solve()",
    setup='import sudokuclass',
    number=100
)
print timeit(
    "sudokun.Sudoku('puzzles/3.txt').solve()",
    setup='import sudokun',
    number=100
)