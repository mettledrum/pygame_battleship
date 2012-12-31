#!/usr/bin/env python

# Andrew Hoyle

import pygame, sys, random
from pygame.locals import *
from Board import *
from Ship import *

'''-----------------------------placement funcs------------------------------'''

# moves ships back to first positions
def resetShips():

    # testing locations for ship
    #j1 = Ship(0, 0, 20, 45)
    #j2 = Ship(25, 0, 20, 70)
    #j3 = Ship(50, 0, 20, 70)
    #j4 = Ship(75, 0, 20, 95)
    #j5 = Ship(100, 0, 20, 120)

    # locations to start off board
    j1 = Ship(500-75-120, 250-45, 20, 45)
    j2 = Ship(500-75-90, 250-70, 20, 70)
    j3 = Ship(500-75-60, 250-70, 20, 70)
    j4 = Ship(500-75-30, 250-95, 20, 95)
    j5 = Ship(500-75, 250-120, 20, 120)

    shipL = []
    shipL.append(j1)
    shipL.append(j2)
    shipL.append(j3)
    shipL.append(j4)
    shipL.append(j5)

    return shipL


# -see if the PLAy or RESET buttons were pressed
# -buttons are hard-coded into the screen
def resetCheck((x,y)):
    if 413 < x and 485 > x:
        if 12 < y and 46 > y:
            return True
    return False
       
def playCheck((x,y)):
    if 413 < x and 485 > x:
        if 56 < y and 90 > y:
            return True
    return False


# -sums the centers of checkerboard that are covered
# -uses set arithmetic union operator... set([(x,y)])
def sumCenters(dotL, shipL):
    _set = set()
    for s in shipL:
        _set |= set(s.center_set(dotL))
    return len(_set)
    

# blits all ships to screen in list of Ships
def blitShips(shipL, scr):
    for s in shipL:
        scr.blit(s.sur, s.pos)

'''------------------------------battle funcs--------------------------------'''

# ------------------------------------- COMPUTER AI FUNCS ----------------------

# checks bounds of grid: [0,9]
def bounds_check_coords(x,y):
    if (x>=0 and x<=9 and y>=0 and y<=9):
        return True
    else:
        return False

# looks for ship, clicked, NOTsunk, returns bool if a tile is found
def find_cShip_not_sunk(uB):
    for i in range(len(uB)):
        for j in range(len(uB[i])):
            if uB[i][j]['clicked'] == True and \
                uB[i][j]['ship'] == True and \
                uB[i][j]['sunk'] == False:
                return True
    return False
    
# spin until unclicked tile is found, change to clicked, and return
def pick_unclicked_random_tile(uB):
    while(True):
        x, y = random.randrange(0,10), random.randrange(0,10)
        if uB[x][y]['clicked'] == False:
            uB[x][y]['clicked'] = True
            return
        
# MUST USE "x,y,i,j" because eval function in comp_play() uses strings!!!
#  with those values
def find_mostest(B, evalStr):

    # pick one first
    x,y = -1,-1

    for i in range(len(B)):
        for j in range(len(B[i])):
            if B[i][j]['clicked'] == True and \
                B[i][j]['ship'] == True and \
                B[i][j]['sunk'] == False:
                x,y = i,j

    # now find highest
    for i in range(len(B)):
        for j in range(len(B[i])):
            if B[i][j]['clicked'] == True and \
                B[i][j]['ship'] == True and \
                B[i][j]['sunk'] == False and \
                eval(evalStr):          # from udlr 0-3 "enum"
                x,y = i,j
    return x,y

