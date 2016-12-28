"""Test Scene for manager using pysdl2.

SDL_Texture* target_tex =SDL_CreateTexture(.....); //Add arg according to you
SDL_SetRenderTarget(my_renderer, target_tex);

SDL_Texture* t1 = SDL_CreateTextureFromSurface(my_renderer, someSurface);
SDL_Texture* t2 = SDL_CreateTextureFromSurface(my_renderer, someOtherSurface);
.
.
.
.
SDL_RenderCopy(my_renderer, t1, NULL, NULL);
SDL_RenderCopy(my_renderer, t2, NULL, NULL);
SDL_RenderCopy(my_renderer, t3, NULL, NULL);
.
.
.
SDL_SetRenderTarget(my_renderer, NULL);
SDL_RendererPresent(my_renderer);


SDL_RenderClear(my_renderer);
SDL_RenderCopy(my_renderer, target_tex, NULL, NULL);
SDL_RendererPresent(my_renderer);
"""

from math import pi, cos, sin
import unittest

import sdl2
from sdl2 import sdlgfx

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.scene_manager.layers import base_layers
from dnf_game.util.ext.rect import Rect


class PySDL2GfxdrawTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=ScenePySDL2GfxdrawTest, test=False).execute()


class DrawLayer(base_layers.Layer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        w = 256
        h = 128
        rect = Rect(0, 0, w, h)
        sdlrenderer = self.manager.renderer.sdlrenderer
        factory = self.manager.factory

        button = factory.from_new_texture(w, h)
        button_tex = button.texture
        with factory.new_render_target(button_tex):
            draw_button(sdlrenderer, rect, 16, (95, 95, 95, 255))
        button.move(8, 8)

        self.create_gradient_surface()
        self.sprite = button

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=(
            self.surface, self.sprite))


class ScenePySDL2GfxdrawTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.draw_layer = DrawLayer(parent=self).activate().show()
        self.insert_layer(self.draw_layer)


def _draw_circle(renderer, cx, cy, rad, color, sides=0):

    c = sdl2.ext.Color(*color)
    r, g, b, a = c.r, c.g, c.g, c.a

    _2pi = pi * 2

    if (sides == 0):
        sides = int(_2pi * rad / 2)

    d_a = _2pi / sides
    angle = d_a

    end_x = rad + cx
    end_y = 0.0 + cy
    i = 0
    sdl2.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    while i != sides:
        start_x = end_x
        start_y = end_y
        end_x = cos(angle) * rad
        end_y = sin(angle) * rad
        end_x += cx
        end_y += cy
        angle += d_a

        sdl2.SDL_RenderDrawLine(renderer,
                                int(start_x), int(start_y),
                                int(end_x), int(end_y))
        i += 1


def draw_button(renderer, rect, rad, color):
    """..."""
    _draw_circle(renderer, rad, rad, rad, color)
    return

    c = sdl2.ext.Color(*color)
    r, g, b, a = c.r, c.g, c.g, c.a

    circle = sdlgfx.filledCircleRGBA
    # circle = sdlgfx.aacircleRGBA
    rectangle = sdlgfx.boxRGBA
    # rectangle = sdlgfx.rectangleRGBA

    # topleft
    circle(renderer, rad, rad, rad, r, g, b, a)
    # bottomleft
    circle(renderer, rad, rect.height - rad, rad, r, g, b, a)
    # left
    rectangle(renderer,
              0,  # x
              rect.top + rad + 1,  # y
              rad,  # w
              rect.height - rad // 2 - 4,  # h
              r, g, b, a)

    # topright
    circle(renderer, rect.right - rad, rect.top + rad, rad, r, g, b, a)
    # top
    rectangle(renderer,
              rect.left + rad + 1,  # x
              0,  # y
              rect.width - rad // 2 - 4,  # w
              rad,  # h
              r, g, b, a)

