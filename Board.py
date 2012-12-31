#!/usr/bin/env python

# Andrew Hoyle

import pygame, sys
from pygame.locals import *


# checker board pattern is created for playing the Ships
class Board:
    def __init__(self):
        self.over_count = 0;
        self.back = pygame.Surface((250,250)).convert()
        self.back.set_alpha(200)    # transparency to ocean, 0-255

        # get center dots for ship correct placement checking
        self.dots = []
        for i in range(10):
            _tempDots = []
            for j in range(10):
                _tempTuple = ( (i*25)+(((25+1)/2)), (j*25)+(((25+1)/2)) )
                _tempDots.append(_tempTuple)   
            self.dots.append(_tempDots)                         

        # draw tiles with alt. colors, put on back
        _theColor = True
        for i in range(10):
            for j in range(10):
                _tempSq = pygame.Surface((25,25)).convert()
                
                # coloration
                if _theColor == True:
                    _tempSq.fill((0,20,255))
                else:
                    _tempSq.fill((140,140,140))
                _theColor = not _theColor
                
                self.back.blit(_tempSq, (i*25,j*25))
            _theColor = not _theColor

