import sudoku
data = sudoku.get_puzzle('puzzles/1.txt')
print sudoku.puzzle_string(data)
sudoku.solve(data)
print sudoku.puzzle_string(data)

print

import sudokuclass
solver = sudokuclass.Sudoku('puzzles/1.txt')
print solver.puzzle_string()
solver.solve()
print solver.puzzle_string()

print

import sudokun
solver = sudokun.Sudoku('puzzles/1.txt')
print solver.puzzle_string()
solver.solve()
print solver.puzzle_string()