# find_mostest(B, evalStr) uses x,y,i,j vars!!!
# computer plays, updates udlr enum(0-3), and returns it
def comp_play(uB,uS,udlr):

    # random pick if no clicked, not sunk, ship is found
    # this random selection could be improved later, by looking
    #  at the remaining ships' sizes for random spacing
    if find_cShip_not_sunk(uB) == False:
        pick_unclicked_random_tile(uB)      # updates 'clicked' value too
        return udlr  
    
    # to hold the coordinates of the most udlr tile
    x, y = 0, 0

    # keeps track of the times in the while loop... if more than
    #  4, there's a special case that this will help escape and 
    #  progress to picking a neighbor of a 'clicked' 'ship' not 'sunk'
    #  that is in bounds and 'unclicked'
    _loopCount = 5

    while(_loopCount > 0):
        # UP
        if udlr == 0:
            # find highest 'ship' & 'clicked' & NOT sunk
            x,y = find_mostest(uB, "y > j")
            # look at x, y in direction of udlr
            if bounds_check_coords(x,y-1) == True and uB[x][y-1]['clicked'] == False:
                # mark as clicked
                uB[x][y-1]['clicked'] = True
                return udlr
            # change direction of udlr, try again
            else: udlr = (udlr + 1) % 4

        # DOWN
        elif udlr == 1:
            # find lowest
            x,y = find_mostest(uB, "y < j")
            # look at x, y in direction of udlr
            if bounds_check_coords(x,y+1) == True and uB[x][y+1]['clicked'] == False:
                # mark as clicked
                uB[x][y+1]['clicked'] = True      
                return udlr
            # change direction of udlr, try again
            else: udlr = (udlr + 1) % 4

        # LEFT
        elif udlr == 2:
            # find "leftest"
            x,y = find_mostest(uB, "x > i")
            # look at x, y in direction of udlr
            if bounds_check_coords(x-1,y) == True and uB[x-1][y]['clicked'] == False:
                # mark as clicked
                uB[x-1][y]['clicked'] = True
                return udlr
            # change direction of udlr, try again
            else: udlr = (udlr + 1) % 4

        # RIGHT
        elif udlr == 3:     
            # find "rightest"
            x,y = find_mostest(uB, "x < i")
            # look at x, y in direction of udlr
            if bounds_check_coords(x+1,y) == True and uB[x+1][y]['clicked'] == False:
                # mark as clicked
                uB[x+1][y]['clicked'] = True 
                return udlr
            # change direction of udlr, try again
            else: udlr = (udlr + 1) % 4

        # ERROR CHECKING for udlr, shouldn't happen
        else: 
            print "something's wrong with the directions!", udlr 
            pygame.quit()
            sys.exit()

        # decrement loop counter
        _loopCount -= 1

    # RARE CASE:
    # if you get here, it's time to pick a neighbor that's 'unclicked'
    x,y = find_neighbor(uB)
    uB[x][y]['clicked'] = True
    return udlr


# for the rare case that there's something above highest,
#  to the left of leftest... etc.
# random 'unclicked' one is picked next to a hit ship not sunk
# returns the next coords. to be picked by comp_play()
def find_neighbor(uB):

    # put 'em in list
    _hitList = []
    for i in range(len(uB)):
        for j in range(len(uB[i])):
            if uB[i][j]['ship'] == True and \
                uB[i][j]['clicked'] == True and \
                uB[i][j]['sunk'] == False:
                _hitList.append((i,j))

    random.shuffle(_hitList)

    # now, check the neighbors of list    
    while(True):
        x,y = _hitList.pop()
        
        # go through each possibility: U D L R
        if bounds_check_coords(x,y-1) == True and uB[x][y-1]['clicked'] == False:
            return x,y-1
        if bounds_check_coords(x,y+1) == True and uB[x][y+1]['clicked'] == False:
            return x,y+1
        if bounds_check_coords(x-1,y) == True and uB[x-1][y]['clicked'] == False:
            return x-1,y
        if bounds_check_coords(x+1,y) == True and uB[x+1][y]['clicked'] == False:
            return x+1,y


