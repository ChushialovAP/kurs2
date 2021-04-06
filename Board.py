import tkinter
from tkinter import *
from checkers.constants import *
from Piece import CheckerPiece


class CheckerBoard(Canvas):
    win = tkinter.Tk()
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    rects = []
    moves = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    jumps = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
    player = 1
    toDel = []
    jump = False
    waitingMove = False
    availableMoves = []
    currentTile = None

    def __init__(self):
        self.win.minsize(HEIGHT, WIDTH)
        Canvas.__init__(self, self.win, bg="white", height=HEIGHT, width=WIDTH)
        self.pack()
        self.createTiles()
        self.createBoard()

        self.bind("<Button-1>", self.getUserClick)
        self.render()
        print(self.board)
        self.win.mainloop()

    def createBoard(self):
        for i in range(0, ROWS):
            num = 0
            if i == 3 or i == 4:
                continue
            if i < 3:
                num = 1
            elif i > 4:
                num = 2
            for j in range(0, COLS):
                if ((i + j) % 2 == 1):
                    if num == 1:
                        self.board[i][j] = 1
                    elif num == 2:
                        self.board[i][j] = 2

    def render(self):
        radius = SQUARE_SIZE // 3

        checkerColor = ""
        checkerOutline = OUTLINE_COLOR

        for i in range(0, ROWS):
            y = SQUARE_SIZE * i + SQUARE_SIZE // 2
            for j in range(0, COLS):
                if self.board[i][j] == 0:
                    continue

                if self.board[i][j] == 1:
                    checkerColor = FIRST_COLOR
                else:
                    checkerColor = SECOND_COLOR

                x = SQUARE_SIZE * j + SQUARE_SIZE // 2
                self.create_oval(x - radius, y - radius, x + radius, y + radius, width=4, fill=checkerColor,
                                 outline=checkerOutline)

    def createTiles(self):
        self.rects = []
        width = SQUARE_SIZE
        height = SQUARE_SIZE
        c = None
        for i in range(0, COLS):
            self.rects.append([])
            x1 = (i * width) + BORDER
            x2 = ((i + 1) * width) - BORDER
            self.create_line(x1, 0, x1, WIDTH, fill=OUTLINE_COLOR, width=3)
            for j in range(0, ROWS):
                y1 = (j * height) + BORDER
                y2 = ((j + 1) * height) - BORDER
                self.create_line(0, y1, HEIGHT, y1, fill=OUTLINE_COLOR, width=3)
                if (i + j) % 2 == 0:
                    c = self.create_rectangle(x1, y1, x2, y2, fill=FIRST_TILE_COLOR)
                else:
                    c = self.create_rectangle(x1, y1, x2, y2, fill=SECOND_TILE_COLOR)
                self.rects[i].append(c)

    def getUserClick(self, event):
        x = int(self.canvasx(event.x) // SQUARE_SIZE)
        y = int(self.canvasy(event.y) // SQUARE_SIZE)

        if self.board[y][x] == self.player or self.board[y][x] == 0:
            print(self.player)
            if self.jump and len(self.checkForMoreJumps(self.currentTile[0], self.currentTile[1], [])) == 0:
                self.jump = False
                self.switchPlayer()
            elif not self.board[y][x] == 0:
                self.currentTile = (y, x)
                self.availableMoves = self.getValidMoves(y, x)
                self.createTiles()
                self.render()
                for (y, x) in self.availableMoves:
                    if self.isValidRow(y) and self.isValidCol(x):
                        self.itemconfig(self.rects[x][y], fill=HIGHLIGHTED_COLOR)
            else:
                if (y, x) in self.availableMoves:
                    if abs(y - self.currentTile[0]) == 1:
                        self.board[y][x] = 1 if self.player == 1 else 2
                        self.board[self.currentTile[0]][self.currentTile[1]] = 0
                        self.createTiles()
                        self.render()
                        self.availableMoves = []
                        self.currentTile = []
                        self.switchPlayer()
                    else:
                        self.jump = True
                        self.toDel.append(self.currentTile)
                        self.availableMoves = self.checkForMoreJumps(y, x, [])
                        self.board[y][x] = 1 if self.player == 1 else 2
                        self.board[self.currentTile[0]][self.currentTile[1]] = 0
                        self.board[(y + self.currentTile[0]) // 2][(x + self.currentTile[1]) // 2] = 0
                        self.currentTile = (y, x)
                        self.createTiles()
                        self.render()

    def getValidMoves(self, y, x):
        validMoves = []
        if self.player == 1:
            for move in self.moves[:2]:
                if self.isValidRow(y + move[0]) and self.isValidCol(x + move[1]):
                    if self.board[y + move[0]][x + move[1]] == 0:
                        validMoves.append((y + move[0], x + move[1]))
        else:
            for move in self.moves[2:]:
                if self.isValidRow(y + move[0]) and self.isValidCol(x + move[1]):
                    if self.board[y + move[0]][x + move[1]] == 0:
                        validMoves.append((y + move[0], x + move[1]))

        # validMoves.append((-1, -1))
        validMoves = self.checkForMoreJumps(y, x, validMoves)
        print(validMoves)
        return validMoves

    def checkForMoreJumps(self, y, x, validMoves):
        for move in self.moves:
            if self.isValidRow(y + move[0]) and self.isValidCol(x + move[1]):
                if self.board[y + move[0]][x + move[1]] != self.player and self.board[y + move[0]][x + move[1]] != 0:
                    if self.isValidRow(y + 2 * move[0]) and self.isValidCol(x + 2 * move[1]):
                        if self.board[y + 2 * move[0]][x + 2 * move[1]] == 0 and (
                                y + 2 * move[0], x + 2 * move[1]) not in validMoves:
                            if (y + 2 * move[0], x + 2 * move[1]) not in self.toDel:
                                validMoves.append((y + 2 * move[0], x + 2 * move[1]))
                            #self.checkForMoreJumps(y + 2 * move[0], x + 2 * move[1], validMoves)
                            # validMoves.append((-1, -1))
        return validMoves

    def switchPlayer(self):
        self.toDel = []
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def isValidRow(self, y):
        if 0 <= y < ROWS:
            return True
        return False

    def isValidCol(self, x):
        if 0 <= x < COLS:
            return True
        return False
