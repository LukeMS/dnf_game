"""..."""
from ctypes import (Structure, POINTER, c_int, c_float, c_void_p, c_char,
                    c_char_p, c_double)

from sdl2.dll import DLL
from sdl2.stdinc import Uint8, Uint32, Sint16
from sdl2.render import SDL_Renderer
from sdl2.surface import SDL_Surface

from dnf_game.util import dnf_path

__all__ = (
    "get_dll_file", "SDL2_GFXPRIMITIVES_MAJOR",
    "SDL2_GFXPRIMITIVES_MINOR", "SDL2_GFXPRIMITIVES_MICRO", "pixelColor",
    "pixelRGBA", "hlineColor", "hlineRGBA", "vlineColor", "vlineRGBA",
    "rectangleColor", "rectangleRGBA", "roundedRectangleColor",
    "roundedRectangleRGBA", "boxColor", "boxRGBA", "roundedBoxColor",
    "roundedBoxRGBA", "lineColor", "lineRGBA", "aalineColor", "aalineRGBA",
    "thickLineColor", "thickLineRGBA", "circleColor", "circleRGBA",
    "arcColor", "arcRGBA", "aacircleColor", "aacircleRGBA",
    "filledCircleColor", "filledCircleRGBA", "ellipseColor", "ellipseRGBA",
    "aaellipseColor", "aaellipseRGBA", "filledEllipseColor",
    "filledEllipseRGBA", "pieColor", "pieRGBA", "filledPieColor",
    "filledPieRGBA", "trigonColor", "trigonRGBA", "aatrigonColor",
    "aatrigonRGBA", "filledTrigonColor", "filledTrigonRGBA", "polygonColor",
    "polygonRGBA", "aapolygonColor", "aapolygonRGBA", "filledPolygonColor",
    "filledPolygonRGBA", "texturedPolygon", "bezierColor", "bezierRGBA")

try:
    dll = DLL(
        libinfo="SDL2_gfx", libnames=["pygame_sdl2_gfx"], path=dnf_path())
except RuntimeError as exc:
    raise ImportError(exc)


def get_dll_file():
    """Gets the file name of the loaded SDL2_gfx library."""
    return dll.libfile

_bind = dll.bind_function


SDL2_GFXPRIMITIVES_MAJOR = 1
SDL2_GFXPRIMITIVES_MINOR = 0
SDL2_GFXPRIMITIVES_MICRO = 0

pixelColor = _bind(
    "pixelColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Uint32],
    c_int
)
pixelRGBA = _bind(
    "pixelRGBA",
    [POINTER(SDL_Surface), Sint16, Sint16, Uint8, Uint8, Uint8, Uint8],
    c_int
)
hlineColor = _bind(
    "hlineColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint32],
    c_int
)
hlineRGBA = _bind(
    "hlineRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8,
         Uint8
    ],
    c_int
)
vlineColor = _bind(
    "vlineColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint32],
    c_int
)
vlineRGBA = _bind(
    "vlineRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8,
        Uint8
    ],
    c_int
)
rectangleColor = _bind(
    "rectangleColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
rectangleRGBA = _bind("rectangleRGBA", [
    POINTER(SDL_Surface),
    Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8],
    c_int
)
roundedRectangleColor = _bind(
    "roundedRectangleColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
roundedRectangleRGBA = _bind(
    "roundedRectangleRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8,
        Uint8, Uint8, Uint8
    ],
    c_int
)
boxColor = _bind(
    "boxColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
boxRGBA = _bind(
    "boxRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8,
        Uint8, Uint8
    ],
    c_int
)
roundedBoxColor = _bind(
    "roundedBoxColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
roundedBoxRGBA = _bind(
    "roundedBoxRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8,
        Uint8, Uint8, Uint8
    ],
    c_int
)
lineColor = _bind(
    "lineColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
lineRGBA = _bind(
    "lineRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8,
        Uint8, Uint8
    ],
    c_int
)
aalineColor = _bind(
    "aalineColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
aalineRGBA = _bind(
    "aalineRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8,
        Uint8, Uint8
    ],
    c_int
)
thickLineColor = _bind(
    "thickLineColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint32],
    c_int
)
thickLineRGBA = _bind(
    "thickLineRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8,
        Uint8, Uint8, Uint8
    ],
    c_int
)
circleColor = _bind(
    "circleColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint32],
    c_int
)
circleRGBA = _bind(
    "circleRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8,
        Uint8
    ],
    c_int
)
arcColor = _bind(
    "arcColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32],
    c_int
)
arcRGBA = _bind(
    "arcRGBA",
    [
        POINTER(SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8,
        Uint8, Uint8, Uint8
    ],
    c_int
)
aacircleColor = _bind(
    "aacircleColor",
    [POINTER(SDL_Surface), Sint16, Sint16, Sint16, Uint32],
    c_int
)
aacircleRGBA = _bind("aacircleRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
filledCircleColor = _bind("filledCircleColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Uint32], c_int)
filledCircleRGBA = _bind("filledCircleRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
ellipseColor = _bind("ellipseColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
ellipseRGBA = _bind("ellipseRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
aaellipseColor = _bind("aaellipseColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
aaellipseRGBA = _bind("aaellipseRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
filledEllipseColor = _bind("filledEllipseColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
filledEllipseRGBA = _bind("filledEllipseRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
pieColor = _bind("pieColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
pieRGBA = _bind("pieRGBA", [POINTER(SDL_Surface), Sint16, Sint16,
                            Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
filledPieColor = _bind("filledPieColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
filledPieRGBA = _bind("filledPieRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
trigonColor = _bind("trigonColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
trigonRGBA = _bind("trigonRGBA", [POINTER(SDL_Surface), Sint16, Sint16,
                                  Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
aatrigonColor = _bind("aatrigonColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
aatrigonRGBA = _bind("aatrigonRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
filledTrigonColor = _bind("filledTrigonColor", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int)
filledTrigonRGBA = _bind("filledTrigonRGBA", [POINTER(
    SDL_Surface), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)
polygonColor = _bind("polygonColor", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, Uint32], c_int)
polygonRGBA = _bind("polygonRGBA", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)
aapolygonColor = _bind("aapolygonColor", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, Uint32], c_int)
aapolygonRGBA = _bind("aapolygonRGBA", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)
filledPolygonColor = _bind("filledPolygonColor", [POINTER(
    SDL_Surface), POINTER(Sint16), POINTER(Sint16), c_int, Uint32], c_int)
filledPolygonRGBA = _bind("filledPolygonRGBA", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)
texturedPolygon = _bind("texturedPolygon", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, POINTER(SDL_Surface), c_int, c_int], c_int)
bezierColor = _bind("bezierColor", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, c_int, Uint32], c_int)
bezierRGBA = _bind("bezierRGBA", [POINTER(SDL_Surface), POINTER(
    Sint16), POINTER(Sint16), c_int, c_int, Uint8, Uint8, Uint8, Uint8], c_int)

SMOOTHING_OFF = 0
SMOOTHING_ON = 1
