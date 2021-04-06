from tkinter import *
import numpy
import copy
import ai
from checkers.constants import *


class Checker:
    def __init__(self):
        self.alive = True
        self.king = False
        self.x = None
        self.y = None
        self.black = False
        self.circle = None
        self.id = None
        self.index = None


class Game(Canvas):

    win = tkinter.Tk()

    waitingMove = False
    currentChecker = None
    color = True

    board = numpy.empty((8, 8), dtype=Checker)
    availableMoves = []
    checkers = []

    def __init__(self):
        self.win.minsize(HEIGHT, WIDTH)
        Canvas.__init__(self, self.win, bg="white", height=HEIGHT, width=WIDTH)
        self.pack()
        self.bind("<Button-1>", self.getUserClick)

        self.initBoard()
        self.drawBoard()
        self.drawCheckers()

        self.win.mainloop()

    def initBoard(self):
        for x in range(0, 8):
            piece_offset = True if x % 2 else False
            for y in range(0, 8):
                if (x % 2 == 0 or y % 2 == 0) and piece_offset:
                    self.addChecker(x, y)
                elif (x % 2 == 1 or y % 2 == 1) and not piece_offset:
                    self.addChecker(x, y)

    def addChecker(self, x, y):
        if y == 3 or y == 4:
            return
        checker = Checker()
        checker.id = (x, y)
        checker.index = x * 8 + (y + 1)
        if y < 4:
            checker.black = True
        checker.x = x
        checker.y = y
        self.board[x, y] = checker
        self.checkers.append(checker)

    def drawBoard(self):
        for x in range(0, 8):
            color_offset = True if x % 2 else False
            for y in range(0, 8):
                color = FIRST_TILE_COLOR
                if x % 2 != color_offset or y % 2 != color_offset:
                    color = SECOND_TILE_COLOR
                self.create_rectangle(x * SQUARE_SIZE, y * SQUARE_SIZE,
                                      x * SQUARE_SIZE + SQUARE_SIZE, y * SQUARE_SIZE + SQUARE_SIZE,
                                      fill=color)

    def drawCheckers(self):
        radius = SQUARE_SIZE // 3
        checkerOutline = OUTLINE_COLOR

        for checker in self.board.flat:
            if checker is not None:
                if checker.black:
                    checkerColor = FIRST_COLOR
                else:
                    checkerColor = SECOND_COLOR
                self.create_oval(checker.x * SQUARE_SIZE + SQUARE_SIZE / 2 - radius,
                                 checker.y * SQUARE_SIZE + SQUARE_SIZE / 2 - radius,
                                 checker.x * SQUARE_SIZE + SQUARE_SIZE / 2 + radius,
                                 checker.y * SQUARE_SIZE + SQUARE_SIZE / 2 + radius,
                                 width=4, fill=checkerColor, outline=checkerOutline)

    def getUserClick(self, event):
        x = int(self.canvasx(event.x) // SQUARE_SIZE)
        y = int(self.canvasy(event.y) // SQUARE_SIZE)

        checker = self.board[x][y]
        if self.waitingMove:
            if checker is not None:
                return
            partial_move = ai.Move(self.currentChecker, (x, y), "?")
            self.getFullMove(partial_move)

        elif checker is not None and checker.black == self.color:
            self.currentChecker = checker
            self.waitingMove = True

    def getFullMove(self, partial_move):
        moves = ai.findJumps(self.board, self.color) + ai.findMoves(self.board, self.color)
        for move in moves:
            if move.checker.id == partial_move.checker.id and move.piece == partial_move.piece:
                move.apply(self.board)
                self.color = not self.color
                self.waitingMove = False
                self.drawBoard()
                self.drawCheckers()