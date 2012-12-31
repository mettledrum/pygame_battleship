#!/usr/bin/env python

# Andrew Hoyle
# -first pygame game, trying to do Battleship

# 12/19/12
# -can't get colors to update based on clicks
# -need to make a "drag" lock or something for the click and drag function
# -organize class objects checking for collisions and mouse-overs
#  with an array that calls the objects' methods

# 12/20/12
# -drag works
# -needs collision detection for edges, so doesn't leave screen
# -color didn't update b/c over_me method had indented if/else too far
# -dots' coordinates at centers of each tile should be stuffed into
#  a list of tuples for determining where ships are placed, and if
#  there's a valid placement of them
# -after a rotation, the over_me() is messed up, click area is 90
#  degrees from displayed ship
# -made pretty picture for behind board
# -if you grab multiple ones, then move one and rotate, the others
#  rotate as well!

# 12/26/12
# -added in compAI, and some functions from the userInput modules
# -evaluations of out of bounds need to come BEFORE the range checking
#  because out of bounds can't be referenced: board[i][j]!

# 12/27/12
# -found a case where comp_play freezes... so made a find_neighbor
#  function that makes a list of the hit but not sunk ships, and
#  picks a random tile UDLR of it that is in bounds, and unclicked
# -accidentally changed the Xs to xs and Ys to ys in funcs.py

# 12/30/12
# -made game work!
# -need to make ship pictures for Ships, and display them during battle
# -needs path.os functionality for different OSs?
# -make colors to board tiles NOT annoyingly colored =)


import pygame, sys, random
from pygame.locals import *
from Board import *
from Ship import *
from funcs import *


