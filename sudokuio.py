def get_board(file_path): return [
    [c for c in line]
    for line in open(file_path, 'r').read().split('\n')
]

def board_string(board): return '\n'.join(
    ' '.join(c if type(c) == str and len(c) == 1 else ' ' for c in line)
    for line in board
)
