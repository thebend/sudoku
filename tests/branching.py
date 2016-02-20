import sudokuio
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
    board = sudokuio.get_board(path)
    print 'Original puzzle'
    print sudokuio.board_string(board)
    print
    board = sudoku.solve(board, OPTIONS)
    print 'Single pass attempt'
    print sudokuio.board_string(board)
    print
    board = sudokuio.get_board(path)
    board = sui.solve(board, OPTIONS)
    print sudokuio.board_string(board)
    raw_input()
