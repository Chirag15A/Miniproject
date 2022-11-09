import pygame
import math
import Checkerc
import Talec



#//defining the variabales that are to be used in the class


FPS = 60
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
LIGHTROSE = (255, 209, 220)
LIGHTPURPLE = (230, 198, 136)
BLACK = (0, 0, 0)
OPACITY = 155


#/// this is an empty list and will append the elements in the content
def add_content_from(listfrom, listto):
    content = []
    for i in listfrom:
        if type(i) == list:
            add_content_from(i, content)
        else:
            content.append(i)
    for i in content:
        listto.append(i)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 400))
tales = []
pygame.display.set_caption("Checkers")
whitesturn = True
firstclick = True
playingchecker = None
wrongtale = None
whitewins = None
for i in range(10):
    row = []
    for j in range(10):
        if i == 0 or i == 9 or j == 0 or j == 9:
            newtale = Talec.Tale(i, j, True, False)
        else:
            if i % 2 == j % 2:
                newtale = Talec.Tale(i, j, True)
            else:
                newtale = Talec.Tale(i, j, False)
            newtale.show()
        row.append(newtale)
    tales.append(row)
whites = []
blacks = []
clock = pygame.time.Clock()
for i in range(1, 5):
    for j in range(6, 9):
        if j % 2 == 1:
            newwhitechecker = Checkerc.Checker(True, tales[2 * i][j])
        else:
            newwhitechecker = Checkerc(True, tales[2 * i - 1][j])
        whites.append(newwhitechecker)

for i in range(1, 5):
    for j in range(1, 4):
        if j % 2 != 1:
            newblackchecker = Checkerc(False, tales[2 * i - 1][j])
        else:
            newblackchecker = Checkerc(False, tales[2 * i][j])
        blacks.append(newblackchecker)

running1 = True
# mainloops
while running1:
    clock.tick(FPS)
    # events
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running1 = False
        # tracking mouse position
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        # clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.button == 1:
                clicked_tale = Talec(math.floor(mousex / 40), math.floor(mousey / 40), True, True)
                for i in tales:
                    for j in i:
                        if clicked_tale == j:
                            clicked_tale = j
                if firstclick:
                    if clicked_tale.checker is not None:
                        playingchecker = clicked_tale.checker
                        if playingchecker._iswhite == whitesturn:
                            playingchecker.highlight(GRAY)
                            if playingchecker.pathlist is not None:
                                for i in playingchecker.pathlist:
                                    i.highlight(GREEN)
                        else:
                            playingchecker.highlight(RED)
                        firstclick = False
                else:
                    if playingchecker.pathlist is not None:
                        for i in playingchecker.pathlist:
                            i.unhighlight()
                    if wrongtale is not None:
                        wrongtale.unhighlight()
                    if playingchecker.pathlist is not None:
                        if clicked_tale not in playingchecker.pathlist:
                            wrongtale = clicked_tale
                            wrongtale.highlight(RED)
                    playingchecker.makeaturn(clicked_tale)
                    if playingchecker.pathlist is not None:
                        for i in playingchecker.pathlist:
                            i.highlight(GREEN)
                    if not playingchecker.isbeating:
                        firstclick = True
                        playingchecker.unhighlight()
                        if playingchecker.pathlist is not None:
                            for i in playingchecker.pathlist:
                                i.unhighlight()

    # updates+rendering
    screen.fill(LIGHTROSE)
    for i in tales:
        for j in i:
            j.update()
    for i in whites:
        i.update()
    for i in blacks:
        i.update()
    pygame.draw.rect(screen, BLACK, (40, 40, 320, 320), 1)
    # global update
    pygame.display.flip()
    # endgame
    if len(whites) == 0:
        whitewins = False
        running1 = False
    elif len(blacks) == 0:
        whitewins = True
        running1 = False

if whitewins:
    print("Congratulations Player1!")
else:
    print("Congratulations Player2!")
