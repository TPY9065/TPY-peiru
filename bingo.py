import pygame
import random
from pygame import *

HEIGHT = 300
WIDTH  = 300
RESOLUTION = (HEIGHT,WIDTH)
BLACK   = (  0,  0,  0)
WHITE   = (255,255,255)
AIRBLUE = (120,255,255)
ROW = HEIGHT//100
COL = WIDTH//100

RC_COR = [0, 0]                                 ### player's last box choice

PLAYER_OR_AI_WIN = [False, False]               ### 0 = player      1 = AI

STAT = [[0,0,0],                                ### map status
        [0,0,0],
        [0,0,0]]

END = [False]                                     ### the game status

pygame.init()
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Bingo")
SCREEN.fill(WHITE)

def reset():
    RC_COR[0] = 0
    RC_COR[1] = 0
    for row in range(ROW):
        for col in range(COL):
            STAT[row][col] = 0
    PLAYER_OR_AI_WIN[0] = False
    PLAYER_OR_AI_WIN[1] = False
    SCREEN.fill(WHITE)
    END[0] = False
    random.seed()

### check row condition
def row_win(row, col):
    if STAT[row-1][col] == STAT[row][col] and STAT[row-2][col] == STAT[row][col]:
        return True
    else:
        return False

### check col condition
def col_win(row, col):
    if STAT[row][col-1] == STAT[row][col] and STAT[row][col-2] == STAT[row][col]:
        return True
    else:
        return False

### check oblique condition
def oblique_win():
    if STAT[0][0] == STAT[1][1] and STAT[1][1] == STAT[2][2] or STAT[0][2] == STAT[1][1] and STAT[1][1] == STAT[2][0]:
        return True
    else:
        return False

### check winning condition
def finish():
    zero_exist = False
    for row in range(ROW):
        for col in range(COL):
            if STAT[row][col] != 0:
                if row_win(row, col) or col_win(row, col):       ### if row or col finished
                    if STAT[row][col] == 1:         ### if player win
                        PLAYER_OR_AI_WIN[0] = True
                    else:                           ### if AI win
                        PLAYER_OR_AI_WIN[1] = True
                    END[0] = True
                    return True
            else:
                zero_exist = True
    if oblique_win() and STAT[1][1] != 0:            ### if oblique finished
        if STAT[1][1] == 1:         ### if player win
            PLAYER_OR_AI_WIN[0] = True
        else:                           ### if AI win
            PLAYER_OR_AI_WIN[1] = True
        END[0] = True
        return True
    elif not(zero_exist):
        END[0] = True
        return True
    else:
        END[0] = False
        return False

### init the game
def init():
    for i in range(ROW):
        pygame.draw.line(SCREEN, BLACK, (i*100, 0), (i*100, 300))
    for i in range(COL):
        pygame.draw.line(SCREEN, BLACK, (0, i*100), (300, i*100))

### draw circle when player click the mouse button
def Draw():
    (x,y) = pygame.mouse.get_pos()
    col = x//100
    row = y//100
    while STAT[row][col] != 0:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                (x,y) = pygame.mouse.get_pos()
                col = x//100
                row = y//100
    RC_COR[0] = row
    RC_COR[1] = col
    STAT[row][col] = 1
    x = col*100+50
    y = row*100+50
    pygame.draw.circle(SCREEN, BLACK, (x,y), 25, 1)
    finish()

def need_col_blocking(row, col):           ### check col blocking
    if STAT[row-1][col] == 1 or STAT[row-2][col] == 1:
        if STAT[row-1][col] == 1 and STAT[row-2][col] == 0:           ### check upper is needed to block and empty space is exist
            STAT[row-2][col] = 2
            pygame.draw.rect(SCREEN, BLACK, (col*100+25, (row-2)%ROW*100+25, 50, 50), 1)
            return True
        elif STAT[row-2][col] == 1 and STAT[row-1][col] == 0:         ### check lower is needed to block and empty space is exist
            STAT[row-1][col] = 2
            pygame.draw.rect(SCREEN, BLACK, (col*100+25, (row-1)%ROW*100+25, 50, 50), 1)
            return True
    return False                            ### space is not enough


def need_row_blocking(row, col):            ### check row blocking
    if STAT[row][col-1] == 1 or STAT[row][col-2] == 1:
        if STAT[row][col-2] == 1 and STAT[row][col-1] == 0:           ### check next col is needed to block or previous is needed
            STAT[row][col-1] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col-1)%COL*100+25, row*100+25, 50, 50), 1)
            return True
        elif STAT[row][col-1] == 1 and STAT[row][col-2] == 0:
            STAT[row][col-2] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col-2)%COL*100+25, row*100+25, 50, 50), 1)
            return True
    return False                            ### space is not enough


