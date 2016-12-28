"""Pure Python implementation of Pygame/PyGameSDL2's gfxdraw.

Original available at:
    github.com/renpy/pygame_sdl2/blob/master/src/pygame_sdl2/gfxdraw.pyx

Altered source mark:
    --------------------------------------------------------------------------
               _ _                    _                                  _
         /\   | | |                  | |                                | |
        /  \  | | |_ ___ _ __ ___  __| |    ___  ___  _   _ _ __ ___ ___| |
       / /\ \ | | __/ _ \ '__/ _ \/ _` |   / __|/ _ \| | | | '__/ __/ _ \ |
      / ____ \| | ||  __/ | |  __/ (_| |   \__ \ (_) | |_| | | | (_|  __/_|
     /_/    \_\_|\__\___|_|  \___|\__,_|   |___/\___/ \__,_|_|  \___\___(_)

    --------------------------------------------------------------------------

PygameSDL2 Notice:
----------------------------------------------------------------------------
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
----------------------------------------------------------------------------
"""

import ctypes

from sdl2 import sdlgfx as sdlgfx_tex
from sdl2.ext import SDLError
from sdl2.ext.color import Color
from dnf_game.util.ext.rect import Rect
from dnf_game.util.ext import pygame_sdl2_gfx_sfc as sdlgfx_sfc


__all__ = (
    'pixel', 'pixelRGBA', 'hline', 'hlineRGBA', 'vline', 'vlineRGBA',
    'rectangle', 'rectangleRGBA', 'rounded_rectangle', 'roundedRectangleRGBA',
    'rounded_box', 'boxRGBA', 'line', 'lineRGBA', 'aaline', 'aalineRGBA',
    'circle', 'circleRGBA', 'arc', 'arcRGBA', 'aacircle', 'aacircleRGBA',
    'filled_circle', 'filledCircleRGBA', 'ellipse', 'ellipseRGBA',
    'aaellipse', 'aaellipseRGBA', 'filled_ellipse', 'filledEllipseRGBA',
    'pie', 'pieRGBA', 'filled_pie', 'filledPieRGBA', 'trigon', 'trigonRGBA',
    'aatrigon', 'aatrigonRGBA', 'filled_trigon', 'filledTrigonRGBA',
    'polygon', 'polygonRGBA', 'aapolygon', 'aapolygonRGBA',
    'filled_polygon', 'filledPolygonRGBA',
    'textured_polygon', 'texturedPolygon', 'bezier', 'bezierRGBA',
    'thick_line', 'thickLineRGBA'
)


