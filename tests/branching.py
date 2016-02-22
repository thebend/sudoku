import sudokuio
import sudoku
import sui

STANDARD_OPTIONS = set('123456789')
dec = [
    ('puzzles/dec-branch-1.txt', STANDARD_OPTIONS),
    ('puzzles/dec-branch-2.txt', STANDARD_OPTIONS),
    ('puzzles/dec-branch-3.txt', STANDARD_OPTIONS)
]
# OPTIONS = set('0123456789ABCDEF')
# OPTIONS = set('123456789ABCDEFG')
# OPTIONS = set('123456789ABCDEFGHIJKLMNOP')
# OPTIONS = set('ABCDEFGHIJKLMNOPQRSTUVWXY')
hex = [
    ('puzzles/hex-1.txt', set('0123456789ABCDEF')),
    ('puzzles/hex-2.txt', set('123456789ABCDEFG'))
]

cent = [
    ('puzzles/cent-1.txt', set('123456789ABCDEFGHIJKLMNOP')),
    ('puzzles/cent-2.txt', set('ABCDEFGHIJKLMNOPQRSTUVWXY'))
]

for path, options in dec:
    board = sudokuio.get_board(path)
    print 'Original puzzle'
    print sudokuio.board_string(board)
    print
    board = sudoku.solve(board, options)
    print 'Single pass attempt'
    print sudokuio.board_string(board)
    print
    board = sudokuio.get_board(path)
    board = sui.solve(board, options)
    print sudokuio.board_string(board)
    raw_input()
