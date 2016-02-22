import sudokuio, suibp

board = sudokuio.get_board('puzzles/dec-elimination-1.txt')
board = suibp.Board(board)
suibp.solve(board)
print board