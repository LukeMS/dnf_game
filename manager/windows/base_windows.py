"""..."""
import os

import pygame
from pygame.compat import xrange_

from manager.scenes import base_scenes
from constants import GAME_COLORS


class Layer(base_scenes.SceneBase):
    """..."""

    bottom_color = (15, 15, 31)
    top_color = (0, 0, 0)

    def __init__(self, *, parent):
        """..."""
        self.parent = parent

    @property
    def cols(self):
        """..."""
        return self._cols

    @cols.setter
    def cols(self, value):
        self._cols = value

    @property
    def rows(self):
        """..."""
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def on_update(self):
        """..."""
        # print("{}.on_update called".format(self.__class__.__name__))
        self.draw()

    def create_solid_surface(self, color=(0, 0, 0)):
        """..."""
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)

    def create_gradient(self):
        """..."""
        bottom_color = self.bottom_color
        top_color = self.top_color

        if getattr(self, 'width', None) is None:
            if getattr(self, 'screen', None) is None:
                self.screen = pygame.display.get_surface()
            self.height = self.screen.get_height()
            self.width = self.screen.get_width()

        self.surface = pygame.Surface((self.width, self.height))

        ar = pygame.PixelArray(self.surface)

        # Do some easy gradient effect.
        for y in range(self.height):

            r = int((bottom_color[0] - top_color[0]) *
                    y / self.height +
                    top_color[0])
            g = int((bottom_color[1] - top_color[1]) *
                    y / self.height +
                    top_color[1])
            b = int((bottom_color[2] - top_color[2]) *
                    y / self.height +
                    top_color[2])

            ar[:, y] = (r, g, b)
        del ar

    def flip_surface(self):
        """..."""
        ar = pygame.PixelArray(self.surface)
        ar[:] = ar[:, ::-1]
        del ar

    def __getstate__(self):
        """..."""
        return None


