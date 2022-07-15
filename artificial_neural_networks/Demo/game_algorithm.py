import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import numpy as np
import copy


####################################################################################################
#
#   DATA
#
#
####################################################################################################


# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (160, 160, 160)

# OUR GRID MAP:
#cellMAP = np.random.randint(2, size=(10, 10))
constMAP = np.array([ [0 , 1 ,1 ,1 ,0 ,1 ,1 ,0 ,0 ,0],
                      [0 , 0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0],
                      [0 , 0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0],
                      [0 , 0 ,1 ,0 ,0 ,0 ,1 ,0 ,1 ,0],
                      [0 , 0 ,0 ,0 ,0 ,0 ,1 ,0 ,1 ,0],
                      [0 , 0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0],
                      [0 , 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
                      [0 , 0 ,1 ,0 ,1 ,0 ,0 ,0 ,0 ,0],
                      [0 , 0 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,0],
                      [0 , 0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0]],np.int32) 
cellMAP = copy.deepcopy(constMAP)

#monster constants
M_UP = 1
M_DOWN = 2
M_LEFT = 3
M_RIGHT = 4

hero = [0,0]
monster = [9,9]
direction = M_UP

score = 0


_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': cellMAP.shape[0], 'lineWidth': 2}



####################################################################################################
#
#   MAIN GAME LOOP
#
#
####################################################################################################
def main():
    pygame.init()

    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    font = pygame.font.SysFont(None, 24)
    img = font.render(str(score), True, GREEN)
    

    while notDead():
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
         _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        moveMonster()
        moveHero()
        placeHero()
        placeMonster()
        placeCells()
        img = font.render(str(score), True, GREEN)
        _VARS['surf'].blit(img, (20, 20))
        pygame.display.update()
    img = font.render(str(score), True, GREEN)
    _VARS['surf'].blit(img, (20, 20))
    pygame.display.update()
    while True:
        checkEvents()


def notDead():
    if hero[0] == monster[0] and hero[1] == monster[1]:
        return False
    else: 
        return True

def placeHero():
    global cellMAP 
    cellMAP = copy.deepcopy(constMAP)
    cellMAP[hero[0]][hero[1]] = 2








####################################################################################################
#
#   GUI VISUAL UPDATE
#
#
####################################################################################################
def placeMonster():
    global cellMAP 
    cellMAP[monster[0]][monster[1]] = 3

# NEW METHOD FOR ADDING CELLS :
def placeCells():
    # GET CELL DIMENSIONS...
    cellBorder = 6
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # DOUBLE LOOP
    for row in range(cellMAP.shape[0]):
        for column in range(cellMAP.shape[1]):
            # Is the grid cell tiled ?
            if(cellMAP[column][row] == 1):
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY)
            if(cellMAP[column][row] == 2):
                drawSquareCellRed(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY)
            if(cellMAP[column][row] == 3):
                drawSquareCellGreen(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY)


# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], BLACK,
     (x, y, dimX, dimY)
    )

# Draw filled rectangle at coordinates
def drawSquareCellRed(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], RED,
     (x, y, dimX, dimY)
    )

# Draw filled rectangle at coordinates
def drawSquareCellGreen(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], GREEN,
     (x, y, dimX, dimY)
    )


