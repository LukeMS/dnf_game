# remove font_obj
"""Scrollable Formatted Text for pysdl2 (sftext-pysdl2).

Copyright (c) 2016 Lucas de Morais Siqueira

Distributed under the GNU Lesser General Public License version 3.

############################################
### SCROLLABLE FORMATTED TEXT FOR PYSDL2 ###
############################################

Support by using, forking, reporting issues and giving feedback:
https://github.com/LukeMS/sftext/

Lucas de Morais Siqueira (aka LukeMS)
lucas.morais.siqueira@gmail.com

This file is part of sftext-pysdl2.

sftext-pysdl2 is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
any later version.

sftext-pysdl2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with sftext-pysfl2. If not, see <http://www.gnu.org/licenses/#LGPL>.
"""

import sdl2

from dnf_game.util.sftext.style import Style
from dnf_game.util import shoehorn
from dnf_game.util.ext.rect import Rect


def space_left(x, scr_w, style, size_func):
    """Calculate the remaining space on the row (in pixels).

    Args:
        x (int): The current horizontal position for insertion to be checked
        against;
        scr_w (int): The maximum size of the row (usually the screen size);
        style (dict): style dictionary containing text_size method, alias and
        font size.

    Returns:
        int
    """
    alias = style['font']
    size = style['size']
    text_size = size_func(' ', alias, size)
    return (scr_w - text_size[0] * 6 - x - 5)


def contain_any(string, chars):
    """Verify if a string contain any of a set of characters.

    Args:
        string (str): the string to be checked againts;
        chars (str): one or more characters to be verified.

    Returns:
        bool
    """
    if isinstance(chars, str):
        chars = [chars]
    return any([c in string for c in chars])


