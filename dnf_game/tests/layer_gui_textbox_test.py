"""Text box example use."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pygooey
import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 400))
screen_rect = screen.get_rect()
done = False


def print_on_enter(id, final):
    """Sample callback function that prints a message to the screen."""
    print('enter pressed, textbox contains {}'.format(final))

# see all settings help(pygooey.TextBox.__init__)
settings = {
    "command": print_on_enter,
    "inactive_on_enter": False,
}
entry = pygooey.TextBox(rect=(70, 100, 150, 30), **settings)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        entry.get_event(event)
    entry.update()
    entry.draw(screen)
    pg.display.update()