# returns new shipL in TILE coordinates
def ship_shapes_to_shipLL(dotL, shipShapeL):
    
    _shipL = []
    _shipTileL = []

    # get values from Ship class list: shipShapeL
    for i in range(len(shipShapeL)):                  
        _shipL.append(shipShapeL[i].center_set(dotL))  

    for i in range(len(_shipL)):
        _shipTileRowL = []
        for j in range(len(_shipL[i])):
            x,y = _shipL[i][j]
            _shipTileRowL.append(coord_to_idx((x,y), 25))
        _shipTileL.append(_shipTileRowL)                     
        
    return _shipTileL


# ---------------------------------- BOTH FUNCS --------------------------------


# -if all in row of cShippLL are 'clicked' == True, then
#   mark those tiles in cBoard as 'sunk' now
# -used in user_play()
def sunk_check(cShipLL, cBoard):
    
    # put all 'unclicked' and 'ship' coords in tuples
    #  into a set
    _boardSet = set()
    for i in range(len(cBoard)):
        for j in range(len(cBoard[i])):
            if cBoard[i][j]['clicked'] == True and cBoard[i][j]['ship'] == True:
                _boardSet |= set([(i, j)])

    # make a set for each row of cShipLL and compare to _boardSet
    for i in cShipLL:
        _setRow = set()
        for j in i:
            _setRow |= set([j])

        # if they're all "hit", mark all tiles with 'sunk'
        if len(_setRow & _boardSet) == len(_setRow):
            for i in _setRow:
                x, y = i
                cBoard[x][y]['sunk'] = True
                    
    # cBoard now has updated 'sunk' values
    return cBoard

# 10x10 board of dict. of attributes; like a 2D array of "structs"
def create_board_list():
    _B = []
    for i in range(10):
        _tempRow = []
        for j in range(10):
            _tempRow.append({          
                'sunk': False,          # totally finished
                'clicked': False,       # clicked on it yet
                'ship': False, })       # is ship on this space?
                                    
        _B.append(_tempRow)
    return _B


# used by clicking checks, and center dots
def coord_to_idx((x,y), sqTileLen, xOff=0, yOff=0):
    return ( (x-xOff) // sqTileLen, (y-yOff) // sqTileLen)


# show the board on the screen at certain offsets based on
#  the values in the Board[][]{} that dictate what portion of
#  the clips images should be shown. 
# (255,0,255) = alpha color to turn to clear
def display_board(checkBoard, board, screen, clips, xOff=0, yOff=0, shipL=None):
    # checkers to screen
    screen.blit(checkBoard, (xOff,yOff))

    # optional display of the ships' List for user board
    if shipL != None:
        blitShips(shipL, screen)     # all 5 ships

    # -get the four types of tiles from clips:
    #  hit sunk nothing miss
    # -probably should make these global so they don't
    #  have to be recreated every time
    hitR = pygame.Rect(0,0, 25,25)
    sunkR = pygame.Rect(0,25*1, 25,25)
    nothingR = pygame.Rect(0,25*2, 25,25)
    missR = pygame.Rect(0,25*3, 25,25)

    # put tiles on screen based on [][]{} values
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]['sunk'] == True:
                screen.blit(clips, (xOff+i*25, yOff+j*25), sunkR)

            elif board[i][j]['clicked'] == True and board[i][j]['ship'] == True:
                screen.blit(clips, (xOff+i*25, yOff+j*25), hitR)

            elif board[i][j]['clicked'] == True and board[i][j]['ship'] == False:
                screen.blit(clips, (xOff+i*25, yOff+j*25), missR)

            else:
                screen.blit(clips, (xOff+i*25, yOff+j*25), nothingR)


# returns True bool if there are 17 'sunk' tiles
def win_check(board):
    _sumSunks = 0
    for i in board:
        for j in i:
            if j['sunk'] == True:
                _sumSunks += 1
    if _sumSunks == 17:
        return True
    else:
        return False


# changes ['ship'] "struct" value based on shipLL tuples (x,y)
def ships_to_board(cBoard, cShipLL):
    for i in cShipLL:
        for j in i:
            x, y = j
            cBoard[x][y]['ship'] = True
    return cBoard


