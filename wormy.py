# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

from curses import KEY_C1
import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 1280
WINDOWHEIGHT = 960
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = ( 70,  50,  70)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    Score = 1
    FPS = 15
    collisions = True
    scoreHack = False

    # Start the apple in a random place.
    apple = getRandomLocation(wormCoords)
    apple2 = getRandomLocation(wormCoords)
    apple3 = getRandomLocation(wormCoords)

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d):
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w):
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s):
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LSHIFT:
                    if FPS <= 14:
                        FPS += 5
                    else:
                        FPS += 15
                elif event.key == K_LCTRL:
                    if FPS >= 16:
                        FPS -= 15
                    else:
                        FPS -= 5
                elif event.key == K_c:
                    collisions = not collisions
                elif event.key == K_x:
                    scoreHack = not scoreHack

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            if collisions:
                return # game over
            else:
                if direction == LEFT:
                    newHead = {'x': WINDOWWIDTH / 20, 'y': wormCoords[HEAD]['y']}
                    wormCoords.insert(0, newHead)
                    del wormCoords[-1]
                    drawWorm(wormCoords)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                elif direction == RIGHT:
                    newHead = {'x': 0, 'y': wormCoords[HEAD]['y']}
                    wormCoords.insert(0, newHead)
                    del wormCoords[-1]
                    drawWorm(wormCoords)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                elif direction == UP:
                    newHead = {'x': wormCoords[HEAD]['x'], 'y': WINDOWHEIGHT / 20}
                    wormCoords.insert(0, newHead)
                    del wormCoords[-1]
                    drawWorm(wormCoords)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                elif direction == DOWN:
                    newHead = {'x': wormCoords[HEAD]['x'], 'y': 0}
                    wormCoords.insert(0, newHead)
                    del wormCoords[-1]
                    drawWorm(wormCoords)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
        if collisions:
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                    return # game over

        # check if worm has eaten an apply
        if (wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']):
            # don't remove worm's tail segment
            if scoreHack:
                Score *= 2
            else:
                Score += 1
            apple = getRandomLocation(wormCoords) # set a new apple somewhere
        elif (wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']):
            # don't remove worm's tail segment
            if scoreHack == True:
                Score *= 2
            else:
                Score += 1
            apple2 = getRandomLocation(wormCoords) # set a new apple somewhere
        elif (wormCoords[HEAD]['x'] == apple3['x'] and wormCoords[HEAD]['y'] == apple3['y']):
            # don't remove worm's tail segment
            if scoreHack == True:
                Score *= 2
            else:
                Score += 1
            apple3 = getRandomLocation(wormCoords) # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment
        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawApple(apple2)
        drawApple(apple3)
        drawMenu(Score, FPS, collisions, scoreHack)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(wormCoords):
    choice = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    for wormBody in wormCoords[1:]:
        if wormBody['x'] != choice['x'] and wormBody['y'] != choice['y']:
            return choice


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawMenu(score, FPS, collisions, scoreHack):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    fpsSurf = BASICFONT.render('FPS: %s' % (FPS), True, WHITE)
    fpsRect = fpsSurf.get_rect()
    fpsRect.topleft = (10, 30)
    DISPLAYSURF.blit(fpsSurf, fpsRect)
    if collisions == True:
        colSurf = BASICFONT.render('Collisions: On', True, WHITE)
    else:
        colSurf = BASICFONT.render('Collisions: Off', True, WHITE)
    colRect = colSurf.get_rect()
    colRect.topleft = (10, 50)
    DISPLAYSURF.blit(colSurf, colRect)
    if scoreHack == True:
        shSurf = BASICFONT.render('Score Hack: On', True, WHITE)
    else:
        shSurf = BASICFONT.render('Score Hack: Off', True, WHITE)
    shRect = shSurf.get_rect()
    shRect.topleft = (10, 70)
    DISPLAYSURF.blit(shSurf, shRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()