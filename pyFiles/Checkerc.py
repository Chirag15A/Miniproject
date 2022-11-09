
import pygame
import math
import main


class Checker:
    def __init__(self, iswhite, tale):
        self._iswhite = iswhite
        tale.placechecker(self)
        self.tale = tale
        self.cover = tale.copy()
        self.isplayable = True
        self.x = self.tale.x
        self.y = self.tale.y
        self.isvisible = True
        self.ishighlighted = False
        self.color = main.BLACK
        self.highlightsurface = pygame.Surface((40, 40))
        self.highlightsurface.fill(self.color)
        self.highlightsurface.set_alpha(0)
        if self._iswhite:
            self.image = pygame.image.load("White.png")
        else:
            self.image = pygame.image.load("Black.png")
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.image.set_alpha(255)#alpha value 255 means that it will be fully opaque
        self.playabletales = []
        self.isbeating = False
        self.isdamka = False
        self.canbeat = False
        self.pathlist = self.find_possible_tales(self.tale, True, True)

    def copy(self):
        return Checker(self._iswhite, self.tale)

    def find_possible_tales(self, st,
                            chi,
                            ok,
                            showweight = False):
        weight = []
        if not self.isdamka:
            path = []
            x = st.x
            y = st.y
            for i in [-1, 1]:
                for j in [-1, 1]:
                    possibletale = main.tales[x + i][y + j]
                    if possibletale._isplayable:
                        if possibletale.checker is None:
                            if chi:
                                if (self._iswhite and j < 0) or (not self._iswhite and j > 0):
                                    path.append(possibletale)
                        else:
                            if possibletale.checker._iswhite != self._iswhite and ok:
                                newpossibletale = main.tales[x + 2 * i][y + 2 * j]
                                if newpossibletale.checker is None and newpossibletale._isplayable:
                                    path.append(newpossibletale)
                                    weight.append(newpossibletale)
            finalpath = []
            main.add_content_from(path, finalpath)
            if len(finalpath) != 0:
                if showweight:
                    return [finalpath,weight]
                else:
                    return finalpath
            else:
                return None
        else:
            path = []
            x = st.x
            y = st.y
            maximumne = 6
            maximumse = 6
            maximumnw = 6
            maximumsw = 6
            for k in range(1, 7):
                for i in [-k, +k]:
                    for j in [-k, +k]:
                        if (i < 0 and j < 0 and k < maximumnw) or (i < 0 < j and k < maximumsw) or (
                                i > 0 and j > 0 and k < maximumse) or (
                                i > 0 > j and k < maximumne):
                            try:
                                possibletale = main.tales[x + i][y + j]
                                if possibletale._isplayable:
                                    if possibletale.checker is None:
                                        if chi:
                                            path.append(possibletale)
                                    else:
                                        if possibletale.checker._iswhite == self._iswhite:
                                            if i < 0 and j < 0:
                                                maximumnw = k - 1
                                            elif i < 0 and j > 0:
                                                maximumsw = k - 1
                                            elif i > 0 and j > 0:
                                                maximumse = k - 1
                                            elif i > 0 and j < 0:
                                                maximumne = k - 1
                                        if possibletale.checker._iswhite != self._iswhite and ok:
                                            newpossibletale = main.tales[int(x + (k + 1) * i / abs(i))][
                                                int(y + (k + 1) * j / abs(j))]
                                            if newpossibletale.checker is None and newpossibletale._isplayable:
                                                path.append(newpossibletale)
                                            else:
                                                if i < 0 and j < 0:
                                                    maximumnw = k - 1
                                                elif i < 0 and j > 0:
                                                    maximumsw = k - 1
                                                elif i > 0 and j > 0:
                                                    maximumse = k - 1
                                                elif i > 0 and j < 0:
                                                    maximumne = k - 1
                            except IndexError:
                                if i < 0 and j < 0:
                                    maximumnw = k
                                elif i < 0 and j > 0:
                                    maximumsw = k
                                elif i > 0 and j > 0:
                                    maximumse = k
                                elif i > 0 and j < 0:
                                    maximumne = k
            finalpath = []
            main.add_content_from(path, finalpath)
            if len(finalpath) != 0:
                if showweight:
                    return [finalpath, weight]
                else:
                    return finalpath
            else:
                return None

    def hide(self):
        if self.isvisible:
            self.isvisible = False

    def show(self):
        if not self.isvisible:
            self.isvisible = True

    def getridof(self):
        if self.isplayable:
            self.isplayable = False

    def highlight(self, color):
        if not self.ishighlighted:
            self.color = color
            self.ishighlighted = True

    def unhighlight(self):
        if self.ishighlighted:
            self.ishighlighted = False

    def move(self, totale):
        self.tale.checker = None
        self.tale = totale
        self.tale.placechecker(self)
        self.x = self.tale.x
        self.y = self.tale.y
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))

    def bebeaten(self):
        global whites
        global blacks
        if self._iswhite:
            for i in whites:
                if i == self:
                    whites.remove(i)
        else:
            for i in blacks:
                if i == self:
                    blacks.remove(i)
        self.tale.checker = None
        self.tale = main.tales[0][0]
        self.cover = self.tale.copy()
        self.tale.placechecker(self)
        self.x = self.tale.x
        self.y = self.tale.y
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.isplayable = False
        self.hide()

    def beat(self, beaten_checker):
        deltax, deltay = beaten_checker.x - self.x, beaten_checker.y - self.y
        self.move(main.tales[int(self.x + (abs(deltax) + 1) * deltax / abs(deltax))][
                      int(self.y + (abs(deltay) + 1) * deltay / abs(deltay))])
        beaten_checker.bebeaten()
        if self.isdamka:
            self.justbeated = True

    def makeaturn(self, tale):
        global whitesturn
        if self.isdamka:
            if self._iswhite == whitesturn:
                possibletale = None
                for i in self.pathlist:
                    if tale == i:
                        possibletale = i
                if possibletale is not None:
                    deltax = (tale.x - self.x) / abs(tale.x - self.x)
                    deltay = (tale.y - self.y) / abs(tale.y - self.y)
                    beatentale = None
                    for i in range(1, abs(tale.x - self.x)+1):
                        maybetale = main.tales[int(self.x + deltax * i)][int(self.y + deltay * i)]
                        if maybetale.checker is not None:
                            if maybetale.checker._iswhite != self._iswhite:
                                if beatentale is None:
                                    beatentale = maybetale
                    if beatentale is None:
                        canbeat = False
                    else:
                        canbeat = True
                    if not canbeat:
                        self.move(possibletale)
                        whitesturn = not whitesturn
                    elif canbeat:
                        if possibletale.checker is None:
                            if beatentale is not None:
                                if beatentale.x <= main.tales[int(tale.x - deltax)][int(tale.y - deltay)].x:
                                    self.beat(beatentale.checker)
                                    self.isbeating = True
                                    self.update()
                                    if self.pathlist is None:
                                        self.isbeating = False
                                        self.justbeated = False
                                        whitesturn = not whitesturn
        else:
            if self._iswhite == whitesturn and self.pathlist is not None:
                possibletale = None
                for i in self.pathlist:
                    if tale == i:
                        possibletale = i
                if possibletale is not None:
                    if abs(possibletale.x - self.x) == 1:
                        self.move(possibletale)
                        self.maybebecomedamka()
                        whitesturn = not whitesturn
                    elif abs(possibletale.x - self.x) == 2:
                        self.beat(main.tales[int((possibletale.x + self.x) / 2)][int((possibletale.y + self.y) / 2)].checker)
                        self.isbeating = True
                        self.maybebecomedamka()
                        self.update()
                        if self.pathlist is None:
                            self.isbeating = False
                            whitesturn = not whitesturn


    def maybebecomedamka(self):
        if (self.tale.y == 1 and self._iswhite) or (self.tale.y == 8 and not self._iswhite):
            self.isdamka = True
            if self._iswhite:
                self.image = pygame.image.load("WhiteDamka.png")
            else:
                self.image = pygame.image.load("BlackDamka.png")

    def update(self):
        if self.isplayable:
            if self.isvisible:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.cover.image.set_alpha(255 - main.OPACITY)
                else:
                    self.cover.image.set_alpha(0)
            else:
                self.cover.image.set_alpha(255)
            if self.ishighlighted:
                self.highlightsurface.fill(self.color)
                self.highlightsurface.set_alpha(255 - main.OPACITY)
            else:
                self.highlightsurface.set_alpha(0)
            if not self.isbeating:
                self.pathlist = self.find_possible_tales(self.tale, True, True)
            else:
                self.pathlist = self.find_possible_tales(self.tale, False, True)
            main.screen.blit(self.image, self.rect)
            main.screen.blit(self.cover.image, self.rect)
            main.screen.blit(self.highlightsurface, self.rect)
        else:
            self.cover.image.set_alpha(255)
            main.screen.blit(self.cover.image, self.rect)

    def __eq__(self, other):
        if (other.x, other.y, other._iswhite) == (self.x, self.y, self._iswhite):
            return True
        else:
            return False