"""Game and graphics logic, mostly."""

import sdl2

from dnf_game.data.constants import SCR_COLS, SCR_ROWS
from dnf_game.scene_manager.layers import base_layers
from dnf_game.util import debug_status, Position
from dnf_game.util.ext.rect import Rect


class LayerMap(base_layers.Layer):
    """The standard play scene for the game."""

    def __init__(self, *, parent):
        """..."""
        super().__init__(parent=parent)
        self.offset = Position((0, 0))
        self.scrolling = True
        self._fog_cache = None

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing", "inventory", "dead"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing", "dead"]:
            return True
        else:
            return False

    @property
    def player(self):
        """..."""
        return self.parent.player

    @property
    def cols(self):
        """..."""
        return self.parent.cols

    @property
    def rows(self):
        """..."""
        return self.parent.rows

    def set_offset(self, obj=None):
        """Center the view around an object.

        Adjustments are made to better show map edges.
        """
        obj = obj if obj else self.player
        if self.cols < SCR_COLS:
            x = obj.x // 2 - (SCR_COLS - self.cols) // 2
        else:
            x = obj.x - SCR_COLS // 2
            x = min(self.parent.max_x - SCR_COLS, x)
            x = max(1, x)

        if self.rows < SCR_ROWS:
            y = obj.y // 2 - (SCR_ROWS - self.rows) // 2
        else:
            y = obj.y - SCR_ROWS // 2
            y = min(self.parent.max_y - SCR_ROWS, y)
            y = max(1, y)

        self.offset = Position((x, y))
        return self.offset
        print(
            ("Player {}=={}, offset {}=={}"
             ", SCR_COLS {}, SCR_ROWS {}").format(
                self.player.pos, obj.pos, self.offset, (x, y),
                SCR_COLS, SCR_ROWS))

    def scroll(self, rel):
        """Scroll map using relative coordinates."""
        if not self.scrolling:
            return

        x, y = [self.offset[0] + rel[0], self.offset[1] + rel[1]]

        self.offset = self.validate_pos((x, y))

    @property
    def hoard(self):
        """..."""
        if self._hoard is None:
            self._hoard = self.parent.manager.factory.from_tileset(
                _id=ord("&"),
                color=(168, 168, 0, 255))
        return self._hoard

    def fx_cache(self, color):
        """..."""
        if color not in self.fx_cache:
            self.fx_cache[color] = self.parent.manager.factory.from_tileset(
                _id=ord(','),
                color=color)
        return self.fx_cache[color]

    @property
    def fog(self):
        """..."""
        if not self._fog_cache:
            self._fog_cache = self.parent.manager.factory.from_color(
                color=(0, 63, 7, 191),
                rect=Rect((0, 0),
                          (self.parent.tile_width, self.parent.tile_height)))
        return self._fog_cache

    def update_pos(self, pos, scr_pos):
        """Logic for redrawing specific positions of the screen."""
        def draw_feature():
            try:
                render(sprites=feature.sprite, x=x, y=y)
            except AttributeError as e:
                from dnf_game.util import describe_error
                describe_error(e,
                               feature.__class__.__name__,
                               feature.__dict__)
                raise

        def draw_objects():
            objects = tile.objects
            if len(objects) > 1:
                render(sprites=self.hoard, x=x, y=y)
            else:
                [render(sprites=obj.sprite, x=x, y=y)
                 for obj in objects if obj]

        def draw_creatures():
            creatures = tile.creatures
            [render(sprites=creature.sprite, x=x, y=y)
             for creature in creatures if creature]

        def draw_tile_fx():
            fx_color = tile_fx.get(coord=pos)
            if fx_color:
                render(sprites=self.fx_cache(fx_color), x=x, y=y)

        def draw_fog():
            fog = self.fog
            render(sprites=fog, x=x, y=y)

        col, row = scr_pos
        x = col * self.parent.tile_width
        y = row * self.parent.tile_height
        parent = self.parent
        tile = parent.current_level[pos]
        feature = tile.feature
        tile_fx = parent.tile_fx
        render = parent.manager.spriterenderer.render

        if feature.explored:
            draw_feature()
            if feature.visible:
                draw_objects()
                draw_creatures()
                draw_tile_fx()
            else:
                draw_fog()

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym

        if self.player.active:
            if sym in [sdl2.SDLK_KP_7]:
                self.player.action(-1, -1)
            elif sym in [sdl2.SDLK_UP, sdl2.SDLK_KP_8]:
                self.player.action(0, -1)
            elif sym in [sdl2.SDLK_KP_9]:
                self.player.action(1, -1)
            elif sym in [sdl2.SDLK_RIGHT, sdl2.SDLK_KP_6]:
                self.player.action(1, 0)
            elif sym in [sdl2.SDLK_KP_3]:
                self.player.action(1, 1)
            elif sym in [sdl2.SDLK_DOWN, sdl2.SDLK_KP_2]:
                self.player.action(0, 1)
            elif sym in [sdl2.SDLK_KP_1]:
                self.player.action(-1, 1)
            elif sym in [sdl2.SDLK_LEFT, sdl2.SDLK_KP_4]:
                self.player.action(-1, 0)
            elif sym in [sdl2.SDLK_SPACE, sdl2.SDLK_KP_5]:
                self.player.action()  # skip a turn

            elif sym == sdl2.SDLK_g:
                if not self.player.action(action='get'):
                    pos = self.player.pos
                    scr_pos = self.player.pos - self.offset
                    self.update_pos(pos, scr_pos)
                    self.parent.on_update()
                    return

            elif sym == sdl2.SDLK_u:
                if not self.player.action(action='use'):
                    pos = self.player.pos
                    scr_pos = self.player.pos - self.offset
                    self.update_pos(pos, scr_pos)
                    return

            elif sym == sdl2.SDLK_k:
                self.player.combat.receive_dmg(999999, "user")
                # TODO: fix, causing crashing error
            elif sym == sdl2.SDLK_e:
                self.player.gain_xp(23000)
                # TODO: fix, causing crashing error
            elif sym == sdl2.SDLK_s:
                # TODO: use in-game ui
                debug_status.view(creature=self.player.combat)
                return
            elif sym == sdl2.SDLK_z:
                # print("debug_status.input called")
                debug_status.input(game=self.game)

        else:
            print("player inactive")
        self.parent.handle_turn()

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_ESCAPE:
            self.parent.quit()

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        pos = x, y
        rel_pos = self.parent.cursor_rel_pos(pos=pos)

        if event.button == "LEFT":  # left button
            target = self.parent.cursor.move(pos, rel_pos)
            debug = getattr(target, 'combat', None)
            debug = target.combat if hasattr(target, 'combat') \
                else self.parent.current_level[rel_pos]
            debug_status.view(creature=debug)
            return

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Handle mouse scroll input for the level."""
        if self.parent.state == 'playing':
            keys = self.manager.key_mods

            ctrl = keys[sdl2.SDLK_LCTRL]

            if ctrl:
                offset = (offset_y, 0)
            else:
                offset = (0, offset_y)

            self.scroll(offset)
            self.parent.on_update()

    def on_update(self):
        """..."""
        update_pos = self.update_pos
        offset = self.offset
        screen_tiles = self.parent.tiles_on_screen()
        [update_pos((x, y), (x - offset.x, y - offset.y))
         for (x, y) in screen_tiles]

if __name__ == '__main__':
    pass
