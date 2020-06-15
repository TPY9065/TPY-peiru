'''
A snake game developed with pygame, changing the variable PLAYER_COLOR can change the color of player, 
also the three comment line 310-312 are used to set the background music of the game. 
Just save the music file in the same directory of the snake file and change the name in line 310
'''
import pygame
import random
import math
from pygame import*
from math import*

### game parameter
HEIGHT = 500
WIDTH  = 500
SIDE = 20                 ### preset 20
ROW    = HEIGHT//SIDE     ### 25
COL    = WIDTH//SIDE      ### 25
RESOLUTION = (WIDTH, HEIGHT)
clock = pygame.time.Clock()
FPS   = 8
mark = 0

### color code
BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)
PINK  = (244,184,215)
DARK_GREEN  = (88,222,98)
PALE_GREEN = (13,247,45)
color_code = [DARK_GREEN, PALE_GREEN]
PLAYER_COLOR = PINK

### screen setting
pygame.init()
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Snake")

### position of snake's body part
snake_position = []

### Title
Title = pygame.font.SysFont('freesansbold.ttf', 144, True, False)
Title_Surf = Title.render('Snake', True, BLACK)
Title_Rect = Title_Surf.get_rect()
Title_Rect.center = (floor(WIDTH/2), floor(HEIGHT/4))

### Start Game
Start_Game = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
Start_Game_Surf = Start_Game.render('Start Game', True, BLACK)
Start_Game_Rect = Start_Game_Surf.get_rect()
Start_Game_Rect.center = (floor(WIDTH/2), floor(HEIGHT/2))

### Exit
Exit = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
Exit_Surf = Exit.render('Exit', True, BLACK)
Exit_Rect = Exit_Surf.get_rect()
Exit_Rect.center = (floor(WIDTH/2), floor(HEIGHT/4*3))

### Game Over
End = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
End_Surf = End.render('Game Over', True, WHITE)
End_Rect = End_Surf.get_rect()
End_Rect.center = (floor(WIDTH/2), floor(HEIGHT/3))

### Mark
Mark = pygame.font.SysFont('freesansbold.ttf', 28, True, False)
Mark_Surf = Mark.render('Mark : ', True, WHITE)
Mark_Rect = Mark_Surf.get_rect()
Mark_Rect.topleft = (floor(WIDTH/5*4), 0)

### Record
Record = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
Record_Surf = Record.render('Your mark is '+str(mark), True, WHITE)
Record_Rect = Record_Surf.get_rect()
Record_Rect.center = (floor(WIDTH/2), floor(HEIGHT/3*2))

### Play Again
Play_Again = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
Play_Again_Surf = Play_Again.render('Play Again?', True, WHITE)
Play_Again_Rect = Play_Again_Surf.get_rect()
Play_Again_Rect.center = (floor(WIDTH/2), floor(HEIGHT/3))

### Yes
Yes = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
Yes_Surf = Yes.render('Yes', True, WHITE)
Yes_Rect = Yes_Surf.get_rect()
Yes_Rect.center = (floor(WIDTH/3), floor(HEIGHT/3*2))

### No
No = pygame.font.SysFont('freesansbold.ttf', 64, True, False)
No_Surf = No.render('No', True, WHITE)
No_Rect = No_Surf.get_rect()
No_Rect.center = (floor(WIDTH/3*2), floor(HEIGHT/3*2))

### movement and its direction      0:stop    1:up    2:down    3:left    4:right
step = 1
movement = {'NONE':(0, 0), 'UP':(0,-step), 'DOWN':(0,step), 'LEFT':(-step,0), 'RIGHT':(step,0)}

### mouse position
(x, y) = (0, 0)

