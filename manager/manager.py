"""SDL2 Tiles Test."""


import os
import sys

import sdl2
import sdl2.ext

RESOURCES = sdl2.ext.Resources(
    os.path.join(os.path.dirname(__file__), "..", "resources"))

from constants import SCR_W, SCR_H, FPS, TILE_W
from manager import Fonts


class Manager(object):
    """Manage scenes and the main loop.

    At each loop the events are passed down to the scene and its updates
    method is called.
    """

    def __init__(
        self, *, width=SCR_W, height=SCR_H, framerate=FPS,
        show_fps=True, show_play_time=False, scene=None
    ):
        """..."""
        self.alive = False
        self._scene = None

        self.show_fps = show_fps
        self.width = width
        self.height = height
        self.fps = framerate
        self.delay = 1 / framerate

        sdl2.ext.init()

        window = sdl2.ext.Window("Tiles", size=(SCR_W, SCR_H),
                                 flags=sdl2.SDL_WINDOW_BORDERLESS)
        self._window = window

        renderer = sdl2.ext.Renderer(window)
        self.renderer = renderer

        factory = SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
        self.factory = factory

        sdl2.sdlttf.TTF_Init()
        self.fonts = Fonts(factory)

        self.tileset = sdl2.ext.load_image(
            RESOURCES.get("tileset{}.png".format(TILE_W)))

        self.spriterenderer = self.factory.create_sprite_render_system(
            window)

        window.show()
        self.renderer.clear()
        if scene:
            self.set_scene(scene)

        self.alive = True

    @property
    def display(self):
        """..."""
        return self._window

    @property
    def scene(self):
        """..."""
        return self._scene

    @property
    def show_fps(self):
        """Show the fps display if True, hide it if False."""
        return self._show_fps

    @show_fps.setter
    def show_fps(self, value):
        """Set the value for _show_fps."""
        if isinstance(value, bool):
            self._show_fps = value
        else:
            raise TypeError(
                "value should be bool but is {}".format(type(value)))

    def execute(self):
        """Main loop handling events and updates."""
        delay = self.delay

        t0 = sdl2.SDL_GetTicks()
        while self.alive:

            t1 = sdl2.SDL_GetTicks()
            dt = (t1 - t0) / 1000
            if dt < delay:
                continue
            self.on_event()
            self.on_update()
            t0 = sdl2.SDL_GetTicks()

        sdl2.ext.quit()
        return 0

    def on_event(self):
        """..."""
        scene = self.scene
        for event in sdl2.ext.get_events():
            # Exit events
            if event.type == sdl2.SDL_QUIT:
                print('sdl2.SDL_QUIT')
                self.quit()
            elif scene:
                scene.on_event(event)

    def on_update(self):
        """Update scene unless specified not to do so."""
        scene = self.scene
        if self.alive and scene:
            self.renderer.clear()

            if scene:
                scene.on_update()

            if self.show_fps:
                self.draw_fps()

    def draw_fps(self):
        """Draw the fps display."""
        pass

    def set_scene(self, scene=None, **kwargs):
        """..."""
        if self.scene:
            self.scene.clear()
        self._scene = scene(_manager=self, **kwargs)


class SpriteFactory(sdl2.ext.SpriteFactory):
    """A factory class for creating Sprite components.

    Subclass of sdl2.ext.SpriteFactory with additional methods.
    """

    def create_sprite_render_system(self, *args, **kwargs):
        """Creates a new SpriteRenderSystem.

        For TEXTURE mode, the passed args and kwargs are ignored and the
        Renderer or SDL_Renderer passed to the SpriteFactory is used.
        """
        if self.sprite_type == sdl2.ext.TEXTURE:
            return TextureSpriteRenderSystem(self.default_args["renderer"])
        else:
            return sdl2.ext.SoftwareSpriteRenderSystem(*args, **kwargs)

    def from_tileset(self, tileset, area):
        """Create a sprite from an area (tile) of a tileset (surface).

        Args:
            tileset (sdl2.surface.SDL_Surface): source surface
            area (rect): tuple with coordinates (x, y, w, h)

        Returns:
            sdl2.ext.sprite.TextureSprite
        """
        surface = tileset
        ssurface = sdl2.ext.subsurface(surface=surface, area=area)
        if self.sprite_type == sdl2.ext.TEXTURE:
            renderer = self.default_args["renderer"]
            texture = sdl2.render.SDL_CreateTextureFromSurface(
                renderer.sdlrenderer, ssurface)
            if not texture:
                raise sdl2.ext.SDLError()
            sprite = sdl2.ext.TextureSprite(texture.contents)
            return sprite
        else:
            raise NotImplementedError()


class TextureSpriteRenderSystem(sdl2.ext.TextureSpriteRenderSystem):
    """A rendering system for TextureSprite components.

    The TextureSpriteRenderSystem class uses a SDL_Renderer as drawing
    device to display TextureSprite objects.
    """

    def render(self, sprites, x=None, y=None):
        """Draw the passed sprites (or sprite).

        x and y are optional arguments that can be used as relative
        drawing location for sprites. If set to None, the location
        information of the sprites are used. If set and sprites is an
        iterable, such as a list of TextureSprite objects, x and y are
        relative location values that will be added to each individual
        sprite's position. If sprites is a single TextureSprite, x and y
        denote the absolute position of the TextureSprite, if set.
        """
        r = sdl2.rect.SDL_Rect(0, 0, 0, 0)
        rcopy = sdl2.render.SDL_RenderCopyEx
        if sdl2.ext.compat.isiterable(sprites):
            renderer = self.sdlrenderer
            x = x or 0
            y = y or 0
            for sprite in sprites:
                r.x = x + sprite.x
                r.y = y + sprite.y
                r.w, r.h = sprite.size
                if rcopy(renderer, sprite.texture, None, r, sprite.angle,
                         sprite.center, sprite.flip) == -1:
                    raise sdl2.ext.SDLError()
        else:
            r.x = sprites.x
            r.y = sprites.y
            r.w, r.h = sprites.size

            dx = 0
            if x is not None:
                if x < 0:
                    dx = abs(x)
                else:
                    r.x = x

            dy = 0
            if y is not None:
                if y < 0:
                    dy = abs(y)
                else:
                    r.y = y

            if dx or dy:
                src_r = sdl2.rect.SDL_Rect(dx, dy, r.w - dx, r.h - dy)
                if rcopy(self.sdlrenderer, sprites.texture, src_r, r,
                         sprites.angle, sprites.center, sprites.flip) == -1:
                    raise sdl2.ext.SDLError()
            else:
                if rcopy(self.sdlrenderer, sprites.texture, None, r,
                         sprites.angle, sprites.center, sprites.flip) == -1:
                    raise sdl2.ext.SDLError()
        sdl2.render.SDL_RenderPresent(self.sdlrenderer)