def pixel(surface, x, y, color, sdlgfx=None):
    """Draw pixel with blending enabled if alpha < 255.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X (horizontal) coordinate of the pixel.
        y (int): Y (vertical) coordinate of the pixel.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.pixelRGBA(surface, x, y, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.pixelRGBA failure")

pixelRGBA = pixel


def hline(surface, x1, x2, y, color, sdlgfx=None):
    """Draw horizontal line with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int):  X coordinate of the first point (i.e. left) of the line.
        x2 (int):  X coordinate of the second point (i.e. right) of the line.
        y  (int):  Y coordinate of the points of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.hlineRGBA(surface, x1, x2, y, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.hlineRGBA failure")

hlineRGBA = hline


def vline(surface, x, y1, y2, color, sdlgfx=None):
    """Draw vertical line with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x  (int):  X coordinate of the points of the line.
        y1 (int):  Y coordinate of the first point (i.e. top) of the line.
        y2 (int):  Y coordinate of the second point (i.e. bottom) of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.vlineRGBA(surface, x, y1, y2, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.vlineRGBA failure")

vlineRGBA = vline


def rectangle(surface, rect, color, sdlgfx=None):
    """Draw rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point (i.e. top right) of the
        rectangle.
        y1 (int): Y coordinate of the first point (i.e. top right) of the
        rectangle.
        x2 (int): X coordinate of the second point (i.e. bottom left) of the
        rectangle.
        y2 (int): Y coordinate of the second point (i.e. bottom left) of the
        rectangle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    if sdlgfx.rectangleRGBA(surface, rect.x, rect.y, rect.x + rect.w,
                            rect.y + rect.h, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.rectangleRGBA failure")

rectangleRGBA = rectangle


def rounded_rectangle(surface, rect, rad, color, sdlgfx=None):
    """Draw rounded-corner rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    if sdlgfx.roundedRectangleRGBA(surface,
                                   rect.right - 1, rect.top + 1,
                                   rect.left + 1, rect.bottom - 1,
                                   rad, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.rectangleRGBA failure")


roundedRectangleRGBA = rounded_rectangle


def rounded_box(surface, rect, rad, color, sdlgfx=None):
    """Draw rounded-corner filled rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    if sdlgfx.roundedBoxRGBA(surface,
                             rect.right, rect.top,
                             rect.left, rect.bottom,
                             rad, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.roundedBoxRGBA failure")

roundedBoxRGBA = rounded_box


def box(surface, rect, color, sdlgfx=None):
    """Draw a filled rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    if sdlgfx.boxRGBA(surface, rect.x, rect.y, rect.x + rect.w,
                      rect.y + rect.h, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.boxRGBA failure")

boxRGBA = box


def line(surface, x1, y1, x2, y2, color, sdlgfx=None):
    """Draw line with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the line.
        y1 (int): Y coordinate of the first point of the line.
        x2 (int): X coordinate of the second point of the line.
        y2 (int): Y coordinate of the second point of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.lineRGBA(surface, x1, y1, x2, y2, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.lineRGBA failure")

lineRGBA = line


def aaline(surface, x1, y1, x2, y2, color, sdlgfx=None):
    """Draw anti-aliased line with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the line.
        y1 (int): Y coordinate of the first point of the line.
        x2 (int): X coordinate of the second point of the line.
        y2 (int): Y coordinate of the second point of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.aalineRGBA(surface, x1, y1, x2, y2, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.aalineRGBA failure")

aalineRGBA = aaline


def circle(surface, x, y, r, color, sdlgfx=None):
    """Draw circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the circle.
        y (int): Y coordinate of the center of the circle.
        rad (int): Radius in pixels of the circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.circleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.circleRGBA failure")

circleRGBA = circle


def arc(surface, x, y, r, start, end, color, sdlgfx=None):
    """Draw arc with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the arc.
        y (int): Y coordinate of the center of the arc.
        rad (int): Radius in pixels of the arc.
        start (int): Starting radius in degrees of the arc. 0 degrees is
        down, increasing counterclockwise.
        end (int): Ending radius in degrees of the arc. 0 degrees is down,
        increasing counterclockwise.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.arcRGBA(surface, x, y, r, start, end, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.arcRGBA failure")

arcRGBA = arc


def aacircle(surface, x, y, r, color, sdlgfx=None):
    """Draw anti-aliased circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the aa-circle.
        y (int): Y coordinate of the center of the aa-circle.
        rad (int): Radius in pixels of the aa-circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.aacircleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.aacircleRGBA failure")

aacircleRGBA = aacircle


def filled_circle(surface, x, y, r, color, sdlgfx=None):
    """Draw filled circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the filled circle.
        y (int): Y coordinate of the center of the filled circle.
        rad (int): Radius in pixels of the filled circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.filledCircleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.filledCircleRGBA failure")

filledCircleRGBA = filled_circle


def ellipse(surface, x, y, rx, ry, color, sdlgfx=None):
    """Draw ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the ellipse.
        y (int): Y coordinate of the center of the ellipse.
        rx (int): Horizontal radius in pixels of the ellipse.
        ry (int): Vertical radius in pixels of the ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.ellipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.ellipseRGBA failure")

ellipseRGBA = ellipse


def aaellipse(surface, x, y, rx, ry, color, sdlgfx=None):
    """Draw anti-aliased ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the aa-ellipse.
        y (int): Y coordinate of the center of the aa-ellipse.
        rx (int): Horizontal radius in pixels of the aa-ellipse.
        ry (int): Vertical radius in pixels of the aa-ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.aaellipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.aaellipseRGBA failure")

aaellipseRGBA = aaellipse


def filled_ellipse(surface, x, y, rx, ry, color, sdlgfx=None):
    """Draw filled ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the filled ellipse.
        y (int): Y coordinate of the center of the filled ellipse.
        rx (int): Horizontal radius in pixels of the filled ellipse.
        ry (int): Vertical radius in pixels of the filled ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.filledEllipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.filledEllipseRGBA failure")

filledEllipseRGBA = filled_ellipse


def pie(surface, x, y, r, start, end, color, sdlgfx=None):
    """Draw pie outline with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the pie.
        y (int):   Y coordinate of the center of the pie.
        rad (int): Radius in pixels of the pie.
        start (int): Starting radius in degrees of the pie.
        end (int): Ending radius in degrees of the pie.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.pieRGBA(surface, x, y, r, start, end, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.pieRGBA failure")

pieRGBA = pie


def filled_pie(surface, x, y, r, start, end, color, sdlgfx=None):
    """Draw filled pie with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the filled pie.
        y (int):   Y coordinate of the center of the filled pie.
        rad (int): Radius in pixels of the filled pie.
        start (int): Starting radius in degrees of the filled pie.
        end (int): Ending radius in degrees of the filled pie.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.filledPieRGBA(surface, x, y, r, start, end, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.filledPieRGBA failure")

filledPieRGBA = filled_pie


def trigon(surface, x1, y1, x2, y2, x3, y3, color, sdlgfx=None):
    """Draw trigon (triangle outline) with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the trigon.
        y1 (int): Y coordinate of the first point of the trigon.
        x2 (int): X coordinate of the second point of the trigon.
        y2 (int): Y coordinate of the second point of the trigon.
        x3 (int): X coordinate of the third point of the trigon.
        y3 (int): Y coordinate of the third point of the trigon.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.trigonRGBA(surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.trigonRGBA failure")

trigonRGBA = trigon


def aatrigon(surface, x1, y1, x2, y2, x3, y3, color, sdlgfx=None):
    """Draw anti-aliased trigon (triangle outline) with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the aa-trigon.
        y1 (int): Y coordinate of the first point of the aa-trigon.
        x2 (int): X coordinate of the second point of the aa-trigon.
        y2 (int): Y coordinate of the second point of the aa-trigon.
        x3 (int): X coordinate of the third point of the aa-trigon.
        y3 (int): Y coordinate of the third point of the aa-trigon.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.aatrigonRGBA(
            surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.aatrigonRGBA failure")

aatrigonRGBA = aatrigon


def filled_trigon(surface, x1, y1, x2, y2, x3, y3, color, sdlgfx=None):
    """Draw filled trigon (triangle) with alpha blending.

    Note: Creates vertex array and uses aapolygon routine to render.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the aa-trigon.
        y1 (int): Y coordinate of the first point of the aa-trigon.
        x2 (int): X coordinate of the second point of the aa-trigon.
        y2 (int): Y coordinate of the second point of the aa-trigon.
        x3 (int): X coordinate of the third point of the aa-trigon.
        y3 (int): Y coordinate of the third point of the aa-trigon.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.filledTrigonRGBA(
            surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.filledTrigonRGBA failure")

filledTrigonRGBA = filled_trigon


def polygon(surface, points, color, sdlgfx=None):
    """
    Draw polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    if sdlgfx.polygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.polygonRGBA failure")

polygonRGBA = polygon


def aapolygon(surface, points, color, sdlgfx=None):
    """
    Draw anti-aliased polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the aa-polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    if sdlgfx.aapolygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.aapolygonRGBA failure")

aapolygonRGBA = aapolygon


def filled_polygon(surface, points, color, sdlgfx=None):
    """
    Draw filled polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the filled polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    if sdlgfx.filledPolygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.filledPolygonRGBA failure")

filledPolygonRGBA = filled_polygon


def textured_polygon(
    surface, points, texture, texture_dx, texture_dy, sdlgfx=None
):
    """
    Draw a polygon filled with the given texture.

    Minimum number of points (vertices coordinates) is 3.
    If you move the polygon and want the texture to apear the same you need
    to change the texture_dx and/or texture_dy values.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        points (list of n 2-tuple int): list of X and Y tuples with vertices
        coordinates for the polygon.
        texture (SDL_Surface): the surface to use to fill the polygon
        texture_dx (int): the horizontal offset of the texture relative to
        the screeen.
        texture_dy (int): the vertical offset of the texture relative to
        the screeen.

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    if sdlgfx.texturedPolygon(
            surface, vx, vy, n, texture, texture_dx, texture_dy):
        raise SDLError("sdlgfx.texturedPolygon failure")

texturedPolygon = textured_polygon


def bezier(surface, points, steps, color, sdlgfx=None):
    """
    Draw a bezier curve with alpha blending.

    Minimum number of points (vertices coordinates) is 3.
    Minimum number of steps for interpolation is 2.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        points (list of n 2-tuple int): list of X and Y tuples with points
        of the bezier curve.
        steps (int): Number of steps for the interpolation.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    if sdlgfx.bezierRGBA(surface, vx, vy, n, steps, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.bezierRGBA failure")

bezierRGBA = bezier


def thick_line(surface, x1, y1, x2, y2, width, color, sdlgfx=None):
    """Draw a thick line with alpha blending.

    Width of the line in pixels. Must be greater then 0.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the line.
        y1 (int): Y coordinate of the first point of the line.
        x2 (int): X coordinate of the second point of the line.
        y2 (int): Y coordinate of the second point of the line.
        width (int): Width of the line in pixels. Must be >0.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Raises:
        SDLError
    """
    sdlgfx = sdlgfx_tex if (sdlgfx is None or sdlgfx == "tex") else sdlgfx_sfc
    c = Color(*color)
    if sdlgfx.thickLineRGBA(
            surface, x1, y1, x2, y2, width, c.r, c.g, c.b, c.a):
        raise SDLError("sdlgfx.thickLineRGBA failure")

thickLineRGBA = thick_line


def rotozoom_surface_xy(surface, angle, zoomx, zoomy, smooth):
    """Rotate and zooms a surface.

    Uses different horizontal and vertival scaling factors and optional
    anti-aliasing.

    Rotates and zooms a 32bit or 8bit 'src' surface to newly created 'dst'
    surface. 'angle' is the rotation in degrees, 'zoomx and 'zoomy' scaling
    factors. If 'smooth' is set then the destination 32bit surface is
    anti-aliased. If the surface is not 8bit or 32bit RGBA/ABGR it will be
    converted into a 32bit RGBA format on the fly.

    Args:
    src (SDL_Surface): The surface to rotozoom.
    angle (float): The angle to rotate in degrees.
    zoomx (float): The horizontal scaling factor.
    zoomy (float): The vertical scaling factor.
    smooth (sdl2.sdlgfx.SMOOTHING_OFF|SMOOTHING_ON): Antialiasing flag; set
        to SMOOTHING_ON to enable.

    Returns:
        The new rotozoomed surface."""
    return sdlgfx_tex.rotozoomSurfaceXY(surface, angle, zoomx, zoomy, smooth)

rotozoomSurfaceXY = rotozoom_surface_xy
