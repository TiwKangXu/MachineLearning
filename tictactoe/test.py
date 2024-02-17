from tictactoe import *


board_1 = [[EMPTY, O, O],
        [EMPTY, X, X],
            [X, O, X]]

board_2 = [[X, EMPTY, X],
            [EMPTY, EMPTY, O],
            [O, O, X]]


print(minimax(board_1))
