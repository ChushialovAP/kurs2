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


def getNeighbor(board, y, x, color, king=False):
    validMoves = []
    if king:
        for move in moves:
            for mult in range(1, 7):
                if isValidRow(y + move[1] * mult) and isValidCol(x + move[0] * mult):
                    if board[y + move[1] * mult][x + move[0] * mult] is None:
                        validMoves.append((y + move[1] * mult, x + move[0] * mult))
                    else:
                        break
    elif color:
        for move in moves[:2]:
            if isValidRow(y + move[1]) and isValidCol(x + move[0]):
                if board[y + move[1]][x + move[0]] is None:
                    validMoves.append((y + move[1], x + move[0]))
    else:
        for move in moves[2:]:
            if isValidRow(y + move[1]) and isValidCol(x + move[0]):
                if board[y + move[1]][x + move[0]] is None:
                    validMoves.append((y + move[1], x + move[0]))

    return validMoves


def getJumps(board, y, x, king=False):
    validMoves = []
    jumped = []
    if king:
        for move in moves:
            for mult in range(2, 6):
                if isValidRow(y + move[1] * mult) and isValidCol(x + move[0] * mult):
                    if board[y + move[1] * mult][x + move[0] * mult] is None:
                        if board[y + move[1] * (mult - 1)][x + move[0] * (mult - 1)] is not None:
                            if board[y + move[1] * (mult - 1)][x + move[0] * (mult - 1)].black != board[y][x].black:
                                validMoves.append((y + move[1] * mult, x + move[0] * mult))
                                jumped.append((y + move[1] * (mult - 1), x + move[0] * (mult - 1)))
                    else:
                        break
    else:
        for jump, move in zip(jumps, moves):
            if isValidRow(y + move[1]) and isValidCol(x + move[0]):
                if isValidRow(y + jump[1]) and isValidCol(x + jump[0]):
                    if board[y + move[1]][x + move[0]] is not None:
                        if board[y + move[1]][x + move[0]].black != board[y][x].black:
                            if board[y + jump[1]][x + jump[0]] is None:
                                validMoves.append((y + jump[1], x + jump[0]))
                                jumped.append((y + move[1], x + move[0]))
    return validMoves, jumped


def findMoves(board, color):
    moves = []
    for checker in board.flat:
        if checker is None or checker.black != color:
            continue
        options = getNeighbor(board, checker.x, checker.y, checker.black, checker.king)

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
        options, jumped = getJumps(board, checker.x, checker.y, checker.king)

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
