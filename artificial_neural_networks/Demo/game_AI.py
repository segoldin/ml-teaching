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
    global score
    global hero
    global monster
    global direction
    pygame.init()

    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    font = pygame.font.SysFont(None, 24)
    img = font.render(str(score), True, GREEN)
    
    while True:
        while notDead():
            checkEvents()
            _VARS['surf'].fill(GREY)
            drawSquareGrid(
             _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
            
            moveHero()
            placeHero()
            moveMonster()
            placeMonster()
            placeCells()
            img = font.render(str(score), True, GREEN)
            _VARS['surf'].blit(img, (20, 20))
            pygame.display.update()

        hero = [0,0]
        monster = [9,9]
        direction = M_UP
        score = 0;
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

def Dead():
    if hero[0] == monster[0] and hero[1] == monster[1]:
        return True
    else: 
        return False

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
    global hero
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







#neural network
out_neuron_up = 0       #out0
out_neuron_down = 0     #out1
out_neuron_left = 0     #out2
out_neuron_right = 0    #out3


in_neuron_top_left = 0      #in0
in_neuron_top = 0           #in1
in_neuron_top_right = 0     #in2
in_neuron_left = 0          #in3
in_neuron_right = 0         #in4
in_neuron_bottom_left = 0   #in5
in_neuron_bottom = 0        #in6
in_neuron_bottom_right = 0  #in7


in0_out0 = 0.1;
in1_out0 = 0.1;
in2_out0 = 0.1;
in3_out0 = 0.1;
in4_out0 = 0.1;
in5_out0 = 0.1;
in6_out0 = 0.1;
in7_out0 = 0.1;

in0_out1 = 1;
in1_out1 = 1;
in2_out1 = 1;
in3_out1 = 1;
in4_out1 = 1;
in5_out1 = 1;
in6_out1 = 1;
in7_out1 = 1;

in0_out2 = 0.1;
in1_out2 = 0.1;
in2_out2 = 0.1;
in3_out2 = 0.1;
in4_out2 = 0.1;
in5_out2 = 0.1;
in6_out2 = 0.1;
in7_out2 = 0.1;

in0_out3 = 0.1;
in1_out3 = 0.1;
in2_out3 = 0.1;
in3_out3 = 0.1;
in4_out3 = 0.1;
in5_out3 = 0.1;
in6_out3 = 0.1;
in7_out3 = 0.1;


def moveHero():
    global score
    #AI implementation
    #we'll use 0 for wall, 1 for available, -1 for monster
    #update inputs
    from time import sleep
    sleep(0.25)
    #sleep(0.5)

    update_input_neurons()
    update_output_neurons()
    direction = choose_biggest()
    if canMoveHero(direction):
        moveHeroTo(direction)
        update_weights_good(direction)
        score = score + 1
    else:
        update_weights_bad(direction)
    #placeMonster()
    if Dead():
        print("DIED")
        update_weights_bad(direction)
    
def update_weights_good(dir):
    global in0_out0 
    global in1_out0 
    global in2_out0 
    global in3_out0 
    global in4_out0 
    global in5_out0 
    global in6_out0 
    global in7_out0 
    global in0_out1 
    global in1_out1 
    global in2_out1 
    global in3_out1 
    global in4_out1 
    global in5_out1 
    global in6_out1 
    global in7_out1 
    global in0_out2
    global in1_out2 
    global in2_out2 
    global in3_out2 
    global in4_out2 
    global in5_out2 
    global in6_out2 
    global in7_out2 
    global in0_out3 
    global in1_out3 
    global in2_out3 
    global in3_out3 
    global in4_out3 
    global in5_out3 
    global in6_out3 
    global in7_out3 
    if dir == M_UP:
        #output neuron that was positive increments its weights, if input neuron was positive
        if out_neuron_up > 0:
            in0_out0 = in0_out0 + 0.1 if in_neuron_top_left > 0     else in0_out0 - 0.1
            in1_out0 = in1_out0 + 0.1 if in_neuron_top > 0          else in1_out0 - 0.1
            in2_out0 = in2_out0 + 0.1 if in_neuron_top_right > 0    else in2_out0 - 0.1
            in3_out0 = in3_out0 + 0.1 if in_neuron_left > 0         else in3_out0 - 0.1
            in4_out0 = in4_out0 + 0.1 if in_neuron_right > 0        else in4_out0 - 0.1
            in5_out0 = in5_out0 + 0.1 if in_neuron_bottom_left > 0  else in5_out0 - 0.1
            in6_out0 = in6_out0 + 0.1 if in_neuron_bottom > 0       else in6_out0 - 0.1
            in7_out0 = in7_out0 + 0.1 if in_neuron_bottom_right > 0 else in7_out0 - 0.1
        #negative, decrement
        else:
            in0_out0 = in0_out0 - 0.1 if in_neuron_top_left > 0     else in0_out0 + 0.1
            in1_out0 = in1_out0 - 0.1 if in_neuron_top > 0          else in1_out0 + 0.1
            in2_out0 = in2_out0 - 0.1 if in_neuron_top_right > 0    else in2_out0 + 0.1
            in3_out0 = in3_out0 - 0.1 if in_neuron_left > 0         else in3_out0 + 0.1
            in4_out0 = in4_out0 - 0.1 if in_neuron_right > 0        else in4_out0 + 0.1
            in5_out0 = in5_out0 - 0.1 if in_neuron_bottom_left > 0  else in5_out0 + 0.1
            in6_out0 = in6_out0 - 0.1 if in_neuron_bottom > 0       else in6_out0 + 0.1
            in7_out0 = in7_out0 - 0.1 if in_neuron_bottom_right > 0 else in7_out0 + 0.1
    if dir == M_DOWN:
        #output neuron that was positive increments its weights
        if out_neuron_down > 0:
            in0_out1 = in0_out1 + 0.1 if in_neuron_top_left > 0     else in0_out1 - 0.1
            in1_out1 = in1_out1 + 0.1 if in_neuron_top > 0          else in1_out1 - 0.1
            in2_out1 = in2_out1 + 0.1 if in_neuron_top_right > 0    else in2_out1 - 0.1
            in3_out1 = in3_out1 + 0.1 if in_neuron_left > 0         else in3_out1 - 0.1
            in4_out1 = in4_out1 + 0.1 if in_neuron_right > 0        else in4_out1 - 0.1
            in5_out1 = in5_out1 + 0.1 if in_neuron_bottom_left > 0  else in5_out1 - 0.1
            in6_out1 = in6_out1 + 0.1 if in_neuron_bottom > 0       else in6_out1 - 0.1
            in7_out1 = in7_out1 + 0.1 if in_neuron_bottom_right > 0 else in7_out1 - 0.1
        #negative, decrement
        else:
            in0_out1 = in0_out1 - 0.1 if in_neuron_top_left > 0     else in0_out1 + 0.1
            in1_out1 = in1_out1 - 0.1 if in_neuron_top > 0          else in1_out1 + 0.1
            in2_out1 = in2_out1 - 0.1 if in_neuron_top_right > 0    else in2_out1 + 0.1
            in3_out1 = in3_out1 - 0.1 if in_neuron_left > 0         else in3_out1 + 0.1
            in4_out1 = in4_out1 - 0.1 if in_neuron_right > 0        else in4_out1 + 0.1
            in5_out1 = in5_out1 - 0.1 if in_neuron_bottom_left > 0  else in5_out1 + 0.1
            in6_out1 = in6_out1 - 0.1 if in_neuron_bottom > 0       else in6_out1 + 0.1
            in7_out1 = in7_out1 - 0.1 if in_neuron_bottom_right > 0 else in7_out1 + 0.1
    if dir == M_LEFT:
        #output neuron that was positive increments its weights
        if out_neuron_left > 0:
            in0_out2 = in0_out2 + 0.1 if in_neuron_top_left > 0     else in0_out2 - 0.1
            in1_out2 = in1_out2 + 0.1 if in_neuron_top > 0          else in1_out2 - 0.1
            in2_out2 = in2_out2 + 0.1 if in_neuron_top_right > 0    else in2_out2 - 0.1
            in3_out2 = in3_out2 + 0.1 if in_neuron_left > 0         else in3_out2 - 0.1
            in4_out2 = in4_out2 + 0.1 if in_neuron_right > 0        else in4_out2 - 0.1
            in5_out2 = in5_out2 + 0.1 if in_neuron_bottom_left > 0  else in5_out2 - 0.1
            in6_out2 = in6_out2 + 0.1 if in_neuron_bottom > 0       else in6_out2 - 0.1
            in7_out2 = in7_out2 + 0.1 if in_neuron_bottom_right > 0 else in7_out2 - 0.1
        #negative, decrement
        else:
            in0_out2 = in0_out2 - 0.1 if in_neuron_top_left > 0     else in0_out2 + 0.1
            in1_out2 = in1_out2 - 0.1 if in_neuron_top > 0          else in1_out2 + 0.1
            in2_out2 = in2_out2 - 0.1 if in_neuron_top_right > 0    else in2_out2 + 0.1
            in3_out2 = in3_out2 - 0.1 if in_neuron_left > 0         else in3_out2 + 0.1
            in4_out2 = in4_out2 - 0.1 if in_neuron_right > 0        else in4_out2 + 0.1
            in5_out2 = in5_out2 - 0.1 if in_neuron_bottom_left > 0  else in5_out2 + 0.1
            in6_out2 = in6_out2 - 0.1 if in_neuron_bottom > 0       else in6_out2 + 0.1
            in7_out2 = in7_out2 - 0.1 if in_neuron_bottom_right > 0 else in7_out2 + 0.1
    if dir == M_RIGHT:
        #output neuron that was positive increments its weights
        if out_neuron_right > 0:
            in0_out3 = in0_out3 + 0.1 if in_neuron_top_left > 0     else in0_out3 - 0.1
            in1_out3 = in1_out3 + 0.1 if in_neuron_top > 0          else in1_out3 - 0.1
            in2_out3 = in2_out3 + 0.1 if in_neuron_top_right > 0    else in2_out3 - 0.1
            in3_out3 = in3_out3 + 0.1 if in_neuron_left > 0         else in3_out3 - 0.1
            in4_out3 = in4_out3 + 0.1 if in_neuron_right > 0        else in4_out3 - 0.1
            in5_out3 = in5_out3 + 0.1 if in_neuron_bottom_left > 0  else in5_out3 - 0.1
            in6_out3 = in6_out3 + 0.1 if in_neuron_bottom > 0       else in6_out3 - 0.1
            in7_out3 = in7_out3 + 0.1 if in_neuron_bottom_right > 0 else in7_out3 - 0.1
        #negative, decrement
        else:
            in0_out3 = in0_out3 - 0.1 if in_neuron_top_left > 0     else in0_out3 + 0.1
            in1_out3 = in1_out3 - 0.1 if in_neuron_top > 0          else in1_out3 + 0.1
            in2_out3 = in2_out3 - 0.1 if in_neuron_top_right > 0    else in2_out3 + 0.1
            in3_out3 = in3_out3 - 0.1 if in_neuron_left > 0         else in3_out3 + 0.1
            in4_out3 = in4_out3 - 0.1 if in_neuron_right > 0        else in4_out3 + 0.1
            in5_out3 = in5_out3 - 0.1 if in_neuron_bottom_left > 0  else in5_out3 + 0.1
            in6_out3 = in6_out3 - 0.1 if in_neuron_bottom > 0       else in6_out3 + 0.1
            in7_out3 = in7_out3 - 0.1 if in_neuron_bottom_right > 0 else in7_out3 + 0.1

def update_weights_bad(dir):
    global in0_out0 
    global in1_out0 
    global in2_out0 
    global in3_out0 
    global in4_out0 
    global in5_out0 
    global in6_out0 
    global in7_out0 
    global in0_out1 
    global in1_out1 
    global in2_out1 
    global in3_out1 
    global in4_out1 
    global in5_out1 
    global in6_out1 
    global in7_out1 
    global in0_out2
    global in1_out2 
    global in2_out2 
    global in3_out2 
    global in4_out2 
    global in5_out2 
    global in6_out2 
    global in7_out2 
    global in0_out3 
    global in1_out3 
    global in2_out3 
    global in3_out3 
    global in4_out3 
    global in5_out3 
    global in6_out3 
    global in7_out3 
    if dir == M_UP:
        #output neuron that was positive increments its weights, if input neuron was positive
        if out_neuron_up > 0:
            in0_out0 = in0_out0 - 0.3 if in_neuron_top_left > 0     else in0_out0 + 0.3
            in1_out0 = in1_out0 - 0.3 if in_neuron_top > 0          else in1_out0 + 0.3
            in2_out0 = in2_out0 - 0.3 if in_neuron_top_right > 0    else in2_out0 + 0.3
            in3_out0 = in3_out0 - 0.3 if in_neuron_left > 0         else in3_out0 + 0.3
            in4_out0 = in4_out0 - 0.3 if in_neuron_right > 0        else in4_out0 + 0.3
            in5_out0 = in5_out0 - 0.3 if in_neuron_bottom_left > 0  else in5_out0 + 0.3
            in6_out0 = in6_out0 - 0.3 if in_neuron_bottom > 0       else in6_out0 + 0.3
            in7_out0 = in7_out0 - 0.3 if in_neuron_bottom_right > 0 else in7_out0 + 0.3
        #negative, decrement
        else:
            in0_out0 = in0_out0 + 0.3 if in_neuron_top_left > 0     else in0_out0 - 0.3
            in1_out0 = in1_out0 + 0.3 if in_neuron_top > 0          else in1_out0 - 0.3
            in2_out0 = in2_out0 + 0.3 if in_neuron_top_right > 0    else in2_out0 - 0.3
            in3_out0 = in3_out0 + 0.3 if in_neuron_left > 0         else in3_out0 - 0.3
            in4_out0 = in4_out0 + 0.3 if in_neuron_right > 0        else in4_out0 - 0.3
            in5_out0 = in5_out0 + 0.3 if in_neuron_bottom_left > 0  else in5_out0 - 0.3
            in6_out0 = in6_out0 + 0.3 if in_neuron_bottom > 0       else in6_out0 - 0.3
            in7_out0 = in7_out0 + 0.3 if in_neuron_bottom_right > 0 else in7_out0 - 0.3
    if dir == M_DOWN:
        #output neuron that was positive increments its weights
        if out_neuron_down > 0:
            in0_out1 = in0_out1 - 0.3 if in_neuron_top_left > 0     else in0_out1 + 0.3
            in1_out1 = in1_out1 - 0.3 if in_neuron_top > 0          else in1_out1 + 0.3
            in2_out1 = in2_out1 - 0.3 if in_neuron_top_right > 0    else in2_out1 + 0.3
            in3_out1 = in3_out1 - 0.3 if in_neuron_left > 0         else in3_out1 + 0.3
            in4_out1 = in4_out1 - 0.3 if in_neuron_right > 0        else in4_out1 + 0.3
            in5_out1 = in5_out1 - 0.3 if in_neuron_bottom_left > 0  else in5_out1 + 0.3
            in6_out1 = in6_out1 - 0.3 if in_neuron_bottom > 0       else in6_out1 + 0.3
            in7_out1 = in7_out1 - 0.3 if in_neuron_bottom_right > 0 else in7_out1 + 0.3
        #negative, decrement
        else:
            in0_out1 = in0_out1 + 0.3 if in_neuron_top_left > 0     else in0_out1 - 0.3
            in1_out1 = in1_out1 + 0.3 if in_neuron_top > 0          else in1_out1 - 0.3
            in2_out1 = in2_out1 + 0.3 if in_neuron_top_right > 0    else in2_out1 - 0.3
            in3_out1 = in3_out1 + 0.3 if in_neuron_left > 0         else in3_out1 - 0.3
            in4_out1 = in4_out1 + 0.3 if in_neuron_right > 0        else in4_out1 - 0.3
            in5_out1 = in5_out1 + 0.3 if in_neuron_bottom_left > 0  else in5_out1 - 0.3
            in6_out1 = in6_out1 + 0.3 if in_neuron_bottom > 0       else in6_out1 - 0.3
            in7_out1 = in7_out1 + 0.3 if in_neuron_bottom_right > 0 else in7_out1 - 0.3
    if dir == M_LEFT:
        #output neuron that was positive increments its weights
        if out_neuron_left > 0:
            in0_out2 = in0_out2 - 0.3 if in_neuron_top_left > 0     else in0_out2 + 0.3
            in1_out2 = in1_out2 - 0.3 if in_neuron_top > 0          else in1_out2 + 0.3
            in2_out2 = in2_out2 - 0.3 if in_neuron_top_right > 0    else in2_out2 + 0.3
            in3_out2 = in3_out2 - 0.3 if in_neuron_left > 0         else in3_out2 + 0.3
            in4_out2 = in4_out2 - 0.3 if in_neuron_right > 0        else in4_out2 + 0.3
            in5_out2 = in5_out2 - 0.3 if in_neuron_bottom_left > 0  else in5_out2 + 0.3
            in6_out2 = in6_out2 - 0.3 if in_neuron_bottom > 0       else in6_out2 + 0.3
            in7_out2 = in7_out2 - 0.3 if in_neuron_bottom_right > 0 else in7_out2 + 0.3
        #negative, decrement
        else:
            in0_out2 = in0_out2 + 0.3 if in_neuron_top_left > 0     else in0_out2 - 0.3
            in1_out2 = in1_out2 + 0.3 if in_neuron_top > 0          else in1_out2 - 0.3
            in2_out2 = in2_out2 + 0.3 if in_neuron_top_right > 0    else in2_out2 - 0.3
            in3_out2 = in3_out2 + 0.3 if in_neuron_left > 0         else in3_out2 - 0.3
            in4_out2 = in4_out2 + 0.3 if in_neuron_right > 0        else in4_out2 - 0.3
            in5_out2 = in5_out2 + 0.3 if in_neuron_bottom_left > 0  else in5_out2 - 0.3
            in6_out2 = in6_out2 + 0.3 if in_neuron_bottom > 0       else in6_out2 - 0.3
            in7_out2 = in7_out2 + 0.3 if in_neuron_bottom_right > 0 else in7_out2 - 0.3
    if dir == M_RIGHT:
        #output neuron that was positive increments its weights
        if out_neuron_right > 0:
            in0_out3 = in0_out3 - 0.3 if in_neuron_top_left > 0     else in0_out3 + 0.3
            in1_out3 = in1_out3 - 0.3 if in_neuron_top > 0          else in1_out3 + 0.3
            in2_out3 = in2_out3 - 0.3 if in_neuron_top_right > 0    else in2_out3 + 0.3
            in3_out3 = in3_out3 - 0.3 if in_neuron_left > 0         else in3_out3 + 0.3
            in4_out3 = in4_out3 - 0.3 if in_neuron_right > 0        else in4_out3 + 0.3
            in5_out3 = in5_out3 - 0.3 if in_neuron_bottom_left > 0  else in5_out3 + 0.3
            in6_out3 = in6_out3 - 0.3 if in_neuron_bottom > 0       else in6_out3 + 0.3
            in7_out3 = in7_out3 - 0.3 if in_neuron_bottom_right > 0 else in7_out3 + 0.3
        #negative, decrement
        else:
            in0_out3 = in0_out3 + 0.3 if in_neuron_top_left > 0     else in0_out3 - 0.3
            in1_out3 = in1_out3 + 0.3 if in_neuron_top > 0          else in1_out3 - 0.3
            in2_out3 = in2_out3 + 0.3 if in_neuron_top_right > 0    else in2_out3 - 0.3
            in3_out3 = in3_out3 + 0.3 if in_neuron_left > 0         else in3_out3 - 0.3
            in4_out3 = in4_out3 + 0.3 if in_neuron_right > 0        else in4_out3 - 0.3
            in5_out3 = in5_out3 + 0.3 if in_neuron_bottom_left > 0  else in5_out3 - 0.3
            in6_out3 = in6_out3 + 0.3 if in_neuron_bottom > 0       else in6_out3 - 0.3
            in7_out3 = in7_out3 + 0.3 if in_neuron_bottom_right > 0 else in7_out3 - 0.3


def update_output_neurons():
    global out_neuron_up
    global out_neuron_down
    global out_neuron_left
    global out_neuron_right
    out_neuron_up    = in0_out0*in_neuron_top_left + in1_out0*in_neuron_top + in2_out0*in_neuron_top_right + in3_out0*in_neuron_left + in4_out0*in_neuron_right + in5_out0*in_neuron_bottom_left + in6_out0*in_neuron_bottom + in7_out0*in_neuron_bottom_right
    out_neuron_down  = in0_out1*in_neuron_top_left + in1_out1*in_neuron_top + in2_out1*in_neuron_top_right + in3_out1*in_neuron_left + in4_out1*in_neuron_right + in5_out1*in_neuron_bottom_left + in6_out1*in_neuron_bottom + in7_out1*in_neuron_bottom_right
    out_neuron_left  = in0_out2*in_neuron_top_left + in1_out2*in_neuron_top + in2_out2*in_neuron_top_right + in3_out2*in_neuron_left + in4_out2*in_neuron_right + in5_out2*in_neuron_bottom_left + in6_out2*in_neuron_bottom + in7_out2*in_neuron_bottom_right
    out_neuron_right = in0_out3*in_neuron_top_left + in1_out3*in_neuron_top + in2_out3*in_neuron_top_right + in3_out3*in_neuron_left + in4_out3*in_neuron_right + in5_out3*in_neuron_bottom_left + in6_out3*in_neuron_bottom + in7_out3*in_neuron_bottom_right
    
def choose_biggest():
    global out_neuron_up
    global out_neuron_down
    global out_neuron_left
    global out_neuron_right
    up_or_down = M_DOWN;
    left_or_right = M_LEFT;
    if out_neuron_up > out_neuron_down :
        up_or_down = M_UP;
    if out_neuron_left < out_neuron_right:
        left_or_right = M_RIGHT;
    if up_or_down == M_UP:
        if left_or_right == M_LEFT:
            if out_neuron_up > out_neuron_left:
                return up_or_down
            else:
                return left_or_right
        else:    
            if out_neuron_up > out_neuron_right:
                return up_or_down
            else:
                return left_or_right
    else:
        if left_or_right == M_LEFT:
            if out_neuron_down > out_neuron_left:
                return up_or_down
            else:
                return left_or_right
        else:    
            if out_neuron_down > out_neuron_right:
                return up_or_down
            else:
                return left_or_right





def update_input_neurons():
    global in_neuron_top_left
    global in_neuron_top
    global in_neuron_top_right
    global in_neuron_left
    global in_neuron_right
    global in_neuron_bottom_left
    global in_neuron_bottom
    global in_neuron_bottom_right
    in_neuron_top_left = 0 if hero[0] == 0 or hero[1] == 0 else (-1 if monster[0] == hero[0]-1 and monster[1]==hero[1]-1 else (0 if constMAP[hero[0]-1][hero[1]-1] == 1 else 1)) 
    in_neuron_top = 0 if hero[0] == 0 else (-1 if monster[0] == hero[0]-1 and monster[1]==hero[1] else (0 if constMAP[hero[0]-1][hero[1]] == 1 else 1))
    in_neuron_top_right = 0 if hero[0] == 0 or hero[1] == 9 else (-1 if monster[0] == hero[0]-1 and monster[1]==hero[1]+1 else (0 if constMAP[hero[0]-1][hero[1]+1] == 1 else 1))
    in_neuron_bottom_left = 0 if hero[0] == 9 or hero[1] == 0 else (-1 if monster[0] == hero[0]+1 and monster[1]==hero[1]-1 else (0 if constMAP[hero[0]+1][hero[1]-1] == 1 else 1))
    in_neuron_bottom_right = 0 if hero[0] == 9 or hero[1] == 9 else (-1 if monster[0] == hero[0]+1 and monster[1]==hero[1]+1 else (0 if constMAP[hero[0]+1][hero[1]+1] == 1 else 1))
    in_neuron_bottom = 0 if hero[0] == 9 else (-1 if monster[0] == hero[0]+1 and monster[1]==hero[1] else (0 if constMAP[hero[0]+1][hero[1]] == 1 else 1))
    in_neuron_left = 0 if hero[1] == 0 else (-1 if monster[0] == hero[0] and monster[1]==hero[1]-1 else (0 if constMAP[hero[0]][hero[1]-1] == 1 else 1))
    in_neuron_right = 0 if hero[1] == 9 else (-1 if monster[0] == hero[0] and monster[1]==hero[1]+1 else (0 if constMAP[hero[0]][hero[1]+1] == 1 else 1))
    #print("grid")
    #print(str(in_neuron_top_left) + str(in_neuron_top) + str(in_neuron_top_right))
    #print(str(in_neuron_left) + "X" + str(in_neuron_right))
    #print(str(in_neuron_bottom_left) + str(in_neuron_bottom) + str(in_neuron_bottom_right))

if __name__ == '__main__':
    main()