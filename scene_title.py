import os

import pygame
"""..."""

from manager.scenes import base_scenes
from manager.windows import base_windows
import scene_map
import char_creation
import descriptions


class MainMenu(base_scenes.SceneBase):
    """..."""

    def __init__(self):
        """..."""
        self.selection = 0

        self.create_items()

        self.menu_layer = base_windows.Menu(
            parent=self,
            title="Caves & Lizards Roguelike",
            items=[item["text"] for item in self._menu])

        self.menu_layer.add_item('New Item')
        self.menu_layer.remove_item('New Item')

    def on_update(self):
        """..."""
        # self.body_frame.on_update()
        self.menu_layer.draw()

    def create_items(self):
        """..."""
        self._menu = [
            {
                "text": "Start a new journey",
                "kwargs": {
                    "scene": char_creation.Create,
                    "target": {
                        "scene": scene_map.SceneMap
                    }
                }
            },
            {
                "text": "Quick Battle",
                "kwargs": {
                    "scene": scene_map.SceneMap,
                    'new': True,
                    'mode': 'pit',
                }
            },
            {
                "text": "Load Game",
                "kwargs": {
                    "scene": scene_map.SceneMap,
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
        self.menu_layer.select(self.selection)

    def on_key_press(self, event):
        """..."""
        if event.key == pygame.K_ESCAPE:
            self.quit()
        if event.key == pygame.K_UP:
            self.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            self.game.set_scene(**self._menu[self.selection]['kwargs'])

    def clear(self):
        """..."""
        self.menu_layer.clear()
        del self.menu_layer


if __name__ == '__main__':
    from manager import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT

    g = Game(scene=MainMenu,
             framerate=LIMIT_FPS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
