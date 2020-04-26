import pygame as pg
import sys, time

from pygame.locals import *

# Global Variables
winner = None
XO = 'x'
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)

board = [[None] * 3, [None] * 3, [None] * 3]

# initialize game window
pg.init()
fps = 30
Clock = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

opening = pg.image.load("img/red.png")
x_img = pg.image.load("img/cross.png")
o_img = pg.image.load("img/zero.png")

# Scaling
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))


def gameOpening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    # vertical lines
    pg.draw.line(screen, line_color,
                 (width / 3, 0),
                 (width / 3, height),
                 7)
    pg.draw.line(screen, line_color,
                 (width / 3 * 2, 0),
                 (width / 3 * 2, height),
                 7)

    # Horizontal lines
    pg.draw.line(screen, line_color,
                 (0, height / 3),
                 (width, height / 3),
                 7)
    pg.draw.line(screen, line_color,
                 (0, height / 3 * 2),
                 (width, height / 3 * 2),
                 7)
    draw_status()


def draw_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + "won"
    if draw:
        message = "Game Draw"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, white)

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    # text_rect = text.get_rect()
    screen.blit(text, ((width / 2), (500 - 50)))
    pg.display.update()


def check_win():
    global board, winner, draw

    for row in range(0, 3):
        if ((board[row][0]) == board[row][1] == board[row][2]) and (board[row][0] is not None):
            # Row won
            winner = board[row][0]
            pg.draw.line(screen,
                         (255, 0, 0),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6),
                         4)
            break

    for col in range(0, 3):
        if ((board[0][col]) == board[1][col] == board[2][col]) and (board[0][col] is not None):
            # col won
            winner = board[0][col]
            pg.draw.line(screen,
                         (255, 0, 0),
                         (0, (col + 1) * height / 3 - height / 6),
                         (width, (col + 1) * height / 3 - height / 6),
                         4)
            break

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70),
                     (50, 50),
                     (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen,
                     (250, 70, 70),
                     (350, 50),
                     (50, 350), 4)
    if all([all(row) for row in board]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):
    global board, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30
    board[row - 1][col - 1] = XO
    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = "o"
    else:
        screen.blit(o_img, (posy, posx))
        XO = "x"
    pg.display.update()
    print(posx, posy)
    print(board)


def userClick():
    x, y = pg.mouse.get_pos()

    # Declaring selected col
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # declaring selected row
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    print(row, col)

    if row and col and board[row - 1][col - 1] is None:
        global XO

        drawXO(row, col)
        check_win()


def resetGame():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    gameOpening()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


gameOpening()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            userClick()
            if winner or draw:
                resetGame()
    pg.display.update()
    Clock.tick(fps)
