import sys
import threading
import time

import pygame
from pygame.compat import xrange_

LOCK = threading.Lock()
surface = None


def create_surface():
    new_sfc = pygame.Surface((255, 255))

    ar = pygame.PixelArray(new_sfc)
    r, g, b = 0, 0, 0
    # Do some easy gradient effect.
    for y in xrange_(255):
        r, g, b = y // 2, y // 2, y
        ar[:, y] = (r, g, b)
    del ar

    return new_sfc


def flip_surface(sfc):
    ar = pygame.PixelArray(sfc)
    ar[:] = ar[:, ::-1]
    del ar


def main():
    global surface
    pygame.init()

    pygame.display.set_mode((255, 255))

    surface = create_surface()

    framerate = 20
    event_rate = 1 / framerate * 2
    update_rate = 1 / framerate

    t_up1 = t_ev1 = time.time()
    while True:
        t_up2 = time.time()
        t_ev2 = time.time()

        if t_up2 - t_up1 > update_rate:
            threading.Thread(target=update, daemon=True).start()
            t_up1 = t_up2

        if t_ev2 - t_ev1 > event_rate:
            event()
            t_ev1 = t_ev2


def update():
    global surface

    screen = pygame.display.get_surface()
    screen.fill((255, 255, 255))
    screen.blit(surface, (0, 0))
    pygame.display.flip()


def event():
    global surface, LOCK

    LOCK.acquire()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flip_surface(surface)

    LOCK.release()


if __name__ == '__main__':
    main()