class Window(Layer):
    """..."""

    def __init__(self, *, parent, x=0, y=0, w=None, h=None, tile_size=32):
        """..."""
        super().__init__(parent=parent)
        if w % tile_size:
            self.width = ((w or parent.width) // 32 + 1) * 32
            self.x = max(x - (self.width - w) // 2, 0)
        else:
            self.width = w or parent.width
            self.x = x
        if h % tile_size:
            self.height = ((h or parent.height) // 32 + 1) * 32
            self.y = max(y - (self.height - y) // 2, 0)
        else:
            self.height = h or parent.height
            self.y = y

        self.tile_size = tile_size

    @property
    def window_skin(self):
        """..."""
        if not hasattr(self, '_window_skin'):
            self._window_skin = self.game.images.get(
                "window_{}px.png".format(self.tile_size))
        return self._window_skin

    @window_skin.setter
    def window_skin(self, img):
        self._window_skin = self.game.Image(img)

    def hide(self):
        """NOT IMPLEMENTED."""
        return
        self.visible = False

    def set_margin(self, v):
        """..."""
        self.width += v * 2
        self.height += v * 2
        self.x = max(self.x - v, 0)
        self.y = max(self.y - v, 0)

    def draw(self):
        """..."""
        max_x = self.width // self.tile_size
        max_y = self.height // self.tile_size

        for x in range(0, max_x):
            for y in range(0, max_y):
                tile_pos = [1, 1]
                if y == 0:
                    tile_pos[1] = 0
                elif y == max_y - 1:
                    tile_pos[1] = 2
                if x == 0:
                    tile_pos[0] = 0
                elif x == max_x - 1:
                    tile_pos[0] = 2

                self.draw_tile(tile_pos, (x, y))

    def draw_tile(self, tile_pos, sfc_pos):
        """..."""
        surface = self.screen
        x, y = sfc_pos

        size = self.tile_size

        dest = pygame.Rect(x * size + self.x, y * size + self.y, size, size)

        src_area = tile_pos[0] * size, tile_pos[1] * size, size, size

        src_img = self.window_skin

        surface.blit(source=src_img, dest=dest, area=src_area)

    def default_window_skin(self):
        """Return the default window skin."""
        self._skin
        size = self.tile_size
        path = os.path.join(
            os.path.dirname(__file__), "resources", "skins", "default",
            "window_{}px.png".format(size))
        return self.pygame.image.load(path).convert_alpha()


class Menu(Layer):
    """..."""

    def __init__(self, *, parent, title, items=None, background=True):
        """..."""
        super().__init__(parent=parent)
        self._title = title
        self._items = items
        self.color = (223, 0, 0)

        self.unselected_color = GAME_COLORS["white"]
        self.set_selected_color()

        self.selection = 0

        self.create_head()
        if items:
            self.create_items()

        self.create_background()

        self.select()

    def create_background(self):
        """..."""
        ((x, y), (x1, y1)) = self.body_rect
        w = x1 - x
        h = y1 - y
        self.background = Window(parent=self, x=x, y=y, w=w, h=h)
        self.background.set_margin(16)

    def add_item(self, text):
        self._items.append(text)
        self.create_items()
        self.select()

    def remove_item(self, item):
        if isinstance(item, str):
            index = self._items.index(item)
        else:
            index = item
        self._items.pop(index)
        self.create_items()
        self.select()

    def clear(self):
        del self.item_render

    def set_selected_color(self):
        selected_color = list(self.unselected_color)
        for i in [0, 1]:
            selected_color[i] = (
                (255 - selected_color[i]) // 2 +
                selected_color[i]
            )
        selected_color[2] = selected_color[2] // 3
        self.selected_color = tuple(selected_color)

    def create_head(self):
        self.screen_size = screen_size = self.screen.get_size()
        self.head_font_size = head_font_size = screen_size[1] // 17
        self.head_font = self.fonts.load(
            'caladea-regular.ttf', head_font_size)

        x, y = screen_size[0] // 2, screen_size[1] // 5

        self.head_title_sfc = self.head_font.render(
            self._title, True, self.color)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = x, y

        self.head_title_shadow_sfc = self.head_font.render(
            self._title, True, GAME_COLORS["darker_gray"])
        self.head_title_shadow_obj = self.head_title_sfc.get_rect()
        self.head_title_shadow_obj.center = x + 2, y + 2

    def color_surface(self, surface, color):
        arr = pygame.surfarray.pixels3d(surface)
        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        del arr

    def select(self, index=0):
        old_selection = self.item_render[self.selection][0][0]
        self.color_surface(old_selection, self.unselected_color)

        self.selection = index

        new_selection = self.item_render[self.selection][0][0]
        self.color_surface(new_selection, self.selected_color)

    def create_items(self):
        items = self._items
        item_render = []

        main_font_size = int(self.head_font_size // 1.1)
        self.main_font = self.fonts.load(
            'caladea-regular.ttf', main_font_size)
        main_font_size = self.main_font.size("A")

        for i, item in enumerate(items):

            txt_sfc = self.main_font.render(
                item, True, self.unselected_color)
            txt_obj = txt_sfc.get_rect()
            x, y = (
                self.screen_size[0] // 2,
                self.head_title_obj.bottom + self.head_title_obj.height * 2 +
                main_font_size[1] * i
            )
            txt_obj.midtop = x, y

            txt_shd_sfc = self.main_font.render(
                item, True, GAME_COLORS["darker_gray"])
            txt_shd_obj = txt_shd_sfc.get_rect()
            txt_shd_obj.midtop = x + 2, y + 2

            item_render.append(
                ((txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)))

            self.item_render = item_render

    @property
    def body_rect(self):
        """..."""

        if getattr(self, '_rect', None) is None:
            _rect = [[None] * 2] * 2
            for ((txt_sfc, txt_obj),
                 (txt_shd_sfc, txt_shd_obj)) in self.item_render:
                topleft0 = txt_obj.topleft
                topleft1 = txt_shd_obj.topleft
                topleft = (min(topleft0[0], topleft1[0]),
                           min(topleft0[1], topleft1[1]))
                _rect[0] = (min(_rect[0][0] or topleft[0], topleft[0]),
                            min(_rect[0][1] or topleft[1], topleft[1]))

                bottomright0 = txt_obj.bottomright
                bottomright1 = txt_shd_obj.bottomright
                bottomright = (max(bottomright0[0], bottomright1[0]),
                               max(bottomright0[1], bottomright1[1]))
                _rect[1] = (max(_rect[1][0] or bottomright[0], bottomright[0]),
                            max(_rect[1][1] or bottomright[1], bottomright[1]))
            self._rect = tuple(_rect)

        return self._rect

    def draw(self):
        self.background.draw()
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

        for (
            (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)
        ) in self.item_render:
            self.screen.blit(txt_shd_sfc, txt_shd_obj)
            self.screen.blit(txt_sfc, txt_obj)


    def __getstate__(self):
        return None


class Choice(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.title_color = (223, 0, 0)

        self.unselected_color = (192, 192, 192)
        self.set_selected_color()

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["choice"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["choice"]:
            return True
        else:
            return False

    def choice(self, title, items, callback):
        """..."""
        self.set_list(title, items, callback)
        self.active = True

    def change_selection(self, value):
        value += self.selection
        value = value % len(self._items)
        self.select(value)

    def confirm(self):
        self.callback(
            (self.selection, self._items[self.selection])
        )

    def set_list(self, title, items, callback):
        self._title = title
        self._items = items
        self.callback = callback

        self.selection = 0

        self.create_head()
        self.create_items()

        self.select(self.selection)

    def clear(self):
        del self.head_title_sfc, self.head_title_shadow_sfc
        del self.item_render

    def set_selected_color(self):
        selected_color = list(self.unselected_color)
        for i in [0, 1]:
            selected_color[i] = (
                (255 - selected_color[i]) // 2 +
                selected_color[i]
            )
        selected_color[2] = selected_color[2] // 3
        self.selected_color = tuple(selected_color)

    def select(self, index=0):
        old_selection = self.item_render[self.selection][0][0]
        self.color_surface(old_selection, self.unselected_color)

        self.selection = index

        new_selection = self.item_render[self.selection][0][0]
        self.color_surface(new_selection, self.selected_color)

    def color_surface(self, surface, color):
        arr = pygame.surfarray.pixels3d(surface)
        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        del arr

    def create_head(self):
        self.screen_size = screen_size = self.screen.get_size()
        self.head_font_size = head_font_size = screen_size[1] // 17
        self.head_font = self.fonts.load(
            'caladea-regular.ttf', head_font_size)

        x, y = (screen_size[0] // 2, screen_size[1] // 5)

        self.head_title_sfc = self.head_font.render(
            self._title, True, self.title_color)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = (x, y)

        self.head_title_shadow_sfc = self.head_font.render(
            self._title, True, GAME_COLORS["darker_gray"])
        self.head_title_shadow_obj = self.head_title_sfc.get_rect()
        self.head_title_shadow_obj.center = (x + 2, y + 2)

    def create_items(self):
        items = self._items
        item_render = []

        main_font_size = int(self.head_font_size // 1.1)
        self.main_font = self.fonts.load(
            'caladea-regular.ttf', main_font_size)
        main_font_size = self.main_font.size("A")

        for i, item in enumerate(items):

            txt_sfc = self.main_font.render(
                item, True, self.unselected_color)
            txt_obj = txt_sfc.get_rect()
            x, y = (
                self.screen_size[0] // 2,
                self.head_title_obj.bottom + self.head_title_obj.height * 2 +
                main_font_size[1] * i
            )

            txt_obj.midtop = x, y

            txt_shd_sfc = self.main_font.render(
                item, True, GAME_COLORS["black"])
            txt_shd_obj = txt_shd_sfc.get_rect()
            txt_shd_obj.midtop = x + 2, y + 2

            item_render.append(
                ((txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)))

            self.item_render = item_render

    def draw(self):
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

        for (
            (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)
        ) in self.item_render:
            self.screen.blit(txt_shd_sfc, txt_shd_obj)
            self.screen.blit(txt_sfc, txt_obj)

    def on_key_press(self, event):
        """..."""
        if event.key == pygame.K_UP:
            self.gfx.choice.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.gfx.choice.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            self.gfx.choice.confirm()
            self.active = False
            self.gfx.choice.clear()

    def __getstate__(self):
        return None


class Msg(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.text = ""
        self.color = (223, 0, 0)
        self.screen_size = self.screen.get_size()
        self.head_font_size = self.screen_size[1] // 18
        self.head_font = self.fonts.load(
            'caladea-regular.ttf', self.head_font_size)

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return False
        else:
            return True

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return False
        else:
            return True

    def draw(self):
        """..."""
        text = self.text
        w, h = self.screen_size

        x, y = w // 2, h // 2

        # prepare
        self.head_title_sfc = self.head_font.render(
            text, True, self.color)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = (x, y)

        self.head_title_shadow_sfc = self.head_font.render(
            text, True, GAME_COLORS["gray"])
        self.head_title_shadow_obj = self.head_title_sfc.get_rect()
        self.head_title_shadow_obj.center = (x, y)

        # render
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

    def __getstate__(self):
        """..."""
        return None


class Inventory(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.offset = 0
        self.create_head()
        self.create_main()

    def draw(self):
        """..."""
        self.screen.blit(self.head_surface,
                         self.head_rect)
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc,
                         self.head_title_obj)

        self.screen.blit(self.main_surface, self.main_rect)
        for (
            (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj), item
        ) in self.inv_render:
            self.screen.blit(txt_shd_sfc,
                             txt_shd_obj)
            self.screen.blit(txt_sfc,
                             txt_obj)

    def click_on(self, pos):
        """..."""
        if self.main_rect.collidepoint(pos):
            for (
                (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj), item
            ) in self.inv_render:
                if (
                    txt_obj.collidepoint(pos) or
                    txt_shd_obj.collidepoint(pos)
                ):
                    if self.mode == 'use':
                        result = item.item.use(
                            user=self.holder, target=self.target)
                        if result != 'used':
                            self.set_inventory(
                                self.holder, self.target, self.mode)
                        return result
                    elif self.mode == 'drop':
                        return item.item.drop(
                            dropper=self.holder)
            ar = pygame.PixelArray(self.main_surface)
            ar[:] = ar[:, ::-1]
            del ar

    def on_key_press(self, event):
        """..."""
        parent = self.parent

        if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
            self.clean_inventory()
            parent.state = "playing"
            parent.on_update()
            return True

    def on_mouse_press(self, event):
        """Handle mouse press input."""
        parent = self.parent
        pos = event.pos

        result = self.click_on(pos)
        print("on_mouse_press result:", result)
        if result in ['used', "dropped"]:
            parent.state = "playing"
            self.clean_inventory()
            parent.player.action()
            parent.handle_turn()
            return True
        elif result in ['equipped', 'cancelled']:
            return True

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["inventory"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["inventory"]:
            return True
        else:
            return False

    def create_head(self):
        """..."""
        self.head_font = self.fonts.load('caladea-regular.ttf', 26)
        h = self.head_font.size("A")[1] * 2
        w = self.screen.get_size()[0]
        w = int(w * 0.9)
        x, y = self.screen.get_size()
        x, y = int(x * 0.05), int(y * 0.05)

        self.head_surface = pygame.Surface(
            (w, h), pygame.SRCALPHA)
        self.head_rect = self.head_surface.get_rect()
        self.head_rect.topleft = (x, y)

        # Create the PixelArray.
        ar = pygame.PixelArray(self.head_surface)
        r, g, b = 0, 0, 0
        # Do some easy gradient effect.
        for y in xrange_(h):
            scale = int(y / h * 31)
            scale = max(0, scale)
            scale = min(scale, 255)
            r, g, b = scale, scale, 223
            ar[:, y] = (r, g, b, 223)
        del ar

        self.head_title_sfc = self.head_font.render(
            "< Inventory >", True, GAME_COLORS["chartreuse"])
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = self.head_rect.center

        self.head_title_shadow_sfc = self.head_font.render(
            "< Inventory >", True, GAME_COLORS["black"])
        self.head_title_shadow_obj = self.head_title_shadow_sfc.get_rect()
        self.head_title_shadow_obj.x, self.head_title_shadow_obj.y = (
            self.head_title_obj.x + 2, self.head_title_obj.y + 2)

    def create_main(self):
        """..."""
        w = self.head_rect.width
        h = int(self.screen.get_size()[1] * 0.7) - self.head_rect.height - 16

        x = self.head_rect.x
        y = self.head_rect.bottom + 8

        self.main_surface = pygame.Surface(
            (w, h), pygame.SRCALPHA)
        self.main_rect = self.main_surface.get_rect()
        self.main_rect.topleft = (x, y)

        # Create the PixelArray.
        ar = pygame.PixelArray(self.main_surface)
        r, g, b = 0, 0, 0
        # Do some easy gradient effect.
        for y in xrange_(h):

            scale1 = int(y / h * 63)
            scale1 = max(0, scale1)
            scale1 = min(scale1, 255)

            scale2 = int(y / h * 127)
            scale2 = max(0, scale2)
            scale2 = min(scale2, 255)

            r, g, b = scale2, scale1, 223
            ar[:, y] = (r, g, b, 223)
        del ar

        test_text = "healing potion potion"
        self.main_font = self.fonts.load('caladea-regular.ttf', 18)

        self.main_item_h = int(self.main_font.size(test_text)[1] * 1.2)

        self.main_item_w = int(self.main_font.size(test_text)[0] * 1.1)
        self.rows = self.main_rect.height // (self.main_item_h + 1)
        self.cols = self.main_rect.width // self.main_item_w

        total_width = self.main_item_w * self.cols
        self.tab_x = int(self.main_rect.width - total_width)

    def create_desc(self):
        """..."""
        pass

    def clean_inventory(self):
        """..."""
        del self.inv_render
        self.inv_render = []
        self.holder = None
        self.target = None

    def set_inventory(self, holder, target=None, mode="use"):
        """..."""
        self.holder = holder
        self.target = target
        self.mode = mode
        offset = self.offset
        self.inventory = self.holder.inventory
        self.inv_render = []

        limit = self.rows * self.cols
        for i, item in enumerate(self.inventory[offset:offset + limit]):
            row = i % self.rows
            col = i // self.rows

            if item.equipment:
                if item.equipment.is_equipped:
                    text = "*{} ({})".format(item.name, item.equipment.slot)
                else:
                    text = "{} ({})".format(item.name, item.equipment.slot)
                color = item.color
            else:
                text = item.name + str(i)
                color = GAME_COLORS["chartreuse"]

            txt_sfc = self.main_font.render(text, True, color)
            txt_obj = txt_sfc.get_rect()
            txt_obj.left = (
                self.main_rect.left + self.tab_x + self.main_item_w * col)
            txt_obj.top = self.main_rect.top + (self.main_item_h * row) + 12

            txt_shd_sfc = self.main_font.render(text, True,
                                                GAME_COLORS["black"])
            txt_shd_obj = txt_shd_sfc.get_rect()
            txt_shd_obj.x, txt_shd_obj.y = (
                txt_obj.x + 2, txt_obj.y + 2)

            self.inv_render.append((
                (txt_sfc, txt_obj),
                (txt_shd_sfc, txt_shd_obj),
                item))

    def __getstate__(self):
        return None


class Bar(Layer):
    """..."""

    x = 16
    y = 16
    height = 26
    font_size = 20
    total_width = 160
    alpha = 90
    bar_color = GAME_COLORS["blood_red"]
    text_color_table = [
        (range(-999, 25), (223, 0, 0)),
        (range(25, 50), GAME_COLORS["yellow"]),
        (range(50, 75), GAME_COLORS["lime"]),
        (range(75, 101), GAME_COLORS["green"])
    ]

    def __init__(self, parent, name):
        """..."""
        super().__init__(parent=parent)
        self.name = name
        self.set_color()

        if self.alpha is None:
            flags = 0
        else:
            flags = pygame.SRCALPHA
            bar_color = list(self.bar_color)
            bar_color.append(self.alpha)
            self.bar_color = tuple(bar_color)

        while True:
            test_font = self.fonts.load('caladea-regular.ttf', self.font_size)
            test_size = test_font.size(self.text)[0]
            if test_size > self.total_width - 16:
                self.font_size -= 1
            else:
                self.font = test_font
                break
        self.bg_surface = pygame.Surface(
            (self.bar_width(), self.height), flags)
        self.bg_rect = self.bg_surface.get_rect()
        self.bg_rect.topleft = (self.x, self.y)

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    def bar_width(self, value=None):
        """..."""
        if value is None:
            return int(self.value / self.maximum * self.total_width)
        else:
            return int(value / self.maximum * self.total_width)

    @property
    def value(self):
        """..."""
        return self.parent.player.combat.hit_points_current

    @property
    def maximum(self):
        """..."""
        return self.parent.player.combat.hit_points_total

    def refresh(self):
        """..."""
        w, h = [self.bar_width(), self.bg_surface.get_height()]
        if w < 1:
            new_size = (1, h)
        else:
            new_size = (w, h)

        self.bg_surface = pygame.transform.scale(self.bg_surface, new_size)

        self.set_color()

    def set_color(self):
        """..."""
        self.text_color = self.get_color()

    def get_color(self):
        """..."""
        percent = max(self.percent, 0)
        table = self.text_color_table

        for i in range(len(table)):
            rng = table[i][0]
            color = table[i][1]
            if percent in rng:
                return color

    def draw(self):
        """..."""
        if self.percent > 0:
            self.bg_surface.fill(self.bar_color)
            self.screen.blit(self.bg_surface, self.bg_rect)

        self.screen.blit(
            self.font.render(self.text, False, self.text_color),
            (self.bg_rect.left + 8, self.bg_rect.top))

    @property
    def percent(self):
        """..."""
        return int(self.value / self.maximum * 100)

    @property
    def text(self):
        """..."""
        return str(self.name + " {}/{}".format(self.value, self.maximum))

    def __getstate__(self):
        """..."""
        return None


class MsgLog(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.font = self.fonts.load('caladea-regular.ttf', 20)

        self.line_height = self.font.get_height()

        self.ypos = int(self.screen.get_height() - self.line_height * 1.2)
        self.clear()

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    def clear(self):
        self._history = []

    def add(self, string, color=None):
        if color is None:
            color = GAME_COLORS["desaturated_green"]
        print(string)
        img = self.font.render(string, 1, color)
        self._history.append(img)
        self._history = self._history[-5:]
        # (50, 200, 50)

    @property
    def history(self):
        return reversed(self._history)

    def draw(self):
        ypos = int(self.ypos)
        for line in self.history:
            self.screen.blit(line, (10, ypos))
            # win.fill(0, (r.right, r.top, 620, r.height))
            ypos -= self.line_height

    def __getstate__(self):
        return None


class Hud(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.text = " "
        self.font = self.fonts.load('caladea-bold.ttf', 14)
        self.x, self.y = self.screen.get_size()
        self.x -= 32
        self.y = 0

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    def draw(self):
        self.display = self.font.render(
            self.text, False, GAME_COLORS["desaturated_green"])
        w, h = self.font.size(self.text)
        self.screen.blit(self.display, (self.x - w, self.y + h))

    def __getstate__(self):
        return None
