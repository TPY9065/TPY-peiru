'''
change FILENAME to the corresponding background music and put it with the py file in the same directory
'''

import pygame
from random import choice, randrange
from time import time

### screen parameter
SIZE = 20
BOARDERLINE_SIZE = 2
PIECE_SIZE = SIZE - 2 * BOARDERLINE_SIZE
WIDTH = 600
HEIGHT = 480
ROW = HEIGHT//SIZE
COL = WIDTH//SIZE//3
RESOLUTION = (WIDTH, HEIGHT)
CLK = pygame.time.Clock()
FPS = 25
TEMPLATE_R = 5
TEMPLATE_C = 5
BOARD_RESOLUTION = (TEMPLATE_R * SIZE, TEMPLATE_C * SIZE)
FILENAME = 'tetris.mid'

### color
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = ( 0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = ( 0, 155, 0)
LIGHTGREEN = ( 20, 175, 20)
BLUE = ( 0, 0, 155)
LIGHTBLUE = ( 20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)
BLANK_COLOR = (255, 255, 255, 0)

EMPTY = '.'
OCCUPIED = 'O'
LEFT = -1
RIGHT = +1
INVALID_POS = +2
LOWEST = +3
SCORES = 0
LEVEL = 1
lastFallTime = time()
lastLeft = time()
lastRight = time()
fallingFreq = 0
VOLUME = 0.05

### block shape
O_shape = [['.....',
            '.....',
            '.OO..',
            '.OO..',
            '.....']]

J_shape = [['.....',
            '.O...',
            '.OOO.',
            '.....',
            '.....'],
           
           ['.....',
            '..O..',
            '..O..',
            '.OO..',
            '.....'],
            
           ['.....',
            '.....',
            '.OOO.',
            '...O.',
            '.....'],
            
           ['.....',
            '..OO.',
            '..O..',
            '..O..',
            '.....']]

L_shape = [['.....',
            '...O.',
            '.OOO.',
            '.....',
            '.....'],
           
           ['.....',
            '.OO..',
            '..O..',
            '..O..',
            '.....'],
            
            ['.....',
            '.....',
            '.OOO.',
            '.O...',
            '.....'],
            
            ['.....',
            '..O..',
            '..O..',
            '..OO.',
            '.....']]

Z_shape = [['.....',
            '.OO..',
            '..OO.',
            '.....',
            '.....'],

           ['.....',
            '..O..',
            '.OO..',
            '.O...',
            '.....']]

S_shape = [['.....',
            '..OO.',
            '.OO..',
            '.....',
            '.....'],

           ['.....',
            '.O...',
            '.OO..',
            '..O..',
            '.....']]

I_shape = [['.....',
            '.....',
            '.OOOO',
            '.....',
            '.....'],

           ['..O..',
            '..O..',
            '..O..',
            '..O..',
            '.....']]

T_shape = [['.....',
            '..O..',
            '.OOO.',
            '.....',
            '.....'],

           ['.....',
            '..O..',
            '.OO..',
            '..O..',
            '.....'],
            
           ['.....',
            '.....',
            '.OOO.',
            '..O..',
            '.....'],
            
           ['.....',
            '..O..',
            '..OO.',
            '..O..',
            '.....']]


PIECE = {'O' : O_shape, 'L' : L_shape, 'J' : J_shape, 'Z' : Z_shape, 'S' : S_shape, 'I' : I_shape, 'T' : T_shape}

SYMBOL = ['O', 'L', 'J', 'Z', 'S', 'I', 'T']

COLOR_LIST = [GRAY, RED, LIGHTRED, GREEN, LIGHTGREEN, BLUE, LIGHTBLUE, YELLOW, LIGHTYELLOW]

PIECE_LIST = {'boardSurf': None, 'shapeChoice': None, 'rotationChoice': None, 'piece': None, 'boardRect': None, 'colorChoice': None}
NEXT_PIECE = {'boardSurf': None, 'shapeChoice': None, 'rotationChoice': None, 'piece': None, 'boardRect': None, 'colorChoice': None}

MAP_STATUS = []

MAP_INFO = []

MENU = {}
GAMEOVER = {}
STAT = {}

#FPS = int(input('Please input the FPS: '))
pygame.init()
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('Tetris')

def gameOptionSetUp():
    global MENU, STAT, GAMEOVER
    start = pygame.font.SysFont('arial', 64, True, False)
    startSurf = start.render('Start', True, BLACK)
    startRect = startSurf.get_rect()
    startRect.center = ((WIDTH//2, HEIGHT//3))
    MENU.update({'start': {'surf': startSurf, 'rect': startRect}})

    leave = pygame.font.SysFont('arial', 64, True, False)
    leaveSurf = leave.render('Exit', True, BLACK)
    leaveRect = leaveSurf.get_rect()
    leaveRect.center = ((WIDTH//2, HEIGHT//3*2))
    MENU.update({'exit': {'surf': leaveSurf, 'rect': leaveRect}})
    GAMEOVER.update({'exit': {'surf': leaveSurf, 'rect': leaveRect}})

    playAgain = pygame.font.SysFont('arial', 64, True, False)
    playAgainSurf = playAgain.render('Play Again', True, BLACK)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = ((WIDTH//2, HEIGHT//3))
    GAMEOVER.update({'playAgain': {'surf': playAgainSurf, 'rect': playAgainRect}})

    score = pygame.font.SysFont('arial', 32, True, False)
    scoreSurf = score.render('Scores: ' + str(SCORES), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = ((WIDTH//6, HEIGHT//4))
    STAT.update({'scores': {'surf': scoreSurf, 'rect': scoreRect, 'scores': SCORES}})

    level = pygame.font.SysFont('arial', 32, True, False)
    levelSurf = level.render('Level: ' + str(LEVEL), True, BLACK)
    levelRect = levelSurf.get_rect()
    levelRect.center = ((WIDTH//6, HEIGHT//4 + scoreRect.height * 2))
    STAT.update({'level': {'surf': levelSurf, 'rect': levelRect, 'level': LEVEL}})
    STAT['level']['surf'] = score.render('Level : ' + str(STAT['level']['level']), True, BLACK)

def showGameOverPage():
    global GAMEOVER, SCREEN
    for keys in GAMEOVER.keys():
        SCREEN.blit(GAMEOVER[keys]['surf'], GAMEOVER[keys]['rect'])

def showPage():
    gameOver = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
    gameOverSurf = gameOver.render('Game Over', True, BLACK)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = ((WIDTH//2, HEIGHT//2))

    SCREEN.blit(gameOverSurf, gameOverRect)

def showMenu():
    global MENU, SCREEN
    for keys in MENU.keys():
        SCREEN.blit(MENU[keys]['surf'], MENU[keys]['rect'])

def showStat():
    global STAT, SCREEN
    for keys in STAT.keys():
        SCREEN.blit(STAT[keys]['surf'], STAT[keys]['rect'])

def setUpScreen():
    global SCREEN
    for row in range(ROW):
        for col in range(COL + 1):
            x, y = boardCordToGlobalCord(col, row)
            pygame.draw.line(SCREEN, BLACK, (x, 0), (x, HEIGHT), BOARDERLINE_SIZE//2)
        pygame.draw.line(SCREEN, BLACK, (WIDTH//3, y), (WIDTH//3*2, y), BOARDERLINE_SIZE//2)

def pause():
    global SCREEN
    while True:
        drawAllBoard()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(0)


def resetMap():
    MAP_STATUS.clear()
    for i in range(ROW):
        MAP_STATUS.append([])
        MAP_INFO.append([])
        for j in range(COL):
            MAP_STATUS[i].append(EMPTY)
            MAP_INFO[i].append(WHITE)

def updateMap():
    global PIECE_LIST, MAP_STATUS, MAP_INFO
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    for i in range(TEMPLATE_R):
        for j in range(TEMPLATE_C):
            if (PIECE_LIST['piece'][i][j] == OCCUPIED):
                MAP_STATUS[row + i][col + j] = PIECE_LIST['piece'][i][j]
                MAP_INFO[row + i][col + j] = PIECE_LIST['colorChoice']

def globalCordToBoardCord(x, y):
    col = x//SIZE - COL
    row = y//SIZE
    return col, row

def pieceGeneration():
    currentPiece = {'boardSurf': None, 'shapeChoice': None, 'rotationChoice': None, 'piece': None, 'boardRect': None, 'colorChoice': None}

    shapeChoice = choice(SYMBOL)
    rotationChoice = randrange(len(PIECE[shapeChoice]))

    """ shapeChoice = 'I'
    rotationChoice = 1 """

    colorChoice = choice(COLOR_LIST)
    piece = PIECE[shapeChoice][rotationChoice]

    for i in range(TEMPLATE_R - 1, -1, -1):
        for j in range(TEMPLATE_C):
            if piece[i][j] == OCCUPIED:
                boardSurf = drawPiece(piece, colorChoice)
                boardRect = boardSurf.get_rect()
                boardRect.x, boardRect.y = boardCordToGlobalCord(COL//2 - 2, (-i - 1))
                currentPiece['boardSurf'] = boardSurf
                currentPiece['shapeChoice'] = shapeChoice
                currentPiece['rotationChoice'] = rotationChoice
                currentPiece['piece'] = piece
                currentPiece['boardRect'] = boardRect
                currentPiece['colorChoice'] = colorChoice

                return currentPiece

def drawPiece(piece, colorChoice):
    boardSurf = pygame.Surface(BOARD_RESOLUTION)
    boardSurf.fill(WHITE)
    boardSurf.set_colorkey(WHITE)
    for i in range(TEMPLATE_R):
        for j in range(TEMPLATE_C):
            if piece[i][j] == OCCUPIED:
                x, y = boardCordToGlobalCord(j - COL, i)
                pygame.draw.rect(boardSurf, BLACK, (x, y, SIZE, SIZE), BOARDERLINE_SIZE)
                pygame.draw.rect(boardSurf, colorChoice, (x + BOARDERLINE_SIZE, y + BOARDERLINE_SIZE, PIECE_SIZE, PIECE_SIZE))
    return boardSurf

def pieceRotation(dir_pressed):
    global PIECE_LIST

    x = PIECE_LIST['boardRect'].x
    y = PIECE_LIST['boardRect'].y

    PIECE_LIST['rotationChoice'] = (PIECE_LIST['rotationChoice'] + 1) % (len(PIECE[PIECE_LIST['shapeChoice']]))
    PIECE_LIST['piece'] = PIECE[PIECE_LIST['shapeChoice']][PIECE_LIST['rotationChoice']]
    PIECE_LIST['boardSurf'] = drawPiece(PIECE_LIST['piece'], PIECE_LIST['colorChoice'])
    PIECE_LIST['boardRect'] = PIECE_LIST['boardSurf'].get_rect()
    PIECE_LIST['boardRect'].x = x
    PIECE_LIST['boardRect'].y = y

    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)

    dir, diffY = checkPosition(dir_pressed, col, row)

    if (dir == INVALID_POS):
        PIECE_LIST['rotationChoice'] = (PIECE_LIST['rotationChoice'] - 1) % (len(PIECE[PIECE_LIST['shapeChoice']]))
        PIECE_LIST['piece'] = PIECE[PIECE_LIST['shapeChoice']][PIECE_LIST['rotationChoice']]
        PIECE_LIST['boardSurf'] = drawPiece(PIECE_LIST['piece'], PIECE_LIST['colorChoice'])
        PIECE_LIST['boardRect'] = PIECE_LIST['boardSurf'].get_rect()
        PIECE_LIST['boardRect'].x = x
        PIECE_LIST['boardRect'].y = y
        return

    if (dir == RIGHT):
        PIECE_LIST['boardRect'].x = shiftRight(dir_pressed, col) * SIZE
    elif (dir == LEFT):
        PIECE_LIST['boardRect'].x = shiftLeft(dir_pressed, col) * SIZE
    else:
        PIECE_LIST['boardRect'].x = x

    if (diffY <= 0):
        PIECE_LIST['boardRect'].y = y + (diffY * SIZE)
    else:
        PIECE_LIST['boardRect'].y = y

def checkPosition(dir_pressed, col, row):
    global PIECE_LIST
    x = []
    for i in range(TEMPLATE_R):
        for j in range(TEMPLATE_C):
            if (PIECE_LIST['piece'][i][j] == OCCUPIED):
                x.append(j)

    enoughSpace, diffY = isEnoughSpace(dir_pressed, row, col)

    if enoughSpace:
        if ((col + min(x) + dir_pressed >= 0)and(col + max(x) + dir_pressed < COL)):
            return 0, diffY
        elif (col + min(x) + dir_pressed < 0):
            return RIGHT, diffY
        elif (col + max(x) + dir_pressed >= COL):
            return LEFT, diffY
    else:
        return INVALID_POS, diffY

def isEnoughSpace(dir, row, col):
    cord = []
    for i in range(TEMPLATE_R):
        for j in range(TEMPLATE_C):
            if (PIECE_LIST['piece'][i][j] == OCCUPIED):
                cord.append({'row': i, 'col': j})

    occupiedY = ROW - 1

    for i in range(ROW):
        if MAP_STATUS[i][col - 2 + cord[len(cord) - 1]['col']] == OCCUPIED:
            occupiedY = i
            break

    highestY = row + cord[0]['row']
    lowestY = row + cord[len(cord) - 1]['row']
    diffY = occupiedY - lowestY

    for i in range(len(cord)):
        r = row + cord[i]['row']
        c = col + cord[i]['col'] + dir
        if (c >= 0)and(c < COL)and(highestY >= 0)and(lowestY < ROW):
            if (MAP_STATUS[r][c] == OCCUPIED):
                return False, diffY
        elif (highestY < 0):
            if (r >= 0):
                if (MAP_STATUS[r][c] == OCCUPIED):
                    return False, diffY
        elif (lowestY >= ROW):
            if (MAP_STATUS[r + diffY][c] == OCCUPIED):
                return False, diffY
    return True, diffY

def shiftRight(dir_pressed, col):
    for i in range(TEMPLATE_C):
        for j in range(TEMPLATE_R):
            if PIECE_LIST['piece'][j][i] == OCCUPIED:
                x = COL - i
                return x

def shiftLeft(dir_pressed, col):
    for i in range(TEMPLATE_C - 1, -1, -1):
        for j in range(TEMPLATE_R - 1, -1, -1):
            if PIECE_LIST['piece'][j][i] == OCCUPIED:
                x = COL * 2 - 1 - i - dir_pressed
                return x

def moveLeft():
    global PIECE_LIST
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    if isValidPosition(LEFT, row, col - 1):
        col -= 1
    PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y = boardCordToGlobalCord(col, row)

def moveRight():
    global PIECE_LIST
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    if isValidPosition(RIGHT, row, col + 1):
        col += 1
    PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y = boardCordToGlobalCord(col, row)

def boardCordToGlobalCord(col, row):
    x = (col + COL) * SIZE
    y = row * SIZE
    return x, y

def falling(key_pressed = False):
    global PIECE_LIST, lastFallTime
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    if isLanded():
        return True

    if not(time() - lastFallTime < fallingFreq):
        row += 1
        PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y = boardCordToGlobalCord(col, row)
        lastFallTime = time()
    
    if key_pressed:
        row += 1
        PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y = boardCordToGlobalCord(col, row)       

    return False

def updateFallingFreq():
    global STAT
    fallingFreq = 0.75 - (STAT['level']['level'] * 0.05)
    if fallingFreq < 0:
        fallingFreq = 0
    return fallingFreq

def isLanded():
    global PIECE_LIST
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    for i in range(TEMPLATE_R - 1, -1, -1):
        for j in range(TEMPLATE_C):
            if (PIECE_LIST['piece'][i][j] == OCCUPIED):
                if (row + i + 1 >= ROW)or(not(isValidPosition(0, row + i + 1, col + j))):
                    return True
    return False

def isValidPosition(dir, row, col):
    global PIECE_LIST, MAP_STATUS
    if dir == LEFT:
        for i in range(TEMPLATE_C):
            for j in range(TEMPLATE_R):
                if PIECE_LIST['piece'][j][i] == OCCUPIED:
                    if (col + i < 0):
                        return False
                    elif (row + i < 0):
                        return True
                    elif (MAP_STATUS[row + j][col + i] == OCCUPIED):
                        return False
    elif dir == RIGHT:
        for i in range(TEMPLATE_C - 1, -1, -1):
            for j in range(TEMPLATE_R - 1, -1, -1):
                if PIECE_LIST['piece'][j][i] == OCCUPIED:
                    if (col + i >= COL):
                        return False
                    elif (row + i < 0):
                        return True
                    elif (MAP_STATUS[row + j][col + i] == OCCUPIED):
                        return False
    else:
        if (row < 0):
            return True
        elif MAP_STATUS[row][col] == OCCUPIED:
            return False

    return True

def control():
    global PIECE_LIST, SCREEN, lastLeft, lastRight

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_LEFT]:
        if (time() - lastLeft > 0.1):
            col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
            if isValidPosition(LEFT, row, col - 1):
                moveLeft()
                lastLeft = time()
    elif key_pressed[pygame.K_RIGHT]:
        if (time() - lastRight > 0.1):
            col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
            if isValidPosition(RIGHT, row, col + 1):
                moveRight()
                lastRight = time()
    elif key_pressed[pygame.K_DOWN]:
        LANDED = falling(True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toBottom()
            elif event.key == pygame.K_UP:
                pieceRotation(0)
            elif event.key == pygame.K_p:
                pause()

def toBottom():
    global PIECE_LIST, MAP_STATUS
    col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
    boardCol = []
    maxRow = 0
    for i in range(TEMPLATE_R - 1, -1, -1):
        for j in range(TEMPLATE_C):
            if (PIECE_LIST['piece'][i][j] == OCCUPIED):
                if not((col + j) in boardCol):
                    boardCol.append(col + j)
                if (i > maxRow):
                    maxRow = i

    availableRow = ROW - 1
    count = 0
    
    for j in boardCol:
        for i in range(ROW - 1):
            if (MAP_STATUS[i + 1][j] == OCCUPIED)and(MAP_STATUS[i][j] == EMPTY):
                if (i < availableRow):
                    availableRow = i
                    count += 1
                    break

    x, y = boardCordToGlobalCord(col, (availableRow - maxRow))
    PIECE_LIST['boardRect'].x = x
    PIECE_LIST['boardRect'].y = y

def drawAllBoard():
    global MAP_STATUS, MAP_INFO, SCREEN
    for row in range(ROW):
        for col in range(COL):
            if (MAP_STATUS[row][col] == OCCUPIED):
                x, y = boardCordToGlobalCord(col, row)
                pygame.draw.rect(SCREEN, BLACK, (x, y, SIZE, SIZE), BOARDERLINE_SIZE)
                pygame.draw.rect(SCREEN, MAP_INFO[row][col], (x + BOARDERLINE_SIZE, y + BOARDERLINE_SIZE, PIECE_SIZE, PIECE_SIZE))

""" def writeToMapFile(filename = "MAP_STATUS.txt"):
    f = open(filename, "w", encoding='ascii')
    for i in range(ROW):
        for j in range(COL):
            f.write(MAP_STATUS[i][j] + "\t")
        f.write("\n")
    f.close()

def writeColorFile(filename = "MAP_INFO.txt"):
    f = open(filename, "w", encoding='ascii')
    for i in range(ROW):
        exist = False
        for j in range(COL):
            if (MAP_INFO[i][j] != WHITE):
                f.write(str(MAP_INFO[i][j]) + "\t" + "row: " + str(i) + " col: " + str(j) + "\n")
                exist = True
        if exist:
            f.write("\n")
    f.close() """


def lineFinished(row):
    global MAP_STATUS
    for col in range(COL):
        if (MAP_STATUS[row][col] == EMPTY):
            return False
    return True

def writeGameStatus():
    f = open('GameStatus.txt', "w", encoding='ascii')
    for row in range(ROW):
        for col in range(COL):
            if (MAP_STATUS[row][col] == EMPTY):
                f.write('row: ' + str(row) + ' col: ' + str(col) + ' is empty' + '\n')
    f.close()    

def resetRow(row):
    global MAP_STATUS, MAP_INFO
    MAP_STATUS[row].clear()
    MAP_INFO[row].clear()
    for i in range(COL):
        MAP_STATUS[row].append(EMPTY)
        MAP_INFO[row].append(WHITE)


def clearLine(row):
    for i in range(row, 0, -1):
        MAP_STATUS[i] = MAP_STATUS[i - 1]
        MAP_INFO[i] = MAP_INFO[i - 1]

def isOnButton(gameOver):
    x, y = pygame.mouse.get_pos()
    if gameOver:
        for keys in GAMEOVER.keys():
            if GAMEOVER[keys]['rect'].collidepoint(x, y):
                pygame.draw.rect(SCREEN, RED, GAMEOVER[keys]['rect'], 5)
                return True
        return False
    else:
        for keys in MENU.keys():
            if MENU[keys]['rect'].collidepoint(x, y):
                pygame.draw.rect(SCREEN, RED, MENU[keys]['rect'], 5)
                return True
        return False

def startIsClicked(gameOver):
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        if gameOver:
            for keys in GAMEOVER.keys():
                if GAMEOVER[keys]['rect'].collidepoint(x, y):
                    if keys == 'playAgain':
                        return True
        else:
            for keys in MENU.keys():
                if MENU[keys]['rect'].collidepoint(x, y):
                    if keys == 'start':
                        return True
    return False

def exitIsClicked(gameOver):
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        if gameOver:
            for keys in GAMEOVER.keys():
                if GAMEOVER[keys]['rect'].collidepoint(x, y):
                    if keys == 'exit':
                        return True
        else:
            for keys in MENU.keys():
                if MENU[keys]['rect'].collidepoint(x, y):
                    if keys == 'exit':
                        return True
    return False   

def main():
    gameOptionSetUp()
    while True:
        SCREEN.fill(WHITE)
        showMenu()
        if isOnButton(False):
            if startIsClicked(False):
                break
            if exitIsClicked(False):
                pygame.quit()
                exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.update()
    start()

def isGameOver():
    global PIECE_LIST
    for i in range(TEMPLATE_R):
        for j in range(TEMPLATE_C):
            if PIECE_LIST['piece'][i][j] == OCCUPIED:
                col, row = globalCordToBoardCord(PIECE_LIST['boardRect'].x, PIECE_LIST['boardRect'].y)
                if (row + i < 0):
                    return True               
                return False
    


def scoreUpdate(count):
    global STAT
    if count <= 1:
        STAT['scores']['scores'] += 100 * count
    elif count == 2:
        STAT['scores']['scores'] += 100 * 3
    elif count == 3:
        STAT['scores']['scores'] += 100 * 5
    else:
        STAT['scores']['scores'] += 100 * 8

    score = pygame.font.SysFont('freesansbold.ttf', 32, True, False)
    STAT['scores']['surf'] = score.render('Scores: ' + str(STAT['scores']['scores']), True, BLACK)
    STAT['scores']['rect'] = STAT['scores']['surf'].get_rect()
    STAT['scores']['rect'].center = ((WIDTH//6, HEIGHT//4))

def levelUpdate():
    global STAT
    available = STAT['scores']['scores'] // (500 * STAT['level']['level'])
    if available > 1:
        STAT['level']['level'] += 1

    level = pygame.font.SysFont('freesansbold.ttf', 32, True, False)
    STAT['level']['surf'] = level.render('Level : ' + str(STAT['level']['level']), True, BLACK)
    STAT['level']['rect'] = STAT['level']['surf'].get_rect()
    STAT['level']['rect'].center = ((WIDTH//6, HEIGHT//4 + STAT['scores']['rect'].height * 2))

def start():
    ### screen initialize
    global PIECE_LIST, lastFallTime, fallingFreq, FILENAME, VOLUME
    resetMap()
    LANDED = False
    NEXT_PIECE = pieceGeneration()
    fallingFreq = updateFallingFreq()
    pygame.mixer_music.load(FILENAME)
    pygame.mixer_music.set_volume(VOLUME)
    pygame.mixer_music.play()
    while True:
        PIECE_LIST = NEXT_PIECE
        NEXT_PIECE = pieceGeneration()
        lastFallTime = time()
        while not(LANDED):
            SCREEN.fill(WHITE)
            setUpScreen()
            showStat()
            drawAllBoard()
            SCREEN.blit(NEXT_PIECE['boardSurf'], (WIDTH//6*5 - 5*SIZE//2, HEIGHT//4 + HEIGHT//8, NEXT_PIECE['boardRect'].width, NEXT_PIECE['boardRect'].height))
            SCREEN.blit(PIECE_LIST['boardSurf'], PIECE_LIST['boardRect'])
            control()
            LANDED = falling()
            CLK.tick(FPS)
            pygame.display.update()
        
        LANDED = False

        if isGameOver():
            gameOver = True
            SCREEN.fill(WHITE)
            showPage()
            pygame.display.update()
            pygame.time.wait(1000)
            while gameOver:
                backgroundMusic.stop()
                SCREEN.fill(WHITE)
                showGameOverPage()
                if isOnButton(gameOver):
                    if startIsClicked(gameOver):
                        gameOver = False
                        break
                    elif exitIsClicked(gameOver):
                        pygame.quit()
                        exit(0)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                pygame.display.update()

            if not(gameOver):
                break

        updateMap()
        #writeGameStatus()
        row = ROW - 1
        count = 0
        while (row > 0):
            if lineFinished(row):
                clearLine(row)
                row += 1
                count += 1
            row -= 1

        scoreUpdate(count)
        levelUpdate()
        fallingFreq = updateFallingFreq()
        #writeToMapFile()
        #writeColorFile()
        pygame.display.update()

    main()

if __name__ == '__main__':
    main()