def main():

    pygame.init()
    random.seed()
    screen = pygame.display.set_mode((500, 350))
    pygame.display.set_caption('Place Your Ships!')

    # cool ocean and ship picture for behind board/ships
    picture = pygame.image.load('user_board.png')

    # checkerboard grid class, does over picture
    b = Board()

    # clock rate cap
    fps = 40 
    clock = pygame.time.Clock()

    # Ship classes placed into list
    shipList = []
    shipList = resetShips()     # 5 of 'em


    '''------------------------ selection -----------------------------------'''
    selectingPlaces = True
    # ship-placement loop
    while selectingPlaces:
        ############################ events ####################################
        for event in pygame.event.get():
            # quit game with X in corner or escape key
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # -for the PLAY, RESET buttons drawn in 'picture'
            #  blitted on screen
            if event.type == MOUSEBUTTONDOWN:                
                _res = resetCheck(pygame.mouse.get_pos())          
                _pla = playCheck(pygame.mouse.get_pos())   

                # put them back to starting place
                if _res == True:
                    shipList = resetShips() 
                
                # legal placement of ships was made
                if _pla == True and 17 == sumCenters(b.dots, shipList):
                    selectingPlaces = False
                    continue

            # manipulating the shipList, all 5 of them
            for S in shipList:
                # checks to see if mouse is over obj.
                if event.type == MOUSEMOTION:
                    S.over_me(pygame.mouse.get_pos())
            
                # prep for dragging, reset rel. mouse pos.
                if event.type == MOUSEBUTTONDOWN and S.over == True:
                    pygame.mouse.get_rel()
                    S.drag = True

                # allow 90 flipping only while dragging
                if event.type == KEYDOWN and S.drag == True:
                    S.rot_me(pygame.mouse.get_pos())
                
                # nix the dragability, must come BEFORE dragging code I think
                if event.type == MOUSEBUTTONUP:
                    S.drag = False

                # move that ship
                if S.drag == True:
                    S.drag_me(pygame.mouse.get_rel())
        ############################ events ####################################

        # checking the correct placement using set()
        #print j.center_count(b.dots)
        #print sumCenters(b.dots, shipList)
                
        # bottom surfaces first when blitting
        screen.blit(picture, (0, 0))    # cool ocean/battleship picture
        screen.blit(b.back, (0, 0))     # checkered tiles
        blitShips(shipList, screen)     # all 5 ships

        pygame.display.update()         # show 'em on screen

        clock.tick(fps)                 # frame rate cap

    '''------------------------ selection over ------------------------------'''

    # VARIABLES AT THIS POINT FOR TRANSITION TO BATTLE:
    # b             -> Board for user placement of Ships
    # b.dots        -> center dots [(x,y),...] on b
    # b.back        -> checkerboard from placement of Ships
    # shipList      -> list of 5 Ship classes
    # userBoard     -> [][]{} of board
    # userShipLL    -> TILE coordinates of ships
        
    # USER STUFF:--------
    # put all 17 (x,y) coords. into userBoard
    userBoard = create_board_list()                 # empty [][]{}
    userShipLL = []
    userShipLL = ship_shapes_to_shipLL(b.dots, shipList)
    userBoard = ships_to_board(userBoard, userShipLL)

    # COMP STUFF:--------
    # battle screen is created, placement one destroyed
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Battle Time!')

    # create checker board grid to click on
    myC1 = pygame.Color(120,0,150)
    myC2 = pygame.Color(140,140,140)
    checkerBoard = create_checker_board(25, 10, 10, myC1, myC2)

    # 4 options for tiles
    clips = pygame.image.load("clips.png")

    # create ships' locations, put in [L][L], then put in compBoard
    compShipLL = place_comp_ships()    
    compBoard = create_board_list()     # initializes values
    compBoard = ships_to_board(compBoard, compShipLL)   

    # battleship pictue background
    BGpic = pygame.image.load("Bship.jpg").convert()


    '''------------------------ battle time ---------------------------------'''

   
    # variables used for battle while loop
    winner = False
    compWins = False
    userWins = False
    userTurn = random.randrange(0, 2)   # pick who starts randomly T/F
    UDLR = random.randrange(0, 4)       # directions [0-3] for AI

    while(not winner):
        ############################ events ####################################
        for event in pygame.event.get():
            # quit game with X in corner or escape key
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # user plays, when it's his turn, must be in bounds and fresh
            # user_play function checks the validity of click
            if event.type == MOUSEBUTTONDOWN and userTurn == True:
                validClick = user_play(coord_to_idx(pygame.mouse.get_pos(), \
                    25, 250, 250), compBoard, compShipLL)
                if validClick == True:
                    userTurn = False
        ############################ events ####################################

        # check for sunks, update them
        userBoard = sunk_check(userShipLL, userBoard)

        # display the boards and tiles
        screen.blit(BGpic, (0,0))
        display_board(b.back, userBoard, screen, clips, 0, 0, shipList)
        display_board(checkerBoard, compBoard, screen, clips, 250, 250)
        pygame.display.update()

        # detect user winning
        if win_check(compBoard) == True:
            winner = True
            userWins = True  
            continue

        # comp plays when it's its turn
        if userTurn == False:
            clock.tick(2)        
            UDLR = comp_play(userBoard, userShipLL, UDLR)
            userTurn = True
            pygame.event.clear()            # for user clicks

        # detect if there's a winner
        if win_check(userBoard) == True:
            winner = True
            compWins = True
            continue

        # cap frame rate
        clock.tick(fps)
  

    '''------------------------ battle time over ----------------------------'''    

    # end of game loading pics, wait for quit or play again button click
    vicPic = pygame.image.load("victory.jpg").convert()
    lossPic = pygame.image.load("loser.jpg").convert()

    # selection for quit, or play again
    choiceMade = False
    playAgain = False

    while(choiceMade == False):
        ############################ events ####################################
        for event in pygame.event.get():
            # quit game with X in corner or escape key
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # for playing again
            if event.type == MOUSEBUTTONDOWN and \
                playAgainCheck(pygame.mouse.get_pos()) == True:
                choiceMade = True
                playAgain = True
        ############################ events ####################################

        # display winner, offer to play again!
        if compWins == True:
            # show the winning image
            screen.blit(lossPic, (0,0))
        else:
            # show losing image!
            screen.blit(vicPic, (0,0))

        # refresh screen, show final results
        display_board(b.back, userBoard, screen, clips, 0, 0, shipList)
        display_board(checkerBoard, compBoard, screen, clips, 250, 250)
        pygame.display.update()

    # to play again or not?  Recursively calls main() if replay==yes
    if playAgain == True:
        main()
    else:
        pygame.quit()
        sys.exit()

# calls main, runs the stuff
if __name__ == '__main__': main()


