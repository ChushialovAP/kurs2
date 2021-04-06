from checkers.constants import *
from copy import deepcopy

moves = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
jumps = [[2, 2], [2, -2], [-2, 2], [-2, -2]]


def isValidRow(y):
    if 0 <= y < ROWS:
        return True
    return False


def isValidCol(x):
    if 0 <= x < COLS:
        return True
    return False


class Move:
    def __init__(self, checker, piece, variant):
        self.checker = checker
        self.piece = piece
        self.type = variant
        self.distance = 1
        self.weight = None
        self.jumped = []

    def apply(self, board):
        board[self.checker.x, self.checker.y] = None
        board[self.piece[0], self.piece[1]] = deepcopy(self.checker)
        board[self.piece[0], self.piece[1]].x = self.piece[0]
        board[self.piece[0], self.piece[1]].y = self.piece[1]
        for jump in self.jumped:
            board[jump[0], jump[1]] = None
        return board


def getNeighbor(board, y, x, up=False, down=False):
    validMoves = []
    if not up:
        for move in moves[:2]:
            if isValidRow(y + move[1]) and isValidCol(x + move[0]):
                if board[y + move[1]][x + move[0]] is None:
                    validMoves.append((y + move[1], x + move[0]))
    elif not down:
        for move in moves[2:]:
            if isValidRow(y + move[1]) and isValidCol(x + move[0]):
                if board[y + move[1]][x + move[0]] is None:
                    validMoves.append((y + move[1], x + move[0]))
    return validMoves


def getJumps(board, y, x, color):
    validMoves = []
    jumped = []
    for jump, move in zip(jumps, moves):
        if isValidRow(y + move[1]) and isValidCol(x + move[0]):
            if isValidRow(y + jump[1]) and isValidCol(x + jump[0]):
                if board[y + move[1]][x + move[0]] is not None:
                    if board[y + move[1]][x + move[0]].black != color:
                        if board[y + jump[1]][x + jump[0]] is None:
                            validMoves.append((y + jump[1], x + jump[0]))
                            jumped.append((y + move[1], x + move[0]))
    return validMoves, jumped


def findMoves(board, color):
    moves = []
    for checker in board.flat:
        if checker is None or checker.black != color:
            continue
        if checker.king:
            options = getNeighbor(board, checker.x, checker.y)
        elif color:
            options = getNeighbor(board, checker.x, checker.y, down=True)
        elif not color:
            options = getNeighbor(board, checker.x, checker.y, up=True)

        for option in options:
            moves.append(Move(checker, (option[0], option[1]), "Move"))
    return moves


def copyBoard(origin):
    new_board = deepcopy(origin)
    return new_board


def findJumps(board, color, old=None, depth=0):
    jumps = []
    for checker in board.flat:
        if checker is None or checker.black != color:
            continue
        options, jumped = getJumps(board, checker.x, checker.y, checker.black)

        for option, jump in zip(options, jumped):
            move = Move(checker, (option[0], option[1]), "Jump")
            move.jumped.append(jump)

            new_board = copyBoard(board)
            move.apply(new_board)

            if depth < 3:
                new_jumps = findJumps(new_board, color, option, depth + 1)
                extra_jump = False
                for n_jump in new_jumps:
                    if n_jump.checker.id == checker.id:
                        extra_jump = True
                        n_jump.jumped.append(jump)
                        if old is not None:
                            n_jump.jumped.append(old)
                        n_jump.checker = checker
                        jumps.append(n_jump)
                if not extra_jump:
                    jumps.append(move)
    return jumps
