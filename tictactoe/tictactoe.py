"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return O if sum(row.count(X) for row in board) > sum(row.count(O) for row in board) else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] is EMPTY:
                set_actions.add((row, col))
    return set_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise  Exception("Invalid action in this state!")
    next_state = copy.deepcopy(board)
    next_state[action[0]][action[1]] = player(board)
    return next_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O
        
    col_0 = []
    col_1 = []
    col_2 = []
    diag_dec = []
    diag_inc = []
    for i in range(3):
        col_0.append(board[i][0])
        col_1.append(board[i][1])
        col_2.append(board[i][2])
        diag_dec.append(board[i][i])
        diag_inc.append(board[i][2 - i])
    threes = [col_0, col_1, col_2, diag_dec, diag_inc]
    for three in threes:
        if EMPTY in three:
            continue
        elif three.count(X) == 3:
            return X
        elif three.count(O) == 3:
            return O
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_count = sum(row.count(EMPTY) for row in board)
    if winner(board) is not None or empty_count == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) is X else -1 if winner(board) is O else 0

class Node():
    def __init__(self, state, v, a, b, successors):
        self.state = state
        self.v = v
        self.a = a
        self.b = b
        self.successors = successors

def print_board(board):
    for row in board:
        print(row)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    root = Node(board, -math.inf, -math.inf, math.inf, [])
    
    v = 0

    if player(board) is X:
        v = max_value(root)
    else:
        v = min_value(root)

    for successor in root.successors:
        if successor.v == v:
            for action in actions(root.state):
                if result(root.state, action) == successor.state:
                    return action
    return None

def max_value(node):
    if terminal(node.state):
        value = utility(node.state)
        node.v = value # must update terminal state's node v value also!!!!!
        return value
    node.v = -math.inf

    results = []
    for action in actions(node.state):
        results.append(result(node.state, action))

    for successor in results:
        new_node = Node(successor, math.inf, node.a, node.b, [])
        node.successors.append(new_node)
        node.v = max(node.v, min_value(new_node))

        if node.v >= node.b:
            return node.v
        node.a = max(node.a, node.v)
    return node.v

def min_value(node):
    if terminal(node.state):
        value = utility(node.state)
        node.v = value
        return value
    node.v = math.inf

    results = []
    for action in actions(node.state):
        results.append(result(node.state, action))

    for successor in results:
        new_node = Node(successor, -math.inf, node.a, node.b, [])
        node.successors.append(new_node)
        node.v = min(node.v, max_value(new_node))

        if node.v <= node.a:
            return node.v
        node.b = min(node.b, node.v)
    return node.v