def drawSquareGrid(origin, gridWH, cells):

    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin

    # DRAW Grid Border:
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
    # # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
    # # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
    # # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

    # Get cell size, just one since its a square grid.
    cellSize = CONTAINER_WIDTH_HEIGHT/cells

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(cells):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (cont_x + (cellSize * x), cont_y),
           (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
    # # HORIZONTAl DIVISIONS
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (cont_x, cont_y + (cellSize*x)),
          (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)




####################################################################################################
#
#   MONSTER CONTROL
#
#
####################################################################################################

def canMove(dir):
    if dir == M_UP:
        if monster[0] == 0:
            return False
        if constMAP[monster[0]-1][monster[1]] != 1:
            return True
        else :
            return False
    if dir == M_DOWN:
        if monster[0] == 9:
            return False
        if constMAP[monster[0]+1][monster[1]] != 1:
            return True
        else :
            return False
    if dir == M_RIGHT:
        if monster[1] == 9:
            return False
        if constMAP[monster[0]][monster[1]+1] != 1:
            return True
        else :
            return False
    if dir == M_LEFT:
        if monster[1] == 0:
            return False
        if constMAP[monster[0]][monster[1]-1] != 1:
            return True
        else :
            return False

def moveMonsterTo(dir):
    global direction
    if dir == M_UP:
        monster[0] = monster[0] - 1
    if dir == M_DOWN:
        monster[0] = monster[0] + 1
    if dir == M_RIGHT:
        monster[1] = monster[1] + 1
    if dir == M_LEFT:
        monster[1] = monster[1] - 1
    direction = dir

def notReverse():
    if direction == M_UP:
        if towardsHero() == M_DOWN:
            return False
    if direction == M_DOWN:
        if towardsHero() == M_UP:
            return False
    if direction == M_RIGHT:
        if towardsHero() == M_LEFT:
            return False
    if direction == M_LEFT:
        if towardsHero() == M_RIGHT:
            return False
    return True


def towardsHero():
    if hero[0] < monster[0]:
        return M_UP
    elif hero[1] < monster[1]:
        return M_LEFT
    elif hero[0] > monster[0]:
        return M_DOWN
    elif hero[1] > monster[1]:
        return M_RIGHT


def turnMonster():
    if direction == M_UP:
        if canMove(M_RIGHT) and hero[1] > monster[1]:
            return M_RIGHT
        if canMove(M_LEFT) and hero[1] < monster[1]:
            return M_LEFT
        if canMove(M_RIGHT):
            return M_RIGHT
        if canMove(M_LEFT):
            return M_LEFT
        return M_DOWN
    if direction == M_DOWN:
        if canMove(M_RIGHT) and hero[1] > monster[1]:
            return M_RIGHT
        if canMove(M_LEFT) and hero[1] < monster[1]:
            return M_LEFT
        if canMove(M_RIGHT):
            return M_RIGHT
        if canMove(M_LEFT):
            return M_LEFT
        return M_UP
    if direction == M_RIGHT:
        if canMove(M_UP) and hero[0] < monster[0]:
            return M_UP
        if canMove(M_DOWN)  and hero[0] > monster[0]:
            return M_DOWN
        if canMove(M_UP):
            return M_UP
        if canMove(M_DOWN):
            return M_DOWN
        return M_LEFT
    if direction == M_LEFT:
        if canMove(M_UP) and hero[0] < monster[0]:
            return M_UP
        if canMove(M_DOWN)  and hero[0] > monster[0]:
            return M_DOWN
        if canMove(M_UP):
            return M_UP
        if canMove(M_DOWN):
            return M_DOWN
        return M_RIGHT


def moveMonster():
    global direction
    #do not move if we just got hero
    if hero[0] != monster[0] or hero[1] != monster[1]:
        #if can move toward hero not reverse
        if canMove(towardsHero()) and notReverse():
        #    do
            moveMonsterTo(towardsHero())
        #else 
        else:
        #    if can keep direction
            if canMove(direction):
                moveMonsterTo(direction)
        #        do
        #    else
            else:
                moveMonsterTo(turnMonster())
        #        try not reverse
        #            else, reverse
        #monster motion





####################################################################################################
#
#   USER INPUT
#
#
####################################################################################################

def checkEvents():
    global score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
            
            
        
 ####################################################################################################
#
#   HERO CONTROL ALGORITHM
#
#
####################################################################################################           
herodirection = M_DOWN;

def moveHeroTo(dir):
    global herodirection
    if dir == M_UP:
        hero[0] = hero[0] - 1
    if dir == M_DOWN:
        hero[0] = hero[0] + 1
    if dir == M_RIGHT:
        hero[1] = hero[1] + 1
    if dir == M_LEFT:
        hero[1] = hero[1] - 1
    direction = dir

def canMoveHero(dir):
    if dir == M_UP:
        if hero[0] == 0:
            return False
        if hero[0]-1 == monster[0] and hero[1] == monster[1]:
            return False
        if constMAP[hero[0]-1][hero[1]] != 1:
            return True
        else:
            return False
    if dir == M_DOWN:
        if hero[0] == 9:
            return False
        if hero[0]+1 == monster[0] and hero[1] == monster[1]:
            return False
        if constMAP[hero[0]+1][hero[1]] != 1:
            return True
        else :
            return False
    if dir == M_RIGHT:
        if hero[1] == 9:
            return False
        if hero[1]+1 == monster[1]  and hero[0] == monster[0]:
            return False
        if constMAP[hero[0]][hero[1]+1] != 1:
            return True
        else :
            return False
    if dir == M_LEFT:
        if hero[1] == 0:
            return False
        if hero[1]-1 == monster[1]  and hero[0] == monster[0]:
            return False
        if constMAP[hero[0]][hero[1]-1] != 1:
            return True
        else :
            return False

def noMonster(dir):
    if dir == M_UP:
        if hero[0]-1==monster[0] and hero[1] == monster[1]:
            return False
        else :
            return True
    if dir == M_DOWN:
        if hero[0]+1==monster[0] and hero[1] == monster[1]:
            return False
        else :
            return True
    if dir == M_RIGHT:
        if hero[0]==monster[0] and hero[1]+1 == monster[1]:
            return False
        else :
            return True
    if dir == M_LEFT:
        if hero[0]==monster[0] and hero[1]-1 == monster[1]:
            return False
        else :
            return True


def turnHeroRight():
    global herodirection
    if herodirection == M_UP:
        herodirection = M_RIGHT
        return
    if herodirection == M_RIGHT:
        herodirection = M_DOWN
        return
    if herodirection == M_DOWN:
        herodirection = M_LEFT
        return
    if herodirection == M_LEFT:
        herodirection = M_UP
        return

def moveHero():
    global score
    global herodirection
    from time import sleep
    sleep(0.5)
    #if can move in same direction, keep doing it
    #otherwise, turn right
    if canMoveHero(herodirection) and noMonster(herodirection):
        moveHeroTo(herodirection)
        score = score + 1
    else:
        turnHeroRight()
        if canMoveHero(herodirection) and noMonster(herodirection):
            moveHeroTo(herodirection)
            score = score + 1
    

if __name__ == '__main__':
    main()