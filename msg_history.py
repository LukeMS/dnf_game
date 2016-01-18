import random

import pygame
from pygame import *

Font = None
"""
generates mumble jumble forever
"""

class MsgLog:
    ypos = 450

    def drawhistory(win, history):
        h = list(history)
        h.reverse()
        for line in h:
            r = win.blit(line, (10, ypos))
            # win.fill(0, (r.right, r.top, 620, r.height))
            ypos -= Font.get_height()


def main():
    init()

    win = display.set_mode((640, 480), RESIZABLE)
    display.set_caption("Mouse Focus Workout")

    global Font
    Font = font.Font(None, 26)

    history = []

    clock = pygame.time.Clock()

    going = True
    while going:
        for e in event.get():
            if e.type == QUIT:
                going = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    going = False

        txt = "".join([mumble() for x in range(
            5, random.randint(6, 36))])

        img = Font.render(txt, 1, (50, 200, 50), (0, 0, 0))
        history.append(img)
        history = history[-30:]

        drawhistory(win, history)

        display.flip()

        clock.tick(90)

    quit()


if __name__ == '__main__':
    main()