def draw_button1(renderer, rect, rad, color):
    """..."""
    c = sdl2.ext.Color(*color)
    r, g, b, a = c.r, c.g, c.g, c.a
    x1 = rect.right
    y1 = rect.top
    x2 = rect.left
    y2 = rect.bottom

    cx = 0
    cy = rad

    cx = 0
    cy = rad
    ocx = None
    ocy = None
    df = 1 - rad
    d_e = 3
    d_se = -2 * rad + 5

    # Test for special cases of straight lines or single point

    # Swap x1, x2 if required
    if (x1 > x2):
        x1, x2 = x2, x1

    # Swap y1, y2 if required
    if (y1 > y2):
        y1, y2 = y2, y1

    # Calculate width & height
    w = x2 - x1 + 1
    h = y2 - y1 + 1

    # Maybe adjust radius
    r2 = rad + rad
    if (r2 > w):
        rad = w // 2
        r2 = rad + rad
    if (r2 > h):
        rad = h // 2

    # Setup filled circle drawing for corners
    x = x1 + rad
    y = y1 + rad
    dx = x2 - x1 - rad - rad
    dy = y2 - y1 - rad - rad

    # Draw corners
    while cx < cy:
        xpcx = x + cx
        xmcx = x - cx
        xpcy = x + cy
        xmcy = x - cy
        if (ocy != cy):
            if (cy > 0):
                ypcy = y + cy
                ymcy = y - cy
                # !!!!!!!!!
                sdlgfx.hlineRGBA(renderer, xmcx, xpcx + dx, ypcy + dy,
                                 r, g, b, a)
                sdlgfx.hlineRGBA(renderer, xmcx, xpcx + dx, ymcy,
                                 r, g, b, a)
            else:
                sdlgfx.hlineRGBA(renderer, xmcx, xpcx + dx, y,
                                 r, g, b, a)
            ocy = cy

        if (ocx != cx):
            if (cx != cy):
                if (cx > 0):
                    ypcx = y + cx
                    ymcx = y - cx
                    sdlgfx.hlineRGBA(renderer, xmcy, xpcy + dx, ymcx,
                                     r, g, b, a)
                    sdlgfx.hlineRGBA(renderer, xmcy, xpcy + dx, ypcx + dy,
                                     r, g, b, a)
                else:
                    sdlgfx.hlineRGBA(renderer, xmcy, xpcy + dx, y,
                                     r, g, b, a)
            ocx = cx

        # Update
        if (df < 0):
            df += d_e
            d_e += 2
            d_se += 2
        else:
            df += d_se
            d_e += 2
            d_se += 4
            cy -= 1
        cx += 1

    # Inside
    if (dx > 0 and dy > 0):
        sdlgfx.boxRGBA(renderer, x1, y1 + rad + 1, x2, y2 - rad,
                       r, g, b, a)

    sdlgfx.hlineRGBA(renderer, rad // 2, x2 - rad // 2, 0,
                     227, 227, 216, 23)
    sdlgfx.hlineRGBA(renderer, rad // 2 - 1, x2 - rad // 2 + 1, 1,
                     227, 227, 216, 23)

    sdlgfx.vlineRGBA(renderer, 0, rad // 2, y2 - rad // 2,
                     227, 227, 216, 23)
    sdlgfx.vlineRGBA(renderer, 1, rad // 2 - 1, y2 - rad // 2 + 1,
                     227, 227, 216, 23)

    sdlgfx.hlineRGBA(renderer, rad // 2 - 1, x2 - rad // 2 + 1, y2 - 1 - 1,
                     0, 0, 0, 47)
    sdlgfx.hlineRGBA(renderer, rad // 2, x2 - rad // 2, y2 - 1,
                     0, 0, 0, 47)

    sdlgfx.vlineRGBA(renderer, x2 - 1 - 1, rad // 2 - 1, y2 - rad // 2 + 1,
                     0, 0, 0, 47)
    sdlgfx.vlineRGBA(renderer, x2 - 1, rad // 2, y2 - rad // 2,
                     0, 0, 0, 47)

    # 227, 227, 216, 31)
    # 0, 0, 0, 63)



if __name__ == '__main__':
    unittest.main(verbosity=2)
