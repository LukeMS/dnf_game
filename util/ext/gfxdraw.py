"""Pure Python implementation of Pygame/PyGameSDL2's gfxdraw.

Original available at:
    github.com/renpy/pygame_sdl2/blob/master/src/pygame_sdl2/gfxdraw.pyx

----------------------------------------------------------------------------
           _ _                    _                                  _
     /\   | | |                  | |                                | |
    /  \  | | |_ ___ _ __ ___  __| |    ___  ___  _   _ _ __ ___ ___| |
   / /\ \ | | __/ _ \ '__/ _ \/ _` |   / __|/ _ \| | | | '__/ __/ _ \ |
  / ____ \| | ||  __/ | |  __/ (_| |   \__ \ (_) | |_| | | | (_|  __/_|
 /_/    \_\_|\__\___|_|  \___|\__,_|   |___/\___/ \__,_|_|  \___\___(_)

----------------------------------------------------------------------------

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

from sdl2 import sdlgfx
from sdl2.ext.color import Color
from dnf_game.util.ext.rect import Rect


def pixel(surface, x, y, color):
    """Draw pixel with blending enabled if alpha < 255.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X (horizontal) coordinate of the pixel.
        y (int): Y (vertical) coordinate of the pixel.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.pixelRGBA(surface, x, y, c.r, c.g, c.b, c.a)

pixelRGBA = pixel


def hline(surface, x1, x2, y, color):
    """Draw horizontal line with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int):  X coordinate of the first point (i.e. left) of the line.
        x2 (int):  X coordinate of the second point (i.e. right) of the line.
        y  (int):  Y coordinate of the points of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.hlineRGBA(surface, x1, x2, y, c.r, c.g, c.b, c.a)

hlineRGBA = hline


def vline(surface, x, y1, y2, color):
    """Draw vertical line with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x  (int):  X coordinate of the points of the line.
        y1 (int):  Y coordinate of the first point (i.e. top) of the line.
        y2 (int):  Y coordinate of the second point (i.e. bottom) of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.vlineRGBA(surface, x, y1, y2, c.r, c.g, c.b, c.a)

vlineRGBA = vline


def rectangle(surface, rect, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    sdlgfx.rectangleRGBA(surface, rect.x, rect.y, rect.x + rect.w,
                         rect.y + rect.h, c.r, c.g, c.b, c.a)

rectangleRGBA = rectangle


def rounded_rectangle(surface, rect, rad, color):
    """Draw rounded-corner rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    return sdlgfx.roundedRectangleRGBA(surface,
                                       rect.right - 1, rect.top + 1,
                                       rect.left + 1, rect.bottom - 1,
                                       rad, c.r, c.g, c.b, c.a)

roundedRectangleRGBA = rounded_rectangle


def rounded_box(surface, rect, rad, color):
    """Draw rounded-corner filled rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    return sdlgfx.roundedBoxRGBA(surface,
                                 rect.right - 1, rect.top + 1,
                                 rect.left + 1, rect.bottom - 1,
                                 rad, c.r, c.g, c.b, c.a)

roundedBoxRGBA = rounded_box


def box(surface, rect, color):
    """Draw a filled rectangle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        rect (Rect): A rectangle representing the area to be draw.
        rad (int): The radius of the corner arc.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    if not isinstance(rect, Rect):
        rect = Rect(rect)
    return sdlgfx.boxRGBA(surface, rect.x, rect.y, rect.x + rect.w,
                          rect.y + rect.h, c.r, c.g, c.b, c.a)

boxRGBA = box


def line(surface, x1, y1, x2, y2, color):
    """Draw line with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the line.
        y1 (int): Y coordinate of the first point of the line.
        x2 (int): X coordinate of the second point of the line.
        y2 (int): Y coordinate of the second point of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.lineRGBA(surface, x1, y1, x2, y2, c.r, c.g, c.b, c.a)

lineRGBA = line


def aaline(surface, x1, y1, x2, y2, color):
    """Draw anti-aliased line with alpha blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x1 (int): X coordinate of the first point of the line.
        y1 (int): Y coordinate of the first point of the line.
        x2 (int): X coordinate of the second point of the line.
        y2 (int): Y coordinate of the second point of the line.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.aalineRGBA(surface, x1, y1, x2, y2, c.r, c.g, c.b, c.a)

aalineRGBA = aaline


def circle(surface, x, y, r, color):
    """Draw circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the circle.
        y (int): Y coordinate of the center of the circle.
        rad (int): Radius in pixels of the circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.circleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a)

circleRGBA = circle


