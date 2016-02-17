import sudoku
import subfs
import subfsi

path = 'puzzles/8.txt'
OPTIONS = set('123456789')
# OPTIONS = set('0123456789ABCDEF')
# OPTIONS = set('123456789ABCDEFG')
# OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

board = sudoku.get_board(path, OPTIONS)
print 'Original puzzle'
print sudoku.board_string(board)
print
sudoku.solve(board, OPTIONS)
print 'Single pass attempt'
print sudoku.board_string(board)
print
print
board = subfsi.get_board(path, OPTIONS)
board = subfsi.solve(board, OPTIONS)
if board: print subfsi.board_string(board)
else: print 'No solution'
