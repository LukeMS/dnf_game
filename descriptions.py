"""..."""
import os
import sys

import sdl2

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game_types import Rect
from sftext.sftext import SFText
from common import packer
from manager.scenes import base_scenes
from manager.windows import base_windows

WHITE = "{color (255, 255, 255)}"
YELLOW = "{color (255, 255, 0)}"


class Navigator(base_windows.Layer):
    """..."""

    def __init__(self, parent, rect, tab_y=10):
        """..."""
        self.db = parent.db

        self.width = rect.width
        self.height = rect.height
        self.x = rect.x
        self.y = rect.y
        self.rect = rect

        self.create_solid_surface()
        self.create_text("")

        self.abs_position = []
        self.key_index_historic = []
        self.current_level = dict(self.db)
        self.previous_level = dict(self.current_level)
        self.keys = sorted(list(self.current_level.keys()))
        self.current_key_index = 0

    def list(self):
        """..."""
        current_key = self.keys[self.current_key_index]
        current_item = self.current_level[current_key]

        document = ("{style}\\" * 2)
        for i in range(len(self.abs_position)):
            level = self.abs_position[i].capitalize()
            if i > 0:
                document += "\\"
            document += level

        str_keys = []
        for i, key in enumerate(self.keys):

            if isinstance(self.current_level[key], dict):
                s = "[{}]".format(key.capitalize())
            else:
                s = key.capitalize()

            if key == current_key:
                s = "{style}{underline True}" + YELLOW + s.upper() + "{style}"

            str_keys.append(s)

        document += "\n[ {} ]".format(", ".join(s for s in str_keys))

        self.create_text(document)

        if isinstance(current_item, dict):
            self.parent.desc_layer.content = self.db['Help']
        else:
            self.parent.desc_layer.content = current_item
        self.parent.desc_layer.create_text(
            header_size=self.sftext.sum_height())

    def create_text(self, text):
        """..."""
        manager = self.manager
        nav_style = "{size 18}" + WHITE
        self.sftext = SFText(text=text, style=nav_style, rect=self.rect,
                             fonts=manager.fonts, manager=manager)

    def previous_item(self):
        """..."""
        self.current_key_index -= 1
        self.current_key_index = self.current_key_index % len(self.keys)
        self.list()

    def next_item(self):
        """..."""
        self.current_key_index += 1
        self.current_key_index = self.current_key_index % len(self.keys)
        self.list()

    def go_down(self):
        """..."""
        current_item = self.current_level[self.keys[self.current_key_index]]
        if isinstance(current_item, dict):
            current_key = self.keys[self.current_key_index]
            self.abs_position.append(current_key)

            self.previous_level = dict(self.current_level)
            self.current_level = dict(self.current_level[current_key])
            self.keys = sorted(list(self.current_level.keys()))

            self.key_index_historic.append(self.current_key_index)
            self.current_key_index = 0
            self.list()

    def go_up(self):
        """..."""
        if len(self.abs_position) > 0:
            self.abs_position.pop()
            self.current_key_index = self.key_index_historic.pop()

            self.current_level = self.fetch_previous()
            self.keys = sorted(list(self.current_level.keys()))

            self.list()

    def fetch_previous(self):
        """..."""
        previous = dict(self.db)
        abs_path = list(self.abs_position)
        for key in abs_path:
            previous = dict(previous[abs_path.pop(0)])
        return previous

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.surface)
        self.sftext.on_update()

    def on_key_press(self, event):
        """..."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_LEFT:
            self.previous_item()
        elif sym == sdl2.SDLK_RIGHT:
            self.next_item()
        elif sym == sdl2.SDLK_BACKSPACE:
            self.go_up()
        elif sym == sdl2.SDLK_RETURN:
            self.go_down()
        else:
            if 97 <= sym <= 122:
                self.search(chr(sym))

    def search(self, _s):
        """Search for a key that matches the imput."""
        def set_i(i):
            self.current_key_index = i
            self.list()

        s = _s.lower()
        matches = []
        for i in range(len(self.keys)):
            if self.keys[i][0].lower() == s:
                matches.append(i)

        if not matches:
            return
        elif len(matches) == 1:
            set_i(matches[0])
        elif self.current_key_index in matches:
            cur_i = matches.index(self.current_key_index)
            j = (cur_i + 1) % len(matches)
            set_i(matches[j])
        else:
            set_i(matches[0])


class Description(base_windows.Layer):
    """..."""

    def __init__(self, parent, rect):
        """..."""
        super().__init__(parent=parent)

        self.content = ""

        self.width = rect.width
        self.height = rect.height
        self.x = rect.x
        self.y = rect.y
        self.rect = rect

        self.db = parent.db

        self.create_solid_surface()
        self.create_text()

    def create_text(self, header_size=None):
        """..."""
        try:
            tab = self.sftext.default_style['h'] * 2
        except AttributeError:
            tab = 6

        manager = self.manager

        y = header_size + tab if header_size else self.y
        self.rect.y = y

        # DEPRE -> rect.height adjusted at initialization.
        # self.rect.height = (self.screen.get_height() - self.rect.y)

        self.sftext = SFText(text=self.content, rect=self.rect,
                             fonts=manager.fonts, manager=manager)

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.surface)
        self.sftext.on_update()

    def on_key_press(self, event):
        """..."""
        self.sftext.on_key_press(event)

    def on_mouse_scroll(self, event):
        """..."""
        self.sftext.on_mouse_scroll(event)


class Main(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(draw_all=True)

        self.db = packer.unpack_json(os.path.join('data', 'descriptions.bzp'))

        self.create_layers()
        self.nav_layer.list()

    def create_layers(self):
        """..."""
        nav_rect = Rect(0,  # left
                        0,  # top
                        self.width,  # width
                        int(self.height * 0.15))  # height
        self.nav_layer = Navigator(parent=self, rect=nav_rect)
        self.insert_layer(self.nav_layer)
        # print(nav_rect.bottom)
        desc_rect = Rect(0,  # left
                         nav_rect.bottom,  # top
                         self.width,  # width
                         self.height - nav_rect.height)  # height
        self.desc_layer = Description(parent=self, rect=desc_rect)
        self.insert_layer(self.desc_layer)

    def insert_layer(self, obj):
        """..."""
        self.layers.append(obj)

    def on_key_press(self, event):
        """..."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()
        elif event.key.keysym.sym in [sdl2.SDLK_PAGEUP, sdl2.SDLK_PAGEDOWN,
                                      sdl2.SDLK_HOME, sdl2.SDLK_END]:
            self.desc_layer.on_key_press(event)
        else:
            self.nav_layer.on_key_press(event)

    def on_mouse_scroll(self, event):
        """..."""
        self.desc_layer.on_mouse_scroll(event)

    def on_update(self):
        """..."""
        super().on_update()

if __name__ == '__main__':
    from manager import Manager

    Manager(scene=Main).execute()
