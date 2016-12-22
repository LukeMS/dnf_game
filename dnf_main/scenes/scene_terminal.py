"""..."""

import os
import sys

import sdl2

WP = os.path.join(os.path.dirname(__file__), '..', '..')
if __name__ == '__main__':
    sys.path.insert(0, WP)
from dnf_main.scenes import scene_map
from scene_manager.scenes import base_scenes
from scene_manager import Manager
from util import Font, Rect


class Terminal(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)

        self.font = Font(name='PressStart2P-Regular.ttf', font_size=12,
                         renderer=self.fonts,
                         color=(127, 255, 127, 255))
        self.font_w, self.font_h = w, h = self.font.get_size("A")
        self.cols = (self.width - 8) // w
        self.rows = (self.height - 8) // h
        print(self.width, self.cols, self.height, self.rows)
        self.text = '#' * self.cols
        self.previous_text = self.text
        self.sprites = []

    def render_sprites(self):
        """..."""
        def position(i):
            return (4, i * self.font_h + 4)

        def valid(pos):
            x, y = pos
            scr_w, scr_h = self.width, self.height
            return x < scr_w and y < scr_h

        if self.sprites and self.previous_text == self.text:
            return
        text = self.get_text()
        render = self.font.render

        self.sprites = [render(t, rect=Rect(position(i), (0, 0)))
                        for i, t in enumerate(text)
                        if t and valid(position(i))]

        self.previous_text = self.text

    def render_sprites_w(self):
        """..."""
        if self.sprites and self.previous_text == self.text:
            return
        text = self.text
        render = self.font.render_w
        self.sprites = [render(text, wrap=self.width - 4)]

    def on_update(self):
        """..."""
        self.render_sprites()
        self.manager.spriterenderer.render(sprites=self.sprites)

    def get_text(self):
        """..."""
        text = self.text

        l = []
        start = 0
        end = 0
        while True:
            if (end % (self.cols - 2) == 0 or
                    text[end] == "\n" or
                    end == len(text) - 1):
                l.append(text[start:end])
                start = end
            if end == len(text) - 1:
                break
            end += 1
        return l

    @staticmethod
    def test():
        """..."""
        m = Manager(scene=Terminal, framerate=10,
                    width=1024, height=768, show_fps=False)
        m._scene.text = """[path: C:/Program Files/minisphere;C:/Program Files/Common Files/Microsoft Shared/Windows Live;C:/Program Files (x86)/Common Files/Microsoft Shared/Windows Live;C:/Python34/Lib/site-packages/PyQt4;C:/Python34/;C:/Python34/Scripts;C:/Program Files/ImageMagick-6.9.1-Q16;C:/ProgramData/Oracle/Java/javapath;C:/Windows/system32;C:/Windows;C:/Windows/System32/Wbem;C:/Windows/System32/WindowsPowerShell/v1.0/;C:/Program Files (x86)/ATI Technologies/ATI.ACE/Core-Static;C:/Program Files (x86)/AMD/ATI.ACE/Core-Static;C:/Program Files (x86)/Autodesk/Backburner/;C:/Program Files/Common Files/Autodesk Shared/;C:/Program Files (x86)/Shoes;C:/Program Files (x86)/Two Pilots/PDF2Text Pilot/;C:/Program Files (x86)/Git/cmd;C:/Program Files (x86)/Windows Live/Shared;C:/Program Files (x86)/Bazaar;C:/Program Files (x86)/File Viewer Lite/lib/magick;C:/Program Files (x86)/QuickTime/QTSystem/;C:/Program Files (x86)/infogridpacific/AZARDI/bin;C:/Program Files (x86)/infogridpacific/AZARDI/bin;C:/Program Files/Calibre2/;C:/ProgramData/chocolatey/bin;C:/Program Files (x86)/Windows Kits/8.1/Windows Performance Toolkit/;C:/c/lib/SDL2-2.0.4--mingw32/bin;C:/c/lib/SFML_2.3.2-GCC_4.9.2/bin;C:/Python35-32/Scripts;C:/Python35-32;C:/cc/cpplint;C:/cc/cppcheck;C:/Program Files (x86)/CodeBlocks/MinGW/bin;C:/Users/Lucas/Documents/batch/bin;C:/Ruby21-x64/bin;C:/Ruby21-x64/sqlite3/bin;C:/Program Files (x86)/Common Files/Hackety Hack/0.r1529/..]"""
        m.execute()


