"""Pure Python implementation of Pygame/PyGameSDL2's transform.

Original available at:
    github.com/renpy/pygame_sdl2/blob/master/src/pygame_sdl2/transform.pyx

----------------------------------------------------------------------------
           _ _                    _                                _
     /\   | | |                  | |                              | |
    /  \  | | |_ ___ _ __ ___  __| |  ___  ___  _   _ _ __ ___ ___| |
   / /\ \ | | __/ _ \ '__/ _ \/ _` | / __|/ _ \| | | | '__/ __/ _ \ |
  / ____ \| | ||  __/ | |  __/ (_| | \__ \ (_) | |_| | | | (_|  __/_|
 /_/    \_\_|\__\___|_|  \___|\__,_| |___/\___/ \__,_|_|  \___\___(_)

----------------------------------------------------------------------------

PygameSDL2 Notice:
----------------------------------------------------------------------------
# Copyright 2014 Patrick Dawson <pat@dw.is>
#                Tom Rothamel <tom@rothamel.us>
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


import sdl2
from dnf_game.util.ext import gfxdraw
from dnf_game.util.ext.surface import Surface


def flip(surface, xbool, ybool):
    """Flip vertically and horizontally.

    This can flip a Surface either vertically, horizontally, or both.
    Flipping a Surface is nondestructive and returns a new Surface with the
    same dimensions.

    Args:
        surface
        xbool
        ybool

    Returns:
        Surface
    """
    rv = Surface(surface.get_size(), surface.get_flags(), surface)
    src = surface.surface
    dest = rv.surface

    for y in range(src.h):

        src_pixel = ((src.pixels) + y * src.pitch)
        src_end = src_pixel + src.w

        if ybool:
            dest_pixel = ((dest.pixels) + (dest.h - y - 1) * dest.pitch)
        else:
            dest_pixel = ((dest.pixels) + y * dest.pitch)

        if xbool:
            dest_pixel += (src.w - 1)
            dest_delta = -1
        else:
            dest_delta = 1

        while src_pixel < src_end:
            dest_pixel[0] = src_pixel[0]
            src_pixel += 1
            dest_pixel += dest_delta

    return rv


def scale(surface, size, DestSurface=None):
    """Resize to new resolution.

    Resizes the Surface to a new resolution. This is a fast scale operation
    that does not sample the results.

    An optional destination surface can be used, rather than have it create a
    new one. This is quicker if you want to repeatedly scale something.
    However the destination must be the same size as the (width, height)
    passed in. Also the destination surface must be the same format.

    Usage:
        scale(Surface, (width, height), DestSurface = None) -> Surface
    """
    if DestSurface is None:
        surf_out = Surface(size, 0, surface)
    else:
        surf_out = DestSurface

    SDL_SetSurfaceBlendMode(surface.surface, SDL_BLENDMODE_NONE)
    err = SDL_UpperBlitScaled(surface.surface, None, surf_out.surface, None)

    if err:
        raise error()

    return surf_out


def rotate(surface, angle):
    """..."""
    return rotozoom(surface, angle, 1.0, SMOOTHING_OFF)


def rotozoom(surface, angle, scale, smooth=1):
    """..."""
    rsurf = rotozoomSurface(surface.surface, angle, scale, smooth)

    if rsurf is None:
        raise sdl2.SDLError()

    rv = Surface(())
    rv.take_surface(rsurf)

    return rv

def get_at(surf, x, y):
    """..."""
    if x < 0:
        x = 0
    elif x >= surf.w:
        x = surf.w - 1
    if y < 0:
        y = 0
    elif y >= surf.h:
        y = surf.h - 1

    p = surf.pixels
    p += y * (surf.pitch // sizeof(uint32_t))
    p += x
    return p[0]

def set_at(surf, x, y, color):
    """..."""
    p = surf.pixels
    p += y * (surf.pitch // sizeof(uint32_t))
    p += x
    p[0] = color


def scale2x(surface, DestSurface=None):
    """Specialized image doubler.

    This will return a new image that is double the size of the original. It
    uses the AdvanceMAME Scale2X algorithm which does a ‘jaggie-less’ scale
    of bitmap graphics.

    This really only has an effect on simple images with solid colors. On
    photographic and antialiased images it will look like a regular
    unfiltered scale.

    An optional destination surface can be used, rather than have it create a
    new one. This is quicker if you want to repeatedly scale something.
    However the destination must be twice the size of the source surface
    passed in. Also the destination surface must be the same format.

    Usage:
        scale2x(Surface, DestSurface = None) -> Surface
    """
    if surface.get_bytesize() != 4:
        raise sdl2.SDLError("Surface has unsupported bytesize.")

    surf_out = DestSurface
    if surf_out is None:
        surf_out = Surface((surface.get_width() * 2,
                            surface.get_height() * 2), 0, surface)

    surface.lock()
    surf_out.lock()

    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            # Get the surrounding 9 pixels.
            a = get_at(surface.surface, x - 1, y - 1)
            b = get_at(surface.surface, x, y - 1)
            c = get_at(surface.surface, x + 1, y - 1)

            d = get_at(surface.surface, x - 1, y)
            e = get_at(surface.surface, x, y)
            f = get_at(surface.surface, x + 1, y)

            g = get_at(surface.surface, x - 1, y + 1)
            h = get_at(surface.surface, x, y + 1)
            i = get_at(surface.surface, x + 1, y + 1)

            # Expand the center pixel.
            if b != h and d != f:
                e0 = d if d == b else e
                e1 = f if b == f else e
                e2 = d if d == h else e
                e3 = f if h == f else e
            else:
                e0 = e1 = e2 = e3 = e

            set_at(surf_out.surface, x * 2, y * 2, e0)
            set_at(surf_out.surface, (x * 2) + 1, y * 2, e1)
            set_at(surf_out.surface, x * 2, (y * 2) + 1, e2)
            set_at(surf_out.surface, (x * 2) + 1, (y * 2) + 1, e3)

    surf_out.unlock()
    surface.unlock()

    return surf_out

def smoothscale(surface, size, DestSurface=None):
    """Scale a surface to an arbitrary size smoothly.

    Uses one of two different algorithms for scaling each dimension of the
    input surface as required. For shrinkage, the output pixels are area
    averages of the colors they cover. For expansion, a bilinear filter is
    used. For the amd64 and i686 architectures, optimized MMX routines are
    included and will run much faster than other machine types. The size
    is a 2 number sequence for (width, height). This function only works
    for 24-bit or 32-bit surfaces. An exception will be thrown if the
    input surface bit depth is less than 24.

    Usage:
        smoothscale(Surface, (width, height), DestSurface = None)

    Returns:
        Surface
    """
    scale_x = size[0] // surface.w
    scale_y = size[1] // surface.h

    rsurf = None

    rsurf = gfxdraw.rotozoomSurfaceXY(
        surface.surface, 0.0,
        scale_x, scale_y,
        sdl2.sdlgfx.SMOOTHING_ON)

    if rsurf is None:
        raise sdl2.SDLError

    # This is inefficient.
    if DestSurface:
        sdl2.SDL_SetSurfaceBlendMode(rsurf.surface,
            sdl2.SDL_BLENDMODE_NONE)
        sdl2.SDL_UpperBlit(rsurf.surface, None, DestSurface.surface, None)

    return rsurf
