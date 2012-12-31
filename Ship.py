#!/usr/bin/env python

# Andrew Hoyle

import pygame, sys
from pygame.locals import *


# -5 of these will be dragged atop the Board to determine
#  the placement of ships for battle
class Ship:
    # colored rectangle at pos: xp, yp
    def __init__(self, xp, yp, w, l):
        # create surface, optimize somehow with convert()
        self.widt = w
        self.leng = l
        self.sur = pygame.Surface((w,l)).convert()

        # give me some color, gets over-colored by over_me()
        self.sur.fill((100,10,0))

        # keeps track of location for screen.blit()
        self.pos = self.sur.get_rect().move(xp, yp)

        # for clicking and dragging events
        self.over = False
        self.drag = False

    # is the mouse on top of me? set "over" bool
    def over_me(self, (xx,yy)):
        if self.pos.right > xx and self.pos.left < xx \
            and self.pos.top < yy and self.pos.bottom > yy:
            self.over = True
        else:
            self.over = False

        # change color based on mouse position
        if self.over == True:
            self.sur.fill((100,100,100))
        else:
            self.sur.fill((100,10,0))

    # move the object based on rel. mouse motion
    def drag_me(self, (rx,ry)):
        self.pos = self.pos.move(rx, ry)

    # returns the number of centers covered
    def center_count(self, centerList):
        _count = 0
        for i in range(len(centerList)):
            for j in range(len(centerList[i])):
                if self.pos.collidepoint(centerList[i][j]):
                    _count = _count + 1
        return _count

    # returns list of tuples of points engulfed
    def center_set(self, centerList):
        _lis = []
        for i in range(len(centerList)):
            for j in range(len(centerList[i])):
                if self.pos.collidepoint(centerList[i][j]):
                    _lis.append(centerList[i][j])
        return _lis

    # rotates CW 90 degrees about mouse drag point
    # messes up a little if you rotate A LOT while moving
    # added over conditional, so multiple can't get clicked
    def rot_me(self, (mx,my)):

        if self.over == True:
            _inX = mx - self.pos.left
            _inY = my - self.pos.top        

            self.sur = pygame.Surface((self.leng,self.widt)).convert()
            self.sur.fill((100,100,100))        

            self.pos = self.sur.get_rect().move \
            ( (mx - (self.leng - _inY)), (my - _inX) )

            # swap 'em for next rotation
            _l = self.leng
            self.leng = self.widt
            self.widt = _l


