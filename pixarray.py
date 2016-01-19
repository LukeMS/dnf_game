#!/usr/bin/env python
import os
import pygame
from pygame.compat import xrange_

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def show(image):
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            break


def main():
    pygame.init()

    pygame.display.set_mode((800, 600))
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)

    pygame.display.flip()

    # Create the PixelArray.
    ar = pygame.PixelArray(surface)
    r, g, b = 0, 0, 0
    # Do some easy gradient effect.
    for y in xrange_(600):
        scale = int(y / 600 * 255)
        scale = max(0, scale)
        scale = min(scale, 255)
        r, g, b = scale, scale, 255
        ar[:, y] = (r, g, b, 50)
    del ar
    show(surface)

    # We have made some gradient effect, now flip it.
    ar = pygame.PixelArray(surface)
    ar[:] = ar[:, ::-1]
    del ar
    show(surface)

if __name__ == '__main__':
    main()
