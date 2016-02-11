from timeit import timeit
import sudoku
import sudokuclass
import sudokun

board = sudoku.get_puzzle('puzzles/1.txt')
print sudoku.puzzle_string(board)

puzzle = sudoku.get_puzzle('puzzles/1.txt')
sudoku.solve(puzzle)
print sudoku.puzzle_string(puzzle)

puzzle = sudokuclass.Sudoku('puzzles/1.txt')
puzzle.solve()
print puzzle

puzzle = sudokun.Sudoku('puzzles/1.txt')
puzzle.solve()
print puzzle

print timeit(
    "sudoku.solve(sudoku.get_puzzle('puzzles/1.txt'))",
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