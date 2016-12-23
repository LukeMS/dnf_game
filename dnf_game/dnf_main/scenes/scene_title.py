"""..."""

import os

import sdl2

from dnf_game.dnf_main.scenes import (scene_descriptions, scene_creation,
                                      scene_map)
from dnf_game.scene_manager.layers.base_layers import Menu, ScrollingSubtitle
from dnf_game.scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_game.util import dnf_path


class SceneTitle(SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(draw_all=True, **kwargs)
        self.selection = 0

        self.create_items()

        self.menu_layer = Menu(
            parent=self,
            title="Dungeons and Fiends",
            items=[item["text"] for item in self._menu],
            background=True)

        self.subtitle_layer = ScrollingSubtitle(
            parent=self,
            subtitles=["a RPG-ish Roguelike...",
                       "maybe a roguelike-ish RPG?",
                       "definitely a roguelikelike!"],
            show_gap=False,
            frame_duration=5,
            step_x=20)

        [self.insert_layer(layer) for layer in [
            self.menu_layer, self.subtitle_layer]]

    def create_items(self):
        """..."""
        self._menu = [
            {
                "text": "Quick Battle",
                "kwargs": {
                    "scene": scene_map.SceneMap,
                    'new': True,
                    'mode': 'Pit',
                }
            },
            {
                "text": "Start a new journey",
                "kwargs": {
                    "scene": scene_creation.SceneCreation,
                    "target": {
                        "scene": scene_map.SceneMap
                    }
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
                    "scene": scene_descriptions.SceneDescriptions
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
        if not os.path.isdir(os.path.join(dnf_path(), 'save')):
            # os.makedirs('save')
            self._menu.pop(2)

    def change_selection(self, value):
        """..."""
        self.selection += value
        self.selection = self.selection % len(self._menu)
        self.menu_layer.select(self.selection)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_UP:
            self.change_selection(-1)
        elif sym == sdl2.SDLK_DOWN:
            self.change_selection(+1)
        elif sym == sdl2.SDLK_RETURN:
            self.manager.set_scene(**self._menu[self.selection]['kwargs'])
        print(self.menu_layer.visible)

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()


if __name__ == '__main__':
    from dnf_game.scene_manager import Manager
    Manager(scene=SceneTitle).execute()