# ---------------------------------- USER FUNCS --------------------------------


def bounds_click_check((x,y)):
    if x<=9 and x>=0 and y<=9 and y>=0:
        return True
    else: return False


# returns alt. color checker board
# color1 and color2 are pygame colors
def create_checker_board(tileWidth, tileRowNum, tileColNum, color1, color2):

    _tempBoard = pygame.Surface(
        (tileWidth*tileRowNum, tileWidth*tileColNum)).convert()

    _altColorBool = True

    for i in range(tileRowNum):
        for j in range(tileColNum):
            _tempSq = pygame.Surface((tileWidth,tileWidth)).convert()

            if _altColorBool == True:
                _tempSq.fill(color1)
            else:
                _tempSq.fill(color2)

            _altColorBool = not _altColorBool
            
            # put tiles on the board
            _tempBoard.blit(_tempSq, (tileWidth*i, tileWidth*j))

        # if row number is even, flip bool again
        if tileRowNum % 2 == 0:
            _altColorBool = not _altColorBool

    _tempBoard.set_alpha(200)

    return _tempBoard
    

# creates the compShipLL randomly for computer opponent
def place_comp_ships():
    _tempShipLL = [ \
        [ (0,0), (0,0), ], \
        [ (0,0), (0,0), (0,0) ], \
        [ (0,0), (0,0), (0,0) ], \
        [ (0,0), (0,0), (0,0), (0,0) ], \
        [ (0,0), (0,0), (0,0), (0,0), (0,0) ] ]

    # loop until satisfactory values are found
    while (True):
        for i in range(len(_tempShipLL)):
            # randomly pick direction NSEW
            _dir = random.randrange(0,4)
            _x, _y, xinc, yinc = 0, 0, 0, 0           # reset _x, _y values
            
            if _dir == 0:
                xinc = 1
            elif _dir == 1:
                xinc = -1
            elif _dir == 2:
                yinc = 1
            else:
                yinc = -1

            # pick starting point
            _sX, _sY = random.randrange(0,10), random.randrange(0,10)
            
            # fill rows
            for j in range(len(_tempShipLL[i])):
                _tempShipLL[i][j] = (_sX + _x, _sY + _y)
                _x += xinc
                _y += yinc
                

        # see if all are uniquely placed, leave func if True
        if set_check(_tempShipLL) == 17 and bounds_check(_tempShipLL) == True:
            return _tempShipLL


# returns number of unique (x,y) tuples in shipLL
# used with place_comp_ships(), compared to 17
def set_check(shipLL):
    # empty set whose length will be returned
    _set = set()
    for i in range(len(shipLL)):
        for j in range(len(shipLL[i])):            
            _set |= set([shipLL[i][j]])        
    return len(_set)


# returns True if (x,y) tuples are all LT: 10, and GT: 0
# used with place_comp_ships()
def bounds_check(shipLL):
    for i in shipLL:
        for j in i:
            X , Y = j
            if (X>9 or X<0 or Y>9 or Y<0):
                return False
    return True
            

# takes click, makes sure it's valid, changes tile to clicked,
#  updates tiles to 'sunk' if a row in cShipLL is all 'unclicked',
#  returns True if there's a valid click after making changes
def user_play((x,y), cBoard, cShipLL):
    
    # check bounds
    if (x>9 or x<0 or y>9 or y<0):
        return False    

    # has it been clicked yet?
    if cBoard[x][y]['clicked'] == True:
        return False

    # unclicked tile has been selected
    # now, mark it as clicked and return
    cBoard[x][y]['clicked'] = True

    # marks tiles in Board as sunk if a row in cShipLL is 'clicked'
    cBoard = sunk_check(cShipLL, cBoard)

    return True
    

# for end of game, to see if play again "button" clicked
def playAgainCheck((x,y)):
    if 375 < x and 475 > x:
        if 175 < y and 225 > y:
            return True
    return False