def arc(surface, x, y, r, start, end, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.arcRGBA(surface, x, y, r, start, end, c.r, c.g, c.b, c.a)

arcRGBA = arc


def aacircle(surface, x, y, r, color):
    """Draw anti-aliased circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the aa-circle.
        y (int): Y coordinate of the center of the aa-circle.
        rad (int): Radius in pixels of the aa-circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.aacircleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a)

aacircleRGBA = aacircle


def filled_circle(surface, x, y, r, color):
    """Draw filled circle with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the filled circle.
        y (int): Y coordinate of the center of the filled circle.
        rad (int): Radius in pixels of the filled circle.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.filledCircleRGBA(surface, x, y, r, c.r, c.g, c.b, c.a)

filledCircleRGBA = filled_circle


def ellipse(surface, x, y, rx, ry, color):
    """Draw ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the ellipse.
        y (int): Y coordinate of the center of the ellipse.
        rx (int): Horizontal radius in pixels of the ellipse.
        ry (int): Vertical radius in pixels of the ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.ellipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a)

ellipseRGBA = ellipse


def aaellipse(surface, x, y, rx, ry, color):
    """Draw anti-aliased ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the aa-ellipse.
        y (int): Y coordinate of the center of the aa-ellipse.
        rx (int): Horizontal radius in pixels of the aa-ellipse.
        ry (int): Vertical radius in pixels of the aa-ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.aaellipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a)

aaellipseRGBA = aaellipse


def filled_ellipse(surface, x, y, rx, ry, color):
    """Draw filled ellipse with blending.

    Args:
        surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
        with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
        x (int): X coordinate of the center of the filled ellipse.
        y (int): Y coordinate of the center of the filled ellipse.
        rx (int): Horizontal radius in pixels of the filled ellipse.
        ry (int): Vertical radius in pixels of the filled ellipse.
        color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.filledEllipseRGBA(surface, x, y, rx, ry, c.r, c.g, c.b, c.a)

filledEllipseRGBA = filled_ellipse


def pie(surface, x, y, r, start, end, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.pieRGBA(surface, x, y, r, start, end, c.r, c.g, c.b, c.a)

pieRGBA = pie


def filled_pie(surface, x, y, r, start, end, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.filledPieRGBA(
        surface, x, y, r, start, end, c.r, c.g, c.b, c.a)

filledPieRGBA = filled_pie


def trigon(surface, x1, y1, x2, y2, x3, y3, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.trigonRGBA(
        surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

trigonRGBA = trigon


def aatrigon(surface, x1, y1, x2, y2, x3, y3, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.aatrigonRGBA(
        surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

aatrigonRGBA = aatrigon


def filled_trigon(surface, x1, y1, x2, y2, x3, y3, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.filledTrigonRGBA(
        surface, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

filledTrigonRGBA = filled_trigon


def polygon(surface, points, color):
    """
    Draw polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    return sdlgfx.polygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a)

polygonRGBA = polygon


def aapolygon(surface, points, color):
    """
    Draw anti-aliased polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the aa-polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    return sdlgfx.aapolygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a)

aapolygonRGBA = aapolygon


def filled_polygon(surface, points, color):
    """
    Draw filled polygon with alpha blending.

    Minimum number of points (vertices coordinates) is 3.

    Args:
    surface (SDL_RENDERER, SDL_TEXTURE): The renderer or texture (created
    with the SDL_TEXTUREACCESS_TARGET flag) to draw on.
    points (list of n 2-tuple int): list of X and Y tuples with vertices
    coordinates for the filled polygon.
    color (Color or 4-tuple with ints between 0-255): RGBA color

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    return sdlgfx.filledPolygonRGBA(surface, vx, vy, n, c.r, c.g, c.b, c.a)

filledPolygonRGBA = filled_polygon


def textured_polygon(surface, points, texture, texture_dx, texture_dy):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    return sdlgfx.texturedPolygon(
        surface, vx, vy, n, texture, texture_dx, texture_dy)

texturedPolygon = textured_polygon


def bezier(surface, points, steps, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    lx, ly = zip(*points)

    vx = (ctypes.c_short * len(lx))(*lx)
    vy = (ctypes.c_short * len(ly))(*ly)

    n = len(vy)

    return sdlgfx.bezierRGBA(surface, vx, vy, n, steps, c.r, c.g, c.b, c.a)

bezierRGBA = bezier


def thick_line(surface, x1, y1, x2, y2, width, color):
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

    Returns:
        Returns 0 on success, -1 on failure.
    """
    c = Color(*color)
    return sdlgfx.thickLineRGBA(
        surface, x1, y1, x2, y2, width, c.r, c.g, c.b, c.a)

thickLineRGBA = thick_line
