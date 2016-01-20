import pygame

from constants import GameColor

from pygame.compat import xrange_


class Choice:
    def __init__(self, gfx):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
        self.title_color = (223, 0, 0)

        self.unselected_color = (192, 192, 192)
        self.set_selected_color()

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
            self._title, True, GameColor.darker_gray)
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
                item, True, GameColor.black)
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

    def __getstate__(self):
        return None


class Msg:
    def __init__(self, gfx):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
        self.color = (223, 0, 0)
        self.screen_size = self.screen.get_size()
        self.head_font_size = self.screen_size[1] // 18
        self.head_font = self.fonts.load(
            'caladea-regular.ttf', self.head_font_size)

    def draw(self, text):
        w, h = self.screen_size

        x, y = w // 2, h // 2

        # prepare
        self.head_title_sfc = self.head_font.render(
            text, True, self.color)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = (x, y)

        self.head_title_shadow_sfc = self.head_font.render(
            text, True, GameColor.gray)
        self.head_title_shadow_obj = self.head_title_sfc.get_rect()
        self.head_title_shadow_obj.center = (x, y)

        # render
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

    def __getstate__(self):
        return None


class Menu:
    def __init__(self, gfx, title, items=None):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
        self._title = title
        self._items = items
        self.color = (223, 0, 0)

        self.unselected_color = GameColor.white
        self.set_selected_color()

        self.selection = 0

        self.create_head()
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
            self._title, True, GameColor.darker_gray)
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
                item, True, GameColor.darker_gray)
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

    def __getstate__(self):
        return None


class Inventory:
    def __init__(self, gfx):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
        self.offset = 0
        self.create_head()
        self.create_main()

    def create_head(self):
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
            "< Inventory >", True, GameColor.chartreuse)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = self.head_rect.center

        self.head_title_shadow_sfc = self.head_font.render(
            "< Inventory >", True, GameColor.black)
        self.head_title_shadow_obj = self.head_title_shadow_sfc.get_rect()
        self.head_title_shadow_obj.x, self.head_title_shadow_obj.y = (
            self.head_title_obj.x + 2, self.head_title_obj.y + 2)

    def create_main(self):
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
        pass

    def clean_inventory(self):
        del self.inv_render
        self.inv_render = []
        self.holder = None
        self.target = None

    def set_inventory(self, holder, target=None, mode="use"):
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

            txt_sfc = self.main_font.render(
                (item.name + str(i)), True, GameColor.chartreuse)
            txt_obj = txt_sfc.get_rect()
            txt_obj.left = (
                self.main_rect.left + self.tab_x + self.main_item_w * col)
            txt_obj.top = self.main_rect.top + (self.main_item_h * row) + 12

            txt_shd_sfc = self.main_font.render(
                (item.name + str(i)), True, GameColor.black)
            txt_shd_obj = txt_shd_sfc.get_rect()
            txt_shd_obj.x, txt_shd_obj.y = (
                txt_obj.x + 2, txt_obj.y + 2)

            self.inv_render.append((
                (txt_sfc, txt_obj),
                (txt_shd_sfc, txt_shd_obj),
                item))

    def draw(self):
        self.screen.blit(self.head_surface, self.head_rect)
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

        self.screen.blit(self.main_surface, self.main_rect)
        for (
            (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj), item
        ) in self.inv_render:
            self.screen.blit(txt_shd_sfc, txt_shd_obj)
            self.screen.blit(txt_sfc, txt_obj)

    def click_on(self, pos):
        if self.main_rect.collidepoint(pos):
            for (
                (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj), item
            ) in self.inv_render:
                if (
                    txt_obj.collidepoint(pos) or
                    txt_shd_obj.collidepoint(pos)
                ):
                    if self.mode == 'use':
                        return item.item.use(
                            user=self.holder, target=self.target)
                    elif self.mode == 'drop':
                        return item.item.drop(
                            dropper=self.holder)
            ar = pygame.PixelArray(self.main_surface)
            ar[:] = ar[:, ::-1]
            del ar

    def __getstate__(self):
        return None


class Bar:
    """Semi-Abstract object for subclassing"""
    x = 16
    y = 16
    height = 26
    font_size = 20
    total_width = 160
    alpha = 90
    bar_color = GameColor.light_red
    text_color_table = [
        (range(0, 25), GameColor.dark_orange),
        (range(25, 50), GameColor.yellow),
        (range(50, 75), GameColor.lime),
        (range(75, 101), GameColor.green)
    ]

    def __init__(self, name, value, maximum, gfx):
        self.name = name
        self.value = value
        self.maximum = maximum
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
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

    def bar_width(self, value=None):
        if value is None:
            return int(self.value / self.maximum * self.total_width)
        else:
            return int(value / self.maximum * self.total_width)

    def set_value(self, value, maximum=None):
        if max is not None:
            self.maximum = maximum
        self.value = value
        w, h = [self.bar_width(), self.bg_surface.get_height()]
        if w < 1:
            new_size = (1, h)
        else:
            new_size = (w, h)

        self.bg_surface = pygame.transform.scale(self.bg_surface, new_size)

        self.set_color()

    def set_color(self):
        self.text_color = self.get_color()

    def get_color(self):
        percent = self.percent
        table = self.text_color_table

        for i in range(len(table)):
            rng = table[i][0]
            color = table[i][1]
            if percent in rng:
                return color

    def draw(self):
        self.bg_surface.fill(self.bar_color)
        self.screen.blit(self.bg_surface, self.bg_rect)

        self.screen.blit(
            self.font.render(self.text, 0, self.text_color),
            (self.bg_rect.left + 8, self.bg_rect.top))

    @property
    def percent(self):
        return int(self.value / self.maximum * 100)

    @property
    def text(self):
        return str(self.name + " {}/{}".format(self.value, self.maximum))

    def __getstate__(self):
        return None


class MsgLog:

    def __init__(self, gfx):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts
        self.font = self.fonts.load('caladea-regular.ttf', 20)

        self.line_height = self.font.get_height()

        self.ypos = int(self.screen.get_height() - self.line_height * 1.2)
        self._history = []

    def add(self, string, color=None):
        if color is None:
            color = GameColor.desaturated_green
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


class Hud:

    def __init__(self, gfx):
        self.gfx = gfx
        self.screen = self.gfx.screen
        self.fonts = self.gfx.fonts

        self.text = " "
        self.font = self.fonts.load('caladea-bold.ttf', 14)
        self.x, self.y = self.screen.get_size()
        self.x -= 32
        self.y = 0

    def draw(self):
        self.display = self.font.render(
            self.text, False, GameColor.desaturated_green)
        w, h = self.font.size(self.text)
        self.screen.blit(self.display, (self.x - w, self.y + h))

    def __getstate__(self):
        return None
