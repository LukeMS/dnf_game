import pygame

from constants import GameColor

from pygame.compat import xrange_


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
