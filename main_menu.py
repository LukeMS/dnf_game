import os

import pygame
"""..."""

import game
from game import Window
import gui
import level_main
import char_creation
import descriptions


class MainMenu(game.BaseScene):
    """..."""

    def __init__(self, game):
        """..."""
        super().__init__(game=game)
        self.selection = 0

        self.create_items()

        self.gui = gui.Menu(
            gfx=self.game.gfx, title="Caves & Lizards Roguelike",
            items=[item["text"] for item in self._menu])

        ((x, y), (x1, y1)) = self.gui.body_rect
        w = x1 - x
        h = y1 - y
        self.body_frame = Window(self, x, y, w, h)
        self.body_frame.set_margin(16)

    def on_update(self):
        """..."""
        #self.screen.fill((0, 255, 0))
        self.body_frame.on_update()
        self.gui.draw()

    def create_items(self):
        """..."""
        self._menu = [
            {
                "text": "Start a new journey",
                "kwargs": {
                    "scene": char_creation.Create,
                    "target": {
                        "scene": level_main.Main
                    }
                }
            },
            {
                "text": "Quick Battle",
                "kwargs": {
                    "scene": level_main.Main,
                    'new': True,
                    'mode': 'pit',
                }
            },
            {
                "text": "Load Game",
                "kwargs": {
                    "scene": level_main.Main,
                    'new': False
                }
            },
            {
                "text": "Tomes of Understanding",
                "kwargs": {
                    "scene": descriptions.Main
                }
            },
            {
                "text": "Options",
                "action": "quit",
                "kwargs": {}
            },
            {
                "text": "Quit",
                "action": "quit",
                "kwargs": {}
            }
        ]
        if not os.path.isdir('save'):
            # os.makedirs('save')
            self._menu.pop(1)

    def change_selection(self, value):
        """..."""
        self.selection += value
        self.selection = self.selection % len(self._menu)
        self.gui.select(self.selection)

    def on_key_press(self, event):
        """..."""
        if event.key == pygame.K_ESCAPE:
            self.quit()
        if event.key == pygame.K_UP:
            self.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            getattr(
                self.game,
                "set_scene"
            )(**self._menu[self.selection]['kwargs'])

    def clear(self):
        """..."""
        self.gui.clear()
        del self.gui

    def __getstate__(self):
        """..."""
        return None


if __name__ == '__main__':
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game.Game(
        scene=MainMenu, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
