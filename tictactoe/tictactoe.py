"""
Tic Tac Toe Player

DO NOT EDIT ANYTHING OUTSIDE THE FUNCTIONS BELOW.
"""

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
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    if terminal(board):
        return None
    return X if count_x == count_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return set()
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    i, j = action
    new_board = [row[:] for row in board]  # deep copy
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Rows
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]
    # Columns
    for j in range(3):
        if board[0][j] is not None and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    # Diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = float("-inf")
        best_action = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action))
            if min_v > v:
                v = min_v
                best_action = action
                if v == 1:
                    break
        return v, best_action

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = float("inf")
        best_action = None
        for action in actions(state):
            max_v, _ = max_value(result(state, action))
            if max_v < v:
                v = max_v
                best_action = action
                if v == -1:
                    break
        return v, best_action

    if current_player == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action

