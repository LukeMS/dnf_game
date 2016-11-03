"""Game and graphics logic, mostly."""
import pygame

from manager.windows import base_windows

from game_types import Position


from common import debug_status

import resources

from constants import SCREEN_COLS, SCREEN_ROWS, TILE_W, TILE_H


class LayerMap(base_windows.Layer):
    """The standard play scene for the game."""

    def __init__(self, *, parent):
        """..."""
        super().__init__(parent=parent)
        self.offset = Position((0, 0))
        self.scrolling = True

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

    def on_update(self):
        """..."""
        # print("level_layer.on_update called")
        # loop all tiles
        for (x, y) in self.parent.tiles_on_screen():
            # draw tile
            # print()
            scr_pos = x - self.offset.x, y - self.offset.y
            pos = (x, y)
            self.update_pos(pos, scr_pos)

    def on_key_press(self, event):
        """Handle key presses input for the level."""
        key = event.key
        # print("layer_map.on_key_press", key)
        if key == pygame.K_ESCAPE:
            self.quit()

        if self.player.active:
            if key in [pygame.K_KP7]:
                self.player.action(-1, -1)
            elif key in [pygame.K_UP, pygame.K_KP8]:
                self.player.action(0, -1)
            elif key in [pygame.K_KP9]:
                self.player.action(1, -1)
            elif key in [pygame.K_RIGHT, pygame.K_KP6]:
                self.player.action(1, 0)
            elif key in [pygame.K_KP3]:
                self.player.action(1, 1)
            elif key in [pygame.K_DOWN, pygame.K_KP2]:
                self.player.action(0, 1)
            elif key in [pygame.K_KP1]:
                self.player.action(-1, 1)
            elif key in [pygame.K_LEFT, pygame.K_KP4]:
                self.player.action(-1, 0)
            elif key in [pygame.K_SPACE, pygame.K_KP5]:
                self.player.action()  # skip a turn

            elif key == pygame.K_g:
                if not self.player.action(action='get'):
                    pos = self.player.pos
                    scr_pos = self.player.pos - self.offset
                    self.update_pos(pos, scr_pos)
                    self.parent.on_update()
                    return

            elif key == pygame.K_u:
                if not self.player.action(action='use'):
                    pos = self.player.pos
                    scr_pos = self.player.pos - self.offset
                    self.update_pos(pos, scr_pos)
                    return

            elif key == pygame.K_k:
                self.player.combat.receive_dmg(999999, "user")
                # TODO: fix, causing crashing error
            elif key == pygame.K_e:
                self.player.gain_xp(23000)
                # TODO: fix, causing crashing error
            elif key == pygame.K_s:
                # TODO: use in-game ui
                debug_status.view(creature=self.player.combat)
                return
            elif key == pygame.K_z:
                # print("debug_status.input called")
                debug_status.input(game=self.game)

        self.parent.handle_turn()

    def on_mouse_press(self, event):
        """Handle mouse press input for the level."""
        pos = event.pos
        rel_pos = self.parent.cursor_rel_pos(pos=pos)

        if event.button == 1:  # left button
            target = self.parent.cursor.move(pos, rel_pos)
            debug = getattr(target, 'combat', None)
            debug = target.combat if hasattr(target, 'combat') \
                else self.parent.current_level[rel_pos]
            debug_status.view(creature=debug)
            return

        self.handle_turn()

    def on_mouse_scroll(self, event):
        """Handle mouse scroll input for the level."""
        if self.game_state == 'playing':
            keys = pygame.key.get_pressed()

            ctrl = keys[pygame.K_LCTRL]

            if event.button == 4:
                if ctrl:
                    self.scroll((-1, 0))
                else:
                    self.scroll((0, -1))
            elif event.button == 5:
                if ctrl:
                    self.scroll((1, 0))
                else:
                    self.scroll((0, 1))
        self.parent.on_update()

    def set_offset(self, obj=None):
        """Center the view around an object.

        Adjustments are made to better show map edges.
        """
        obj = obj if obj else self.player
        if self.cols < SCREEN_COLS:
            x = obj.x // 2 - (SCREEN_COLS - self.cols) // 2
        else:
            x = obj.x - SCREEN_COLS // 2
            x = min(self.parent.max_x - SCREEN_COLS, x)
            x = max(1, x)

        if self.rows < SCREEN_ROWS:
            y = obj.y // 2 - (SCREEN_ROWS - self.rows) // 2
        else:
            y = obj.y - SCREEN_ROWS // 2
            y = min(self.parent.max_y - SCREEN_ROWS, y)
            y = max(1, y)

        self.offset = Position((x, y))
        return self.offset
        print(
            ("Player {}=={}, offset {}=={}"
             ", SCREEN_COLS {}, SCREEN_ROWS {}").format(
                self.player.pos, obj.pos, self.offset, (x, y),
                SCREEN_COLS, SCREEN_ROWS))

    def scroll(self, rel):
        """Scroll map using relative coordinates."""
        if not self.scrolling:
            return

        x, y = [self.offset[0] + rel[0], self.offset[1] + rel[1]]

        self.offset = self.validate_pos((x, y))

    def update_pos(self, pos, scr_pos):
        """Logic for redrawing specific positions of the screen."""
        def draw_feature():
            draw(tile.feature.id, (x, y),
                 color=tile.feature.color,
                 tiling_index=tile.feature.tiling_index,
                 tile_variation=tile.feature.tile_variation)

        def draw_objects():
            objects = tile.objects
            if len(objects) > 1:
                draw(ord("&"), (x, y), (168, 168, 0))
            else:
                [draw(obj.id, (x, y), obj.color) for obj in objects if obj]

        def draw_creatures():
            [draw(ord(creature.combat.name[0]), (x, y), creature.color)
             for creature in tile.creatures if creature]

        def draw_tile_fx():
            fx_color = tile_fx.get(coord=pos)
            if fx_color:
                draw(ord(','), (x, y), color=fx_color)

        x, y = scr_pos
        # try:
        tile = self.parent.current_level[pos]
        tile_fx = self.parent.tile_fx
        # except KeyError:
        # return
        draw = self.parent.draw_tile

        if tile.feature.explored:
            draw_feature()
            if tile.feature.visible:
                draw_objects()
                draw_creatures()
                draw_tile_fx()
            else:
                self.parent.draw_fog((x, y))

    def screenshot(self, fname=None, map_cols=None, map_rows=None):
        """..."""
        map_cols = map_cols
        map_rows = map_rows
        fname = fname or ("{}-{}.png".format(__file__, self.mode))

        canvas = pygame.Surface((TILE_W * map_cols, TILE_H * map_rows))

        grid = self.levels[self.current_level]['grid']

        for x in range(0, map_cols):
            for y in range(0, map_rows):
                tile = grid[(x, y)]
                id = tile.id
                color = tile.color
                tiling_index = tile.tiling_index
                tile_variation = tile.tile_variation

                dest = pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

                src, surface = resources.Tilesets.get_tile(
                    id, color, tiling_index, tile_variation)

                canvas.blit(
                    source=surface, dest=dest, area=src)

        pygame.image.save(canvas, fname)

if __name__ == '__main__':
    pass
