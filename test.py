from timeit import timeit
import sudoku

data = sudoku.get_puzzle('puzzles/1.txt')
print sudoku.puzzle_string(data)
sudoku.solve(data)
print sudoku.puzzle_string(data)

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