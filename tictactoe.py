"""
Tic Tac Toe Player
"""

import math
import copy
from queue import Empty
import re

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
    if board == initial_state():
        return X
    elif terminal(board):
        return "The Game is Over."
    xCounts = 0
    oCounts = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                xCounts += 1
            elif board[i][j] == O:
                oCounts += 1

    if xCounts > oCounts:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return "The Game is Over."

    availableActions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                availableActions.add((i, j))

    return availableActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = copy.deepcopy(board)

    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Not Possible Action")
    else:
        newBoard[action[0]][action[1]] = player(board)

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking horizontally
    for i in range(len(board)):
        if (len(set(board[i])) == 1) and board[i][0] is not EMPTY:
            return board[i][0]

    # Checking Vertically
    for i in range(len(board)):
        if (len(set([row[i] for row in board])) == 1) and board[0][i] is not EMPTY:
            return board[0][i]

    # Checking Diagonally
    mainDiagonal = [board[i][i] for i in range(len(board))]
    secondaryDiagonal = [board[i][len(board)-i-1] for i in range(len(board))]

    if (len(set(mainDiagonal)) == 1) and mainDiagonal[0] is not EMPTY:
        return mainDiagonal[0]
    if (len(set(secondaryDiagonal)) == 1) and secondaryDiagonal[0] is not EMPTY:
        return secondaryDiagonal[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == EMPTY:
                    return False
        
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    toTrack = {}

    if player(board) == X:
        for action in actions(board):
            toTrack[minValue(result(board, action))] = action
        maxV = max(toTrack.keys())
        return toTrack[maxV]

    if player(board) == O:
        for action in actions(board):
            toTrack[maxValue(result(board, action))] = action
        minV = min(toTrack.keys())
        return toTrack[minV]

    raise NotImplementedError


def maxValue(board):
    
    if terminal(board):
        return utility(board)
    
    v = -math.inf

    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    
    if terminal(board):
        return utility(board)
    
    v = math.inf

    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v