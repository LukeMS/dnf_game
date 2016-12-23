"""..."""

from contextlib import contextmanager
import ctypes
import os

import sdl2
import sdl2.ext

from dnf_game.data.constants import SCR_W, SCR_H, FPS, TILE_W
from dnf_game.data.tiles_index import TilesetIndex
from dnf_game.scene_manager.resources import FontsManager
from dnf_game.scene_manager.base_entity import ManagerSingletonMeta
from dnf_game.util.ext import time
from dnf_game.util.ext.namedtuple_with_abc import namedtuple
from dnf_game.util.ext.rect import Rect

RESOURCES = sdl2.ext.Resources(
    os.path.join(os.path.dirname(__file__), "..", "resources"))
TILESET = sdl2.ext.load_image(RESOURCES.get("tileset{}.png".format(TILE_W)))


class Manager(metaclass=ManagerSingletonMeta):
    """Manage scenes and the main loop.

    At each loop the events are passed down to the scene and its updates
    method is called.
    """

    def __init__(
        self, *, width=SCR_W, height=SCR_H, framerate=FPS, show_fps=True,
        show_play_time=False, scene=None, test=False, scene_args=None,
        opacity=255, window_color=None
    ):
        """
        Args:
            opacity (int): a number from 0 to 255, where 0 will make the
            window fully transparent (invisible) and 255 fully opaque (
            opacity value will be ignored in that case)
        """
        self.alive = False
        self._scene = None

        self.show_fps = show_fps
        self.width = width
        self.height = height
        self.fps = framerate
        self.test = test

        sdl2.ext.init()

        window = sdl2.ext.Window("Tiles", size=(SCR_W, SCR_H),
                                 flags=sdl2.SDL_WINDOW_BORDERLESS)
        if opacity < 255:
            sdl2.video.SDL_SetWindowOpacity(window.window, opacity / 255)
        sfc = sdl2.SDL_GetWindowSurface(window.window).contents
        opf = sfc.format.contents

        self._window = window
        self.opacity = opacity
        self.window_color = window_color or (0, 0, 0, 255)

        renderer = sdl2.ext.Renderer(window)
        self.renderer = renderer

        factory = SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
        factory.opf = opf
        self.factory = factory

        sdl2.sdlttf.TTF_Init()
        self.fonts = FontsManager(factory)

        self.tile_size = TILE_W

        self.spriterenderer = self.factory.create_sprite_render_system(
            window)

        window.show()
        # self.renderer.clear()
        scene_args = scene_args or {}
        if scene:
            self.set_scene(scene, **scene_args)

        sdl2.SDL_RaiseWindow(window.window)
        self.alive = True
        self.get_mouse_state()
        self.clock = time.Clock()

    def get_mouse_state(self):
        """..."""
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        self._mouse_x = x.value
        self._mouse_y = y.value
        return self._mouse_x, self._mouse_y

    @property
    def scene(self):
        """..."""
        return self._scene

    @property
    def fonts(self):
        """super__doc__."""
        return self._fonts

    @fonts.setter
    def fonts(self, val):
        """super__doc__."""
        self._fonts = val

    @property
    def factory(self):
        """super__doc__."""
        return self._factory

    @factory.setter
    def factory(self, val):
        """super__doc__."""
        self._factory = val

    def execute(self):
        """Main loop handling events and updates."""
        while self.alive:

            self.ms = self.clock.tick(self.fps)
            self.on_event()
            self.on_update()

        sdl2.ext.quit()
        return 0

    def on_event(self):
        """Handle the events and distribute them."""
        scene = self.scene
        if scene is None:
            return
        for event in sdl2.ext.get_events():
            # Exit events
            if event.type == sdl2.SDL_QUIT:
                self.quit()
            if event.type == sdl2.SDL_WINDOWEVENT_FOCUS_GAINED:
                self.on_update()

            self.key_mods = modifiers = self._modifiers_translate(
                event.key.keysym.mod)

            if event.type == sdl2.SDL_KEYUP:
                scene.on_key_release(event=event, mod=modifiers)
            elif event.type == sdl2.SDL_KEYDOWN:
                scene.on_key_press(event=event, mod=modifiers)
            elif event.type == sdl2.SDL_MOUSEMOTION:
                x = event.motion.x
                y = event.motion.y
                buttons = event.motion.state
                self._mouse_x = x
                self._mouse_y = y
                dx = x - self._mouse_x
                dy = y - self._mouse_y
                if buttons & sdl2.SDL_BUTTON_LMASK:
                    scene.on_mouse_drag(x=x, y=y, dx=dx, dy=dy,
                                        button="LEFT")
                elif buttons & sdl2.SDL_BUTTON_MMASK:
                    scene.on_mouse_drag(x=x, y=y, dx=dx, dy=dy,
                                        button="MIDDLE")
                elif buttons & sdl2.SDL_BUTTON_RMASK:
                    scene.on_mouse_drag(x=x, y=y, dx=dx, dy=dy,
                                        button="RIGHT")
                else:
                    scene.on_mouse_motion(x=x, y=y, dx=dx, dy=dy)
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x = event.button.x
                y = event.button.y

                button_n = event.button.button
                if button_n == sdl2.SDL_BUTTON_LEFT:
                    button = "LEFT"
                elif button_n == sdl2.SDL_BUTTON_RIGHT:
                    button = "RIGHT"
                elif button_n == sdl2.SDL_BUTTON_MIDDLE:
                    button = "MIDDLE"

                double = bool(event.button.clicks - 1)

                scene.on_mouse_press(event=event, x=x, y=y,
                                     button=button, double=double)

            elif event.type == sdl2.SDL_MOUSEWHEEL:
                offset_x = event.wheel.x
                offset_y = event.wheel.y
                scene.on_mouse_scroll(event=event,
                                      offset_x=offset_x, offset_y=offset_y)
        return

    def _modifiers_translate(self, modifiers):
        _modifiers = set()
        if modifiers & (sdl2.SDLK_LSHIFT | sdl2.SDLK_RSHIFT):
            _modifiers.add("SHIFT")
        if modifiers & (sdl2.SDLK_LCTRL | sdl2.SDLK_RCTRL):
            _modifiers.add("CTRL")
        if modifiers & (sdl2.SDLK_LALT | sdl2.SDLK_RALT):
            _modifiers.add("ALT")
        return _modifiers

    def on_update(self):
        """Update scene unless specified not to do so."""
        def update():
            scene.on_update()
            if self.show_fps:
                self.draw_fps()

        scene = self.scene
        if self.alive and scene:
            if scene:
                if not scene.ignore_regular_update:
                    self.renderer.clear(self.window_color)
                    update()
                    self.present()
            if self.test:
                self.alive = False

    def present(self):
        """Flip."""
        sdl2.render.SDL_RenderPresent(self.spriterenderer.sdlrenderer)

    def draw_fps(self):
        """Draw the fps display."""
        ms = self.ms
        if self.show_fps and self.scene:
            text = "FPS: %.3d" % ms
            self.scene.draw_fps(text)

    def set_scene(self, scene=None, **kwargs):
        """..."""
        if self.scene:
            self.scene.clear()
        self._scene = scene(manager=self, **kwargs)


class SpriteFactory(sdl2.ext.SpriteFactory):
    """A factory class for creating Sprite components.

    Subclass of sdl2.ext.SpriteFactory with additional methods.
    """

    @contextmanager
    def new_render_target(self, target):
        """Set a context for the render target.

        When done, set it to None.

        Args:
            target (SDL_RENDERER, SDL_TEXTURE): the target of the renderer
            to be used during this context.
        """
        renderer = self.default_args["renderer"]
        sdl2.SDL_SetRenderTarget(renderer.sdlrenderer, target)
        yield
        sdl2.SDL_SetRenderTarget(renderer.sdlrenderer, None)

    def create_sprite_render_system(self, *args, **kwargs):
        """Create a new SpriteRenderSystem.

        For TEXTURE mode, the passed args and kwargs are ignored and the
        Renderer or SDL_Renderer passed to the SpriteFactory is used.
        """
        if self.sprite_type == sdl2.ext.TEXTURE:
            return TextureSpriteRenderSystem(self.default_args["renderer"])
        else:
            raise NotImplementedError()

    def from_surface(self, tsurface, free=False, position=None):
        """Create a Sprite from the passed SDL_Surface.

        If free is set to True, the passed surface will be freed
        automatically.
        """
        sprite = super().from_surface(tsurface, free)
        sprite.__class__ = TextureSprite
        if position:
            sprite.position = position
        return sprite

    def from_new_texture(self, w, h, drawable=True):
        """..."""
        sdlrenderer = self.default_args["renderer"].sdlrenderer.contents
        access = sdl2.SDL_TEXTUREACCESS_TARGET if drawable else None
        sprite = self.create_texture_sprite(sdlrenderer, (w, h),
                                            access=access)
        sprite.__class__ = TextureSprite
        return sprite

    def from_tileset(
        self, *, tile=None, pos=None, var=None, _id=None, area=None,
        position=None, rect=None, color=None
    ):
        """Create a sprite from a tile name or id code.

        Args:
            tile (str): name ot the tile type
            pos (int): tile position relative to auto-tiling
            var (int): tile variation
            _id (int): tile ordinal position on the tileset (e.g.: _id=127)
            area (rect): tuple with coordinates (x, y, w, h)

        Returns:
            sdl2.ext.sprite.TextureSprite
        """
        if position:
            raise DeprecationWarning(
                "Position not used anymore, use rect instead.")
        area = area or TilesetIndex.get_tile_rect(
            tile=tile, var=var, pos=pos, _id=_id)
        sprite = self._from_tileset_area(area)
        sprite.set_rect(rect)
        return sprite

    def _from_tileset_area(self, area, tileset=TILESET):
        """Create a sprite from an area (tile) of a tileset (surface).

        Args:
            area (rect): tuple with coordinates (x, y, w, h)
            tileset (sdl2.surface.SDL_Surface): source surface

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
            sprite = TextureSprite(texture.contents)
            return sprite
        else:
            raise NotImplementedError()

    def from_color(self, *, rect, color=None, bpp=32, masks=None):
        """Create a sprite with a certain color."""
        masks = masks or (0xFF000000, 0x00FF0000, 0x0000FF00, 0x000000FF)
        color = color or (0, 0, 0, 255)
        sprite = super().from_color(color, rect.size, bpp, masks)
        sprite.__class__ = TextureSprite
        sprite.set_rect(rect)
        return sprite

    def create_surface(self, w, h, bpp=32, masks=None):
        """..."""
        masks = masks or (0xFF000000, 0x00FF0000, 0x0000FF00, 0x000000FF)
        rmask, gmask, bmask, amask = masks
        return sdl2.SDL_CreateRGBSurface(0, w, h, bpp,
                                         rmask, gmask, bmask, amask)

    def from_gradient(
        self, *, rect, color_start=None, color_end=None, mode=None, masks=None
    ):
        """..."""
        def step(i):
            if mode in ("h", "H"):
                dest_rect.x = i
                # dest_rect.w = 1
            elif mode in ("v", "V"):
                dest_rect.y = i
                # dest_rect.h = 1
        fill_rect = sdl2.SDL_FillRect
        map_rgba = sdl2.SDL_MapRGBA
        convert_to_color = sdl2.ext.convert_to_color

        mode = mode or "v"
        w, h = rect.size
        color_start = color_start or (10, 36, 106, 255)
        color_end = color_end or (166, 202, 240, 255)

        dest_rect = sdl2.rect.SDL_Rect(0, 0, w, h)
        cur_r, cur_g, cur_b, cur_a = color_start
        end_r, end_g, end_b, end_a = color_end

        # SDL_CreateRGBSurface(flags, width, height, depth(bits), r, g, b, a)
        sfc = self.create_surface(w, h)

        # loses opacity!
        # sfc = sdl2.SDL_ConvertSurface(sfc, self.opf, 0)

        fmt = sfc.contents.format.contents

        if mode in ("h", "H"):
            div = w
        elif mode in ("v", "V"):
            div = h

        d_r = (end_r - cur_r) / div
        d_g = (end_g - cur_g) / div
        d_b = (end_b - cur_b) / div
        d_a = (end_a - cur_a) / div
        for i in range(div):
            step(i)
            color = convert_to_color((cur_r, cur_g, cur_b, cur_a))
            color = map_rgba(fmt, color.r, color.g, color.b, color.a)
            # SDL_FillRect(dst, rect, color)
            fill_rect(sfc, dest_rect, color)
            cur_r += d_r
            cur_g += d_g
            cur_b += d_b
            cur_a += d_a

        sprite = self.from_surface(sfc.contents, True)
        sprite.set_rect(rect)
        return sprite


class TextureSprite(sdl2.ext.TextureSprite):
    """A simple, visible, texture-based 2D object, using a renderer."""

    frame_rect = None

    def flip_sprite(self, mode=None):
        """..."""
        if mode in ("h", "H"):
            self.flip ^= sdl2.SDL_FLIP_HORIZONTAL
        elif mode in ("v", "V"):
            self.flip ^= sdl2.SDL_FLIP_VERTICAL
        else:
            self.flip = sdl2.SDL_FLIP_NONE

    def get_rect(self, **kwargs):
        """Get the rectangular area of the sprite.

        Returns a new rectangle covering the sprite area. This rectangle will
        have the sprite's x, y, width and height.

        You can pass keyword argument values to this function. These named
        values will be applied to the attributes of the Rect before it is
        returned. An example would be ‘mysurf.get_rect(center=(100,100))’
        to create a rectangle for the Surface centered at a given position.

        Usage:
            get_rect()

        Returns:
            Rect
        """
        r = Rect(self.position, self.size)
        for k, v in kwargs.items():
            setattr(r, k, v)
        return r

    def get_alpha_mod(self):
        """Get the alpha value multiplier for render copy operations.

        Returns:
            (int): integer alpha value.
        """
        alpha = ctypes.c_uint8(0)
        sdl2.SDL_GetTextureAlphaMod(self.texture, ctypes.byref(alpha))
        return alpha.value

    def get_color_mod(self):
        """Get the color value multiplier for render copy operations.

        Returns:
            (int), (int), (int): 3-tuple of rgb integer values (RGB).
        """
        r = ctypes.c_uint8(0)
        g = ctypes.c_uint8(0)
        b = ctypes.c_uint8(0)
        sdl2.SDL_GetTextureAlphaMod(self.texture,
                                    ctypes.byref(r),
                                    ctypes.byref(g),
                                    ctypes.byref(b))
        return r.value, g.value, b.value

    def set_alpha_mod(self, alpha=None):
        """Set a alpha value multiplier for render copy operations.

        When this texture is rendered, during the copy operation the source
        alpha value is modulated by this alpha value according to the
        following formula:
            srcA = srcA * (alpha / 255)

        Args:
            alpha (int): integer between 0 and 255

        Returns:
            None
        """
        alpha = alpha or 255
        sdl2.SDL_SetTextureAlphaMod(self.texture, alpha)

    def set_color_mod(self, color=None):
        """Set a color value multiplier for render copy operations.

        When this texture is rendered, during the copy operation each source
        color channel is modulated by the appropriate color value according
        to the following formula:
            srcC = srcC * (color / 255)

        Args:
            color (3-tuple of ints): rgb color with values between 0 and 255

        Returns:
            None
        """
        color = color or (255, 255, 255)
        sdl2.SDL_SetTextureColorMod(self.texture, *color)

    def set_animation(self, cols, rows, col_w, row_h, col=0, row=0):
        """"Set animation frames parameters.

        Args:
            cols (int): number of frame columns
            rows (int): number of frame rows
            col_w (int): width of each column, in pixels
            row_h (int): height of each row, in pexels
            col (int): the column of the desired starting frame
            row (int): the row of the desired starting frame

        Returns:
            TextureSprite (self): reference to self instance, making it
            possible to use this method on the object creation (see Usage
            below).

        Usage:
                # here a 10x1 area of 32x32 tiles is used
                sprite = TextureSprite(**kwargs).set_animation(
                    10, 1, 32, 32)
        """
        self.cols = cols
        self.rows = rows
        self.col_w = col_w
        self.row_h = row_h
        self.col = col
        self.row = row
        self._size = col_w, row_h
        self.set_current_rect()

        return self

    def set_current_rect(self):
        """..."""
        self.frame_rect = sdl2.rect.SDL_Rect(self.col * self.col_w,
                                             self.row * self.row_h,
                                             self.col_w,
                                             self.row_h)

    def step(self, col=0, row=0):
        """..."""
        if not col and not row:
            return
        if col:
            self.col += col
            self.col = self.col % self.cols
        if row:
            self.row += row
            self.row = self.row % self.rows
        self.set_current_rect()

    def reset_alpha_mod(self):
        """Redefine the alpha multiplier on the sprite texture to default."""
        self.set_alpha_mod(alpha=None)

    def reset_color_mod(self):
        """Redefine the color multiplier on the sprite texture to default."""
        self.set_color_mod(color=None)

    @property
    def bottomright(self):
        """..."""
        return self.get_rect().bottomright

    @property
    def topleft(self):
        """..."""
        return self.get_rect().topleft

    def set_rect(self, rect):
        """Set the position and size of the sprite from a Rect.

        Args:
            rect: a Rect from which position and size will be taken.
        """
        if rect is None:
            return
        self.position = rect.topleft
        # TODO implement sprite resizing on sdl2.ext.sprite
        # self.size = rect.size


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
                frame_rect = sprites.frame_rect or None
                if rcopy(self.sdlrenderer, sprites.texture, frame_rect, r,
                         sprites.angle, sprites.center, sprites.flip) == -1:
                    raise sdl2.ext.SDLError()
        # To avoid flickering present must be called only once, by the
        # manager
        # sdl2.render.SDL_RenderPresent(self.sdlrenderer)


class FeedbackEntry(namedtuple.abc):
    """A specific feedback entry for EventFeedback.

    Args:
        status (bool): Status of the event handling.
        entity (str): name of the entity providing this feedback.
        data (any type): data to be sent back up with the feeback. Should be
        used when various states are possible when the event is handled.
    """

    _fields = "status entity data"

    def __str__(self):
        """..."""
        return ('{0.__class__.__name__}'
                '(status={0.status},'
                ' entity={0.entity.__class__.__name__}),'
                ' data={0.data})'.format(self))


class EventFeedback(object):
    """A structured feedback sent by entities when events are caught.

    Events are passed down from the Manager to scenes, layers and it child
    entities.
    When a feeback is sent by a child of nth depth on the entities recursion,
    raising it all the way back to the Manager prevents the recursion from
    keep going without need.
    """

    def __init__(self):
        """Initialization."""
        self.feebacks = []

    def register(self, status, entity, data=None):
        """Register the event handling done by the entity.

        Args:
            status (bool): Status of the event handling.
            entity (entity instance): entity providing this feedback (example
            below).
            data (str or any type): data to be sent back up with the feeback.
            Should be used when various states are possible and knowledge of
            it should be passed up.

        Example:
            def on_key_press(self, event, mod):
                # the input is handled, something is done sucessfully
                feedback = EventFeedback()
                feedback.register(status=True, entity=self)
                return feedback
        """
        self.feedbacks.append(
            FeedbackEntry(status=status, entity=entity.__class__, data=data))

    @property
    def handled(self):
        """..."""
        return any(fb.status for fb in self.feebacks)

    def __getstate__(self):
        """..."""
        return None

if __name__ == '__main__':
    Manager()
