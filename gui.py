import os
import pygame

from constants import GameColor
import resources


class _Hud:
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

    def __init__(self, name, value, maximum):
        self.name = name
        self.value = value
        self.maximum = maximum
        self.set_color()

        self.screen = pygame.display.get_surface()

        if self.alpha is None:
            flags = 0
        else:
            flags = pygame.SRCALPHA
            bar_color = list(self.bar_color)
            bar_color.append(self.alpha)
            self.bar_color = tuple(bar_color)

        while True:
            test_font = fonts.load('caladea-regular.ttf', self.font_size)
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

    def set_value(self, value):
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


if __name__ == '__main__':
    pygame.init()

    # set up the window
    DISPLAYSURF = pygame.display.set_mode((800, 600))

    fonts = resources.Fonts(path=os.path.join("resources", "fonts"))

    hud = _Hud(name="Health", value=100, maximum=100)
    clock = pygame.time.Clock()
    # run the game loop
    running = True
    while running:
        DISPLAYSURF.fill(GameColor.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        hud.draw()
        if True:
            value = hud.value - 5
            value = value % 100
            hud.set_value(value)

        pygame.display.update()
        clock.tick(10)