### player
class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        ###constructor
        super().__init__()

        ###parameter
        self.image = pygame.Surface((SIDE, SIDE))
        self.image.fill(BLACK)
        self.dir = 'NONE'

        ###draw the snake
        pygame.draw.rect(self.image, color, (0, 0, SIDE, SIDE))
        self.rect = self.image.get_rect()

    def move(self, dir):
        self.rect.x = (self.rect.x//SIDE+dir[0])*SIDE
        self.rect.y = (self.rect.y//SIDE+dir[1])*SIDE

    def update(self):
        self.move(movement[self.dir])

    def re_generate(self, s, BLANK_POSITION = []):
        if BLANK_POSITION == []:
            self.rect.x = random.randrange(SIDE, WIDTH-SIDE, SIDE)
            self.rect.y = random.randrange(SIDE, WIDTH-SIDE, SIDE)
        else:
            self.rect.topleft = random.choice(BLANK_POSITION)

### check in map
    def inbox(self):
        if self.rect.x == 0 or self.rect.x == WIDTH-SIDE or self.rect.y == 0 or self.rect.y == HEIGHT-SIDE:
            return False
        else:
            return True

block_list = pygame.sprite.Group()
snake_list = pygame.sprite.Group()

### map status to check which block is occupied
MAP_STATUS = []
BLANK_POSITION = []
BLANK = '.'
OCCUPIED = 'O'

### initialize the map status
def init(BLANK_POSITION):
    BLANK_POSITION.clear()

    MAP = []
    for i in range(ROW):
        MAP.append([BLANK]*COL)

    return MAP

### create fruit
fruit = Block(RED)
fruit.re_generate(snake_position)

### create player
snake = Block(PLAYER_COLOR)
snake.rect.x = COL//2*SIDE
snake.rect.y = ROW//2*SIDE

### add to sprite group
block_list.add(fruit)
block_list.add(snake)
snake_list.add(snake)

### check the game state
GameStart = False
Exit_Game = False

### building map
def build():
    states = 0
    box = 0
    for row in range(ROW):
        for col in range(COL):
            if row == 0 or col == 0 or row == ROW-1 or col == COL-1:
                pygame.draw.rect(SCREEN, BLACK, (row*SIDE, col*SIDE, SIDE, SIDE))
            elif col%2 == 0 and box%2 == 0:
                pygame.draw.rect(SCREEN, color_code[states], (row*SIDE, col*SIDE, SIDE, SIDE))
            else:
                pygame.draw.rect(SCREEN, color_code[(states+1)%2], (row*SIDE, col*SIDE, SIDE, SIDE))
        states = (states+1)%2
        box *= -1

###update snake position
def update():
    for i in range(len(snake_position)-1, 0, -1):
        snake_position[i]['x'] = snake_position[i-1]['x']
        snake_position[i]['y'] = snake_position[i-1]['y']
        snake_position[i]['d'] = snake_position[i-1]['d']
    snake_position[0]['x'] = snake.rect.x
    snake_position[0]['y'] = snake.rect.y
    snake_position[0]['d'] = snake.dir

    i = 0;
    for s in snake_list:
        s.rect.x = snake_position[i]['x']
        s.rect.y = snake_position[i]['y']
        s.dir = snake_position[i]['d']
        i += 1

### add new body part
def add_body():
    tail = len(snake_position)-1
    body = Block(PLAYER_COLOR)
    body.rect.x = snake_position[tail]['x']
    body.rect.y = snake_position[tail]['y']
    body.dir    = snake_position[tail]['d']
    new = {'x':body.rect.x, 'y':body.rect.y, 'd': body.dir}
    snake_position.append(new)
    block_list.add(body)
    snake_list.add(body)

### check gameover
def touch_itself():
    length = len(snake_position)
    ### check the head touch the body
    if length > 1:
        for i in range(length):
            for j in range(i, length-1):
                if snake_position[i]['x'] == snake_position[j+1]['x'] and snake_position[i]['y'] == snake_position[j+1]['y']:
                    return True
    return False

def GameOver_Page():
    Record_Surf = Record.render('Your mark is '+str(mark), True, WHITE)
    SCREEN.fill(BLACK)
    SCREEN.blit(End_Surf, End_Rect)
    SCREEN.blit(Record_Surf, Record_Rect)
    pygame.display.update()

def ShowMarks():
    Mark_Surf = Mark.render('Mark : '+ str(mark), True, WHITE)
    Record_Rect.center = (WIDTH/2, HEIGHT/3*2)
    SCREEN.blit(Mark_Surf, Mark_Rect)

def PlayAgain():
    ### wait until players make a desicion
    (x,y) = (0,0)
    SCREEN.fill(BLACK)
    SCREEN.blit(Play_Again_Surf, Play_Again_Rect)
    SCREEN.blit(Yes_Surf, Yes_Rect)
    SCREEN.blit(No_Surf, No_Rect)
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                (x,y) = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if Yes_Rect.collidepoint((x,y)):
                    return True
                elif No_Rect.collidepoint((x,y)):
                    return False

        if Yes_Rect.collidepoint((x,y)):
            pygame.draw.rect(SCREEN, RED, (Yes_Rect.x, Yes_Rect.y, Yes_Rect.w, Yes_Rect.h), 5)
        elif No_Rect.collidepoint((x,y)):
            pygame.draw.rect(SCREEN, RED, (No_Rect.x, No_Rect.y, No_Rect.w, No_Rect.h), 5)

        pygame.display.update()

def reset():
    snake_position.clear()
    block_list.empty()
    snake_list.empty()

    ### create fruit
    fruit.re_generate(snake_position)

    ### create player
    snake.rect.x = COL//2*SIDE
    snake.rect.y = ROW//2*SIDE
    snake.dir = 'NONE'

    ### add to sprite group
    block_list.add(fruit)
    block_list.add(snake)
    snake_list.add(snake)

    ### snake position of each part
    snake_position.append({'x': snake.rect.x, 'y': snake.rect.y, 'd': snake.dir})

def update_map_status(MAP_STATUS):
    for i in range(len(snake_position)):
        x = snake_position[i]['x']//SIDE
        y = snake_position[i]['y']//SIDE
        MAP_STATUS[y][x] = OCCUPIED

def get_blank_position():
    POSITION = []
    for row in range(1, len(MAP_STATUS)-1):
        for col in range(1, len(MAP_STATUS[row])-1):
            if MAP_STATUS[row][col] == BLANK:
                POSITION.append((col*SIDE, row*SIDE))
    return POSITION

### Title page
while not(GameStart or Exit_Game):

    '''
    pygame.mixer.music.load('clannad.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    '''
    SCREEN.fill(DARK_GREEN)
    SCREEN.blit(Start_Game_Surf, Start_Game_Rect)
    SCREEN.blit(Exit_Surf, Exit_Rect)
    SCREEN.blit(Title_Surf, Title_Rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        if event.type == MOUSEMOTION:
            (x,y) = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            if Start_Game_Rect.collidepoint((x,y)):
                GameStart = True
                reset()
                MAP_STATUS = init(BLANK_POSITION)
            elif Exit_Rect.collidepoint((x,y)):
                Exit_Game = True

    if Start_Game_Rect.collidepoint((x,y)):
        pygame.draw.rect(SCREEN, RED, (Start_Game_Rect.x, Start_Game_Rect.y, Start_Game_Rect.w, Start_Game_Rect.h), 5)
    elif Exit_Rect.collidepoint((x,y)):
        pygame.draw.rect(SCREEN, RED, (Exit_Rect.x, Exit_Rect.y, Exit_Rect.w, Exit_Rect.h), 5)

    pygame.display.update()

### main loop
while GameStart:
    ### previous state
    pre = snake.dir

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            ###sys.exit()
        if event.type == pygame.KEYDOWN:        ### get key pressed
            if event.key == pygame.K_UP and pre != 'DOWN':
                snake.dir = 'UP'
            elif event.key == pygame.K_DOWN and pre != 'UP':
                snake.dir = 'DOWN'
            elif event.key == pygame.K_LEFT and pre != 'RIGHT':
                snake.dir = 'LEFT'
            elif event.key == pygame.K_RIGHT and pre != 'LEFT':
                snake.dir = 'RIGHT'

	### snake action
    snake.update()
    ### add body and re-generate the position of fruit again
    if snake.rect.colliderect(fruit.rect):
        add_body()
        mark += 1
        MAP_STATUS = init(BLANK_POSITION)
        update_map_status(MAP_STATUS)
        BLANK_POSITION = get_blank_position()
        fruit.re_generate(snake_position, BLANK_POSITION)
    elif not(snake.inbox()) or touch_itself():
        ### show the page of marks and ask players choice
        pygame.time.wait(1000)
        GameOver_Page()
        pygame.time.wait(1000)
        if PlayAgain():
            reset()
            MAP_STATUS = init(BLANK_POSITION)
            mark = 0
            continue
        else:
            pygame.quit()
            sys.exit()
            break

    ### background setting
    update()
    build()

    ### pygame.draw.rect(SCREEN, RED, (0, 0, WIDTH, HEIGHT), SIDE)
    block_list.draw(SCREEN)
    ShowMarks()
    clock.tick(FPS)
    pygame.display.update()
### end of main loop