def need_oblique_blocking(row, col):
    if STAT[row-1][col-1] == 1 or STAT[row+1][col+1] == 1:
        if STAT[row-1][col-1] == 1 and STAT[row+1][col+1] == 0:           ### check blocking is needed and space exist
            STAT[row+1][col+1] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col+1)*100+25, (row+1)*100+25, 50, 50), 1)
            return True
        elif STAT[row+1][col+1] == 1 and STAT[row-1][col-1] == 0:
            STAT[row-1][col-1] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col-1)*100+25, (row-1)*100+25, 50, 50), 1)
            return True
    if STAT[row-1][col+1] == 1 or STAT[row+1][col-1] == 1:
        if STAT[row-1][col+1] == 1 and STAT[row+1][col-1] == 0:           ### check blocking is needed and space exist
            STAT[row+1][col-1] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col-1)*100+25, (row+1)*100+25, 50, 50), 1)
            return True
        elif STAT[row+1][col-1] == 1 and STAT[row-1][col+1] == 0:
            STAT[row-1][col+1] = 2
            pygame.draw.rect(SCREEN, BLACK, ((col+1)*100+25, (row-1)*100+25, 50, 50), 1)
            return True
    return False                            ### space is not enough

def need_block(row, col):               ### is blocking needed
    if need_col_blocking(row, col) or need_row_blocking(row, col):    ### check whether row or col block is needed
        return True
    elif (row + col)%2 == 0 and need_oblique_blocking(1, 1):              ### oblique blocking is needed
        return True                     ### oblique block is needed
    else:
        return False                    ### blocking is not needed

### AI's action
def AI(r, c):
    if not(need_block(r, c)):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        while True:
            if STAT[row][col] == 0:
                STAT[row][col] = 2
                pygame.draw.rect(SCREEN, BLACK, (col*100+25, row*100+25, 50, 50), 1)
                break;
            else:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
    finish()

### check the game statistic is working
def check():
        for i in range(ROW):
            for j in range(COL):
                print(STAT[i][j], end = '')
            print()
        print()
        pygame.time.wait(3000)

def show(text):
    SCREEN.fill(WHITE)
    largeText = pygame.font.SysFont('arial', 50)
    TextSurface = largeText.render(text, True, BLACK)
    TextRect = TextSurface.get_rect()
    TextRect.center = (WIDTH/2, HEIGHT/2)
    SCREEN.blit(TextSurface, TextRect)
    pygame.display.update()
    pygame.time.wait(3000)

def option():
    Selected = False
    while not(Selected):

        SCREEN.fill(WHITE)

        ### setting up the Play Again button
        PlayAgain = pygame.font.SysFont('arial', 50)
        PlayAgainSurface = PlayAgain.render('Play Again', True, BLACK)
        PlayAgainRect = PlayAgainSurface.get_rect()
        PlayAgainRect.center = (WIDTH/2, HEIGHT/2-50)

        ### setting up the Exit button
        Back = pygame.font.SysFont('arial', 50)
        BackSurface = Back.render('Exit', True, BLACK)
        BackRect = BackSurface.get_rect()
        BackRect.center = (WIDTH/2, HEIGHT/2+50)

        ### get the xy-cor of Exit button
        Back_x = BackRect.x
        Back_y = BackRect.y
        Back_w = BackRect.w
        Back_h = BackRect.h

        ### get the xy-cor of Play button
        Play_x = PlayAgainRect.x
        Play_y = PlayAgainRect.y
        Play_w = PlayAgainRect.w
        Play_h = PlayAgainRect.h

        SCREEN.blit(PlayAgainSurface, PlayAgainRect)
        SCREEN.blit(BackSurface, BackRect)

        ### show highlighted box when move to the corresponding button
        (x, y) = pygame.mouse.get_pos()
        if PlayAgainRect.collidepoint((x, y)):
            pygame.draw.rect(SCREEN, AIRBLUE, (Play_x-5, Play_y-5, Play_w+10, Play_h+10), 5)
        elif BackRect.collidepoint((x, y)):
            pygame.draw.rect(SCREEN, AIRBLUE, (Back_x-5, Back_y-5, Back_w+10, Back_h+10), 5)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if PlayAgainRect.collidepoint((x, y)):
                    Selected = True
                    reset()
                elif BackRect.collidepoint((x, y)):
                    Selected = True


### main program
def main():
    reset()
    while not(END[0]):
        init()
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit
                exit(0)
            elif event.type == MOUSEBUTTONUP:
                Draw()
                pygame.display.update()
                if finish():
                    pygame.time.wait(1000)
                    if PLAYER_OR_AI_WIN[0]:
                        show("YOU WIN")
                    else:
                        show("DRAW")
                    option()
                    break
                AI(RC_COR[0], RC_COR[1])
                pygame.display.update()
                if finish():
                    pygame.time.wait(1000)
                    if PLAYER_OR_AI_WIN[1]:
                        show("YOU LOSE")
                    else:
                        show("DRAW")
                    option()
                    break
        pygame.display.update()
        #check()

if __name__ == '__main__':
    main()