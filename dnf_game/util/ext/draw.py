"""..."""

from dnf_game.util.ext import gfxdraw


def ellipse(surface, color, rect, width=0):
    """Draw a round shape inside a rectangle.

    Draws an elliptical shape on the Surface. The given rectangle is the area
    that the circle will fill. The width argument is the thickness to draw
    the outer edge. If width is zero then the ellipse will be filled.

    Usage:
        ellipse(Surface, color, Rect, width=0) -> Rect
    """
    try:
        surface = surface.surface
    except AttributeError:
        pass
    if not width:
        gfxdraw.filled_ellipse(
            surface, rect.x + rect.w // 2, rect.y + rect.h // 2,
            rect.w // 2, rect.h // 2, color, sdlgfx="sfc")
    else:
        width = min(width, min(rect.w, rect.h) / 2)
        for loop in range(width):
            gfxdraw.ellipse(
                surface, rect.x + rect.w // 2, rect.y + rect.h // 2,
                rect.w // 2 - loop, rect.h // 2 - loop, color, sdlgfx="sfc")