class TerminalGrid(Terminal):
    """..."""

    add_obj = scene_map.SceneMap.add_obj
    rem_obj = scene_map.SceneMap.rem_obj

    def __init__(self, *, map_gen, **kwargs):
        """..."""
        super().__init__()
        self.font = Font(name='PressStart2P-Regular.ttf', font_size=8,
                         renderer=self.manager.fonts)
        self.w, self.h = w, h = self.font.get_size('A')
        self.cols = (self.width - 8) // w
        self.rows = (self.height - 8) // h
        self.text = '#' * self.cols
        map_gen.terminal = self
        self.map_gen = map_gen
        map_gen.run_test()

    @property
    def current_level(self):
        """..."""
        return self.map_gen.map

    def manual_update(self):
        """..."""
        self.manager.renderer.clear()
        self.on_update()
        self.manager.present()

    def on_update(self):
        """..."""
        _map = self.map_gen.map
        font_render = self.font.render
        batch = [font_render(chr(tile.id),
                             color=tile.color,
                             rect=Rect((4 + self.w * x, y * self.h), (0, 0)))
                 for (x, y), tile_group in _map.items()
                 for tile in tile_group.get_all()
                 if tile]
        self.manager.spriterenderer.render(sprites=batch)
        return
        for (x, y), tile_group in _map.items():
            for tile in tile_group.get_all():
                if not tile:
                    continue
                char = chr(tile.id)
                color = tile.color
                img = self.font.render(char, True, color)
                self.screen.blit(img, (4 + self.w * x, y * self.h))

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()


class SurfaceGrid(TerminalGrid):
    """..."""

    wrap = False
    offset = 0, 0
    scroll_k = 5
    ignore_regular_update = True

    def get_pos(self, x, y):
        """Handle wrapping."""
        if self.wrap:
            return x % self.cols, y % self.rows
        else:
            return x, y

    def on_update(self):
        """..."""
        _map = self.map_gen.map
        for (x, y), tile in _map.items():
            if x < self.offset[0] or y < self.offset[1]:
                continue
            char = chr(tile.feature.id)
            color = tile.feature.color
            img = self.font.render(char, True, color)
            self.screen.blit(img, (4 + self.w * (x - self.offset[0]),
                                   (y - self.offset[1]) * self.h))

    def scroll(self, x, y):
        """Adjust offset for screen scrolling."""
        offset = list(self.offset)
        offset[0] += x
        offset[1] += y

        offset[0] = min(self.map_gen.map.cols - self.cols, offset[0])
        offset[0] = max(0, offset[0])

        offset[1] = min(self.map_gen.map.rows - self.rows, offset[1])
        offset[1] = max(1, offset[1])

        self.offset = tuple(offset)

    def on_key_press(self, event):
        """Handle key presses input for the level."""
        """
        print("SurfaceGrid.on_key_press")
        print("offset:", self.offset,
              "cols:", self.cols,
              "rows:", self.rows)
        """
        if event.key == pygame.K_ESCAPE:
                self.quit()
        elif event.key in [pygame.K_UP, pygame.K_KP8]:
            self.scroll(0, -1)
        elif event.key in [pygame.K_KP9]:
            self.scroll(1, -1)
        elif event.key in [pygame.K_RIGHT, pygame.K_KP6]:
            self.scroll(1, 0)
        elif event.key in [pygame.K_KP3]:
            self.scroll(1, 1)
        elif event.key in [pygame.K_DOWN, pygame.K_KP2]:
            self.scroll(0, 1)
        elif event.key in [pygame.K_KP1]:
            self.scroll(-1, 1)
        elif event.key in [pygame.K_LEFT, pygame.K_KP4]:
            self.scroll(-1, 0)
        self.manual_update()

    def on_mouse_scroll(self, event):
        """Handle mouse scroll input for the level."""
        k = self.scroll_k
        keys = pygame.key.get_pressed()

        ctrl = keys[pygame.K_LCTRL]

        if event.button == 4:
            if ctrl:
                self.scroll(-k, 0)
            else:
                self.scroll(0, -k)
        elif event.button == 5:
            if ctrl:
                self.scroll(k, 0)
            else:
                self.scroll(0, k)
        self.manual_update()


