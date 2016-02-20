import sudoku
import sui

paths = [
    'puzzles/dec-branch-1.txt',
    'puzzles/dec-branch-2.txt',
    'puzzles/dec-branch-3.txt'
]
OPTIONS = set('123456789')
# OPTIONS = set('0123456789ABCDEF')
# OPTIONS = set('123456789ABCDEFG')
# OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')

for path in paths:
    board = sudoku.get_board(path, OPTIONS)
    print 'Original puzzle'
    print sudoku.board_string(board)
    print
    sudoku.solve(board, OPTIONS)
    print 'Single pass attempt'
    print sudoku.board_string(board)
    print
    board = sui.get_board(path, OPTIONS)
    board = sui.solve(board, OPTIONS)
    print sui.board_string(board)
    raw_input()