class SFText():
    """Scrollable Formatted Text for pygame."""

    def __init__(
        self, *, text, rect, fonts, manager, font_path='.', style=None
    ):
        """Initialization.

        Args:
            text: the text that will be rendered;
            font_path: location that will be searched for the required fonts;
            style: a default style to be used;
            rect: a Rect object (pass in a subarea if you don't want
            to use all of the screen when rendering).
        """
        if isinstance(text, bytes):
            self.text = text.decode('utf-8')
        elif isinstance(text, str):
            self.text = text

        self.fonts = fonts
        self.manager = manager

        Style.set_default(style)

        self.screen_rect = Rect(rect)

        self.anchor_x = self.screen_rect.x
        self.anchor_y = self.screen_rect.y

        # print('parsing text')
        self.parse_text()
        # print('done parsing')
        # print('rendering surfaces')
        self.render_surfaces()
        # print('done rendering surfaces')

        return

        self.print_stats()
        # self.screenshot('sftext.png')
        _y = None
        for p in self.parsed:
            if p['rect'].y == _y:
                print(p, end="")
            else:
                print()
                print(p, end="")
                _y = p['rect'].y
        # exit()

    def set_font(self, obj):
        """..."""
        if obj['bold'] and obj['italic'] and obj['separate_bolditalic']:
            obj['font_obj'] = self.fonts.load(
                obj['separate_bolditalic'],
                obj['size'])
        elif obj['separate_bold'] and obj['bold']:
            obj['font_obj'] = self.fonts.load(
                obj['separate_bold'],
                obj['size'])
        elif obj['separate_italic'] and obj['italic']:
            obj['font_obj'] = self.fonts.load(
                obj['separate_italic'],
                obj['size'])
        else:
            obj['font_obj'] = self.fonts.load(
                obj['font'],
                obj['size'])

    def parse_text(self):
        """..."""
        fonts = self.fonts
        size_func = fonts.text_size
        self.parsed = []
        scr_w = self.screen_rect.width

        default_style = Style.default_style

        default_style['w'], default_style['h'] = size_func(
            text=' ',
            name=default_style['font'],
            size=default_style['size'])
        self.default_style = default_style

        y = 0
        for line in self.text.splitlines():
            x = 0
            for style in line.split("{style}"):

                # print('splitting style...', end="")
                text, styled_txt = Style.split(style)
                # print('done!')

                self.set_font(styled_txt)

                w, h = styled_txt['w'], styled_txt['h'] = size_func(
                    text=' ',
                    name=styled_txt['font'],
                    size=styled_txt['size'])

                # determine the amount of space needed to render text
                wraps = self.wrap_text(text, scr_w, x, styled_txt)
                # print('wrapping...', end="")
                for wrap in wraps:
                    rect_w, rect_h = size_func(text=wrap['text'],
                                               name=wrap['font'],
                                               size=wrap['size'])
                    rect = Rect((0, 0), (rect_w, rect_h))

                    # ################
                    # Calculate remaining space on the row, escaping to the
                    # next one if necessary.
                    # (x, scr_w, size_func, alias, font_size)
                    if wrap['w1'] > space_left(x, scr_w, wrap, size_func):
                        x = 0
                        y += wrap['h']
                    # ################

                    if len(wraps) == 1 and wrap['align'] == 'center':
                        rect.midtop = (
                            self.screen_rect.width // 2,
                            self.screen_rect.bottom + y)
                    else:
                        rect.topleft = (
                            x + w * 3,
                            self.screen_rect.bottom + y)
                    wrap['rect'] = rect
                    wrap['x'] = x
                    wrap['y'] = y
                    if False:
                        print("\n{}: {},".format('x', wrap['x']), end='')
                        print("{}: {},".format('y', wrap['y']), end='')
                        print("{}: {},".format('w', wrap['w']), end='')
                        print("{}: {}".format('h', wrap['h']))
                        print(wrap['text'])
                    self.parsed.append(wrap)

                    x += wrap['w1']
                # print('done!')
            y += wrap['h']
        # exit()
        # print('done parsing')

        self.start_y = (- self.screen_rect.h +
                        self.default_style['h'] -
                        self.anchor_y)

        self.y = self.start_y

        self.end_y = -(self.sum_height() +
                       self.anchor_y +
                       self.default_style['h'] * 2)

    def sum_height(self):
        """..."""
        if self.parsed:
            # return sum(p['h'] for p in self.parsed if not p['x'])
            v = max([p['y'] + p['h'] for p in self.parsed])
            # print(v)
            return v
        else:
            return 0

    def print_stats(self):
        """..."""
        print(("start_y {}, y {}, end_y {},"
               "anchor_y {}, sum_height{}, screen_rect.h{}").format(
            self.start_y, self.y, self.end_y, self.anchor_y,
            self.sum_height(), self.screen_rect.h))

    def wrap_text(self, text, scr_w, x0, styled_txt):
        """..."""
        fonts = self.fonts
        size_func = fonts.text_size

        x = int(x0)
        break_chars = [" ", ",", ".", "-", "\n"]
        style = dict(styled_txt)
        wrapped = []

        alias = style['font']
        font_size = style['size']

        txt_w = size_func(text, alias, font_size)[0]
        if (txt_w <= space_left(x, scr_w, style, size_func) or
                len(text) == 0):
            style['text'] = text
            style['w1'] = txt_w
            wrapped.append(style)
            return wrapped

        wrapped = [text]

        iterations = 1
        while True:
            wrap = wrapped[-1]
            # First case: it fits entirely
            txt_w = size_func(wrap, alias, font_size)[0]
            if txt_w < space_left(x, scr_w, style, size_func):
                # It fits, we pack it and break.
                style['text'] = wrap
                style['w1'] = txt_w
                wrapped[-1] = dict(style)
                break

            # Second case
            # We see how many chars can fit in the space
            # end + 1 will not exceed the string length or the first case
            # would have to be valid
            for end in range(len(wrap)):
                txt_w = size_func(wrap[:end + 1], alias, font_size)[0]
                if txt_w >= space_left(x, scr_w, style, size_func):
                    break

            forced = not contain_any(wrap[:end], break_chars)
            if forced and x:
                x = 0
                continue

            # We now look for break_chars in the end of the fragment
            for i in range(end, -1, -1):
                c = wrap[i]
                if c in break_chars or forced:
                    fit = wrap[:i]
                    remains = wrap[i:]
                    style['text'] = fit
                    style['w1'] = size_func(fit, alias, font_size)[0]
                    wrapped[-1] = dict(style)
                    wrapped.append(remains)
                    x = 0
                    break
            if iterations > 100:
                print("#######")
                print(shoehorn(text))
                print("len(text) =", len(text))
                print("scr_w =", scr_w)
                print("x0 =", x0)
                print("space_left =", space_left(x0, scr_w, style))
                print("x =", x)
                print("space_left =", space_left(x, scr_w, style))
                print("'w1' =", size_func(text, alias, font_size)[0])
                print("size(' ' * 12)[0] =", size_func(' ' * 12, alias,
                                                       font_size)[0])
                print("styled_txt =", styled_txt)
                print("#######")
            iterations += 1
        return wrapped

    def screenshot(self, fname):
        """..."""
        raise NotImplementedError("Screenshot not implemented")
        # canvas = pygame.Surface((self.screen_rect.width, self.sum_height()))
        # self.on_update(limit=False, canvas=canvas)
        # pygame.image.save(canvas, fname)

    def render_surfaces(self):
        """Generate sprites from text fragments.

           vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
             BASE ON PYGAME VERSION'S ON_UPDATE
           vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        """
        fonts = self.fonts

        for parsed in self.parsed:
            font = parsed['font']
            size = parsed['size']
            color = parsed['color']
            text = parsed['text']
            bold = parsed['bold']
            italic = parsed['italic']
            spec_b_i = parsed['separate_bolditalic']
            spec_b = parsed['separate_bold']
            spec_i = parsed['separate_italic']

            if not text:
                parsed['sprite'] = None
                continue

            if bold and italic and not spec_b_i:
                # print('pygame-bold', p['text'])
                parsed['font_obj'].set_bold(bold)
                # print('pygame-italic', p['text'])
                parsed['font_obj'].set_italic(italic)
            elif not spec_b and bold:
                # print('pygame-bold', p['text'])
                parsed['font_obj'].set_bold(bold)
            elif not spec_i and italic:
                # print('pygame-italic', p['text'])
                parsed['font_obj'].set_italic(italic)

            # TODO: formatting in sdl2
            # p['font_obj'].set_underline(p['underline'])

            parsed['sprite'] = fonts.render(text, font, size, color)

    def on_update(self, limit=True):
        """..."""
        def visible_sprites():
            for parsed in self.parsed:
                rect = parsed['rect'].move(
                    self.anchor_x, self.y + self.anchor_y)
                if limit and rect.bottom - parsed['h'] < self.anchor_y:
                    continue
                if limit and rect.top >= (self.screen_rect.bottom -
                                          self.default_style['h']):
                    break

                sprite = parsed['sprite']
                if sprite is None:
                    continue
                sprite.position = rect.x, rect.y
                yield sprite

        self.manager.spriterenderer.render(sprites=visible_sprites())

    def scroll(self, y=0):
        """..."""
        if isinstance(y, int):
            self.y += y
            if (abs(self.end_y) <= self.screen_rect.h):
                self.y = self.start_y
            elif self.y < self.end_y:
                self.y = self.end_y
            elif self.y > self.start_y:
                self.y = self.start_y
        elif isinstance(y, str):
            if y == 'home':
                self.y = self.start_y
            elif y == 'end':
                self.y = self.end_y if (
                    abs(self.end_y) > self.screen_rect.h) else self.start_y

        # self.print_stats()

    def post_update(self):
        """..."""
        self.screen.blit(self.bg, dest=self.screen_rect)

    def on_key_press(self, event):
        """..."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_UP:
            # if event.type == pygame.KEYDOWN and sym == sdl2.SDLK_UP
            self.scroll(50)
        elif sym == sdl2.SDLK_PAGEUP:
            # elif event.type == pygame.KEYDOWN and sym == sdl2.SDLK_PAGEUP:
            self.scroll(500)
        elif sym == sdl2.SDLK_HOME:
            # elif event.type == pygame.KEYDOWN and sym == sdl2.SDLK_HOME:
            self.scroll('home')
        elif sym == sdl2.SDLK_DOWN:
            # elif event.type == pygame.KEYDOWN and sym == sdl2.SDLK_DOWN:
            self.scroll(-50)
        elif sym == sdl2.SDLK_PAGEDOWN:
            # elif event.type == pygame.KEYDOWN and sym == sdl2.SDLK_PAGEDOWN:
            self.scroll(-500)
        elif sym == sdl2.SDLK_END:
            # elif event.type == pygame.KEYDOWN and sym == sdl2.SDLK_END:
            self.scroll('end')

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """..."""
        self.scroll(offset_y * 50)
