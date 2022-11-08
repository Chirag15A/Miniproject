import pygame
import math
import main

#//defining the variabales that are to be used in the class



class Tale:
    def __init__(self, x, y, iswhite, isplayable=True):
        self.x = x
        self.y = y
        self._iswhite = iswhite
        self._isplayable = isplayable
        self.checker = None
        self._isvisible = False
        if self._iswhite:
            self.image = pygame.image.load("LightTale.png")
        else:
            self.image = pygame.image.load("DarkTale.png")
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.color = main.GRAY
        self.ishighlighted = False
        self.highlightsurface = pygame.Surface((40, 40))
        self.highlightsurface.fill(self.color)
        self.highlightsurface.set_alpha(0)
#//////////////////////////////////////////////
    def update(self):
        if self._isplayable:
            if self._isvisible:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image.set_alpha(main.OPACITY)
                else:
                    self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        if self.ishighlighted:
            self.highlightsurface.fill(self.color)
            self.highlightsurface.set_alpha(255 - main.OPACITY)
        else:
            self.highlightsurface.set_alpha(0)
        main.screen.blit(self.image, self.rect)
        main.blit(self.highlightsurface, (self.x * 40, self.y * 40))
#///////////////////////////////////////
    def show(self):
        self._isvisible = True

    def hide(self):
        self._isvisible = False

    def placechecker(self, checker):
        if self.checker is None:
            self.checker = checker

    def removechecker(self):
        if self.checker is not None:
            self.checker = None

    def copy(self):
        return Tale(self.x, self.y, self._iswhite, self._isplayable)

    def highlight(self, color):
        if not self.ishighlighted:
            self.color = color
            self.ishighlighted = True

    def unhighlight(self):
        if self.ishighlighted:
            self.color = None
            self.ishighlighted = False

    def __eq__(self, other):
        if type(other)!=Tale:
            return False
        elif (other.x, other.y) == (self.x, self.y):
            return True
        else:
            return False
#////////////////////////////////////
