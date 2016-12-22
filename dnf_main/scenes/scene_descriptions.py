"""..."""
import os

import sdl2

from dnf_game.util import packer
from dnf_game.util.ext.rect import Rect
from dnf_game.util.sftext import SFText
from dnf_game.scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_game.scene_manager.layers.base_layers import Layer

WHITE = "{color (255, 255, 255)}"
YELLOW = "{color (255, 255, 0)}"


class LayerNavigator(Layer):
    """..."""

    def __init__(self, tab_y=10, **kwargs):
        """..."""
        super().__init__(**kwargs)

        self.db = self.parent.db
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
        # self.height = self.sftext.sum_height()
        # self.y = 0
        header_rect = Rect(self)
        header_rect.y = 0
        header_rect.height = self.sftext.sum_height()
        self.parent.desc_layer.create_text(header_rect=header_rect)

    def create_text(self, text):
        """..."""
        manager = self.manager
        nav_style = "{size 18}" + WHITE
        self.sftext = SFText(text=text, style=nav_style, rect=self,
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
        super().on_update()
        self.sftext.on_update()

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
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


class LayerDescription(Layer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)

        self.content = ""

        self.db = self.parent.db

        self.create_text()

    def create_text(self, header_rect=None):
        """..."""
        try:
            tab = self.sftext.default_style['h'] * 2
        except AttributeError:
            tab = 6

        manager = self.manager

        y = header_rect.bottom + tab if header_rect else self.y
        self.y = y
        self.height = self.parent.height - self.y

        self.sftext = SFText(text=self.content, rect=self,
                             fonts=manager.fonts, manager=manager)

    def on_update(self):
        """..."""
        super().on_update()
        self.sftext.on_update()

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        self.sftext.on_key_press(event, mod)

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        self.sftext.on_mouse_scroll(event, offset_x, offset_y)


class SceneDescriptions(SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(draw_all=True)
        _path = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        fname = os.path.join(_path, 'descriptions.bzp')
        self.db = packer.unpack_json(fname)

        self.create_layers()
        self.nav_layer.list()

    def create_layers(self):
        """..."""
        nav_rect = Rect(0,  # left
                        0,  # top
                        self.width,  # width
                        self.height // 4)  # height
        self.nav_layer = LayerNavigator(parent=self, rect=nav_rect)
        self.insert_layer(self.nav_layer)
        # print(nav_rect.bottom)
        desc_rect = Rect(0,  # left
                         nav_rect.bottom,  # top
                         self.width,  # width
                         self.height - nav_rect.height)  # height
        self.desc_layer = LayerDescription(parent=self, rect=desc_rect)
        self.insert_layer(self.desc_layer)

    def insert_layer(self, obj):
        """..."""
        self.layers.append(obj)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()
        elif event.key.keysym.sym in [sdl2.SDLK_PAGEUP, sdl2.SDLK_PAGEDOWN,
                                      sdl2.SDLK_HOME, sdl2.SDLK_END]:
            self.desc_layer.on_key_press(event, mod)
        else:
            self.nav_layer.on_key_press(event, mod)

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        self.desc_layer.on_mouse_scroll(event, offset_x, offset_y)

    def on_update(self):
        """..."""
        super().on_update()

if __name__ == '__main__':
    from dnf_game.scene_manager import Manager

    Manager(scene=SceneDescriptions).execute()