class SurfaceTiledGrid(TerminalGrid):
    """Tile-based Grid for surface maps."""

    def __init__(self, game, **kwargs):
        """Initialization."""
        super().__init__(game, **kwargs)

        self.text = '#' * self.cols
        self.wrap = False
        self.offset = 0, 0
        self.scroll_k = 3

        path = os.path.join(os.path.dirname(__file__), "resources", "fonts")
        self.fonts = resources.Fonts(path=path)

        self.set_font()

    def set_font(self):
        """Select a font type and size.

        Screen size in chars (cols and rows) is based on this font."""
        self.font = self.fonts.load('Cousine-Bold.ttf', 14)

        self.w, self.h = w, h = self.font.size(' ')
        self.cols = (self.width - 8) // w
        self.rows = (self.height - 8) // h

    def on_update(self):
        """..."""
        def draw(tile):
            txt = chr(tile.id)
            clr = tile.color
            return self.font.render(txt, True, clr)

        font_w = self.w
        font_h = self.h

        self.screen.fill((0, 0, 0))
        x0, y0 = self.offset
        x1 = min(x0 + self.cols, self.map_w)
        y1 = min(y0 + self.rows, self.map_h)

        [self.screen.blit(draw(v), ((x - x0) * font_w + 4,
                                    (y - y0) * font_h))
         for (x, y), v in self.map.items()
         if x0 <= x < x1 and y0 <= y < y1]

        pygame.display.flip()

    def draw(self, grid, grid_w, grid_h):
        """..."""
        self.on_update()

    def get_pos(self, x, y):
        """Handle wrapping."""
        if self.wrap:
            return x % self.cols, y % self.rows
        else:
            return x, y

    def scroll(self, x, y):
        """Adjust offset for screen scrolling."""
        offset = list(self.offset)
        offset[0] += x
        offset[1] += y

        offset[0] = min(self.map_w - self.cols, offset[0])
        offset[0] = max(0, offset[0])

        offset[1] = min(self.map_h - self.rows, offset[1])
        offset[1] = max(1, offset[1])

        self.offset = tuple(offset)

    def on_key_press(self, event):
        """Handle key presses input for the level."""
        """
        print("SurfaceGrid.on_key_press")
        print("offset:", self.offset,
              "cols:", self.cols,
              "rows:", self.rows)
        """
        if event.key == pygame.K_ESCAPE:
                self.quit()
        elif event.key in [pygame.K_UP, pygame.K_KP8]:
            self.scroll(0, -1)
        elif event.key in [pygame.K_KP9]:
            self.scroll(1, -1)
        elif event.key in [pygame.K_RIGHT, pygame.K_KP6]:
            self.scroll(1, 0)
        elif event.key in [pygame.K_KP3]:
            self.scroll(1, 1)
        elif event.key in [pygame.K_DOWN, pygame.K_KP2]:
            self.scroll(0, 1)
        elif event.key in [pygame.K_KP1]:
            self.scroll(-1, 1)
        elif event.key in [pygame.K_LEFT, pygame.K_KP4]:
            self.scroll(-1, 0)
        self.print()

    def on_mouse_scroll(self, event):
        """Handle mouse scroll input for the level."""
        k = self.scroll_k
        keys = pygame.key.get_pressed()

        ctrl = keys[pygame.K_LCTRL]

        if event.button == 4:
            if ctrl:
                self.scroll(-k, 0)
            else:
                self.scroll(0, -k)
        elif event.button == 5:
            if ctrl:
                self.scroll(k, 0)
            else:
                self.scroll(0, k)
        self.print()

if __name__ == '__main__':
    Terminal.test()
