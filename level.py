"""Game and graphics logic, mostly."""
import pygame

from game import BaseScene

from game_types import Position
import main_menu

import level_input
import level_session_mgr
import sprite
import resources

from constants import GAME_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLS, \
    SCREEN_ROWS, TILE_W, TILE_H


class LevelScene(BaseScene):
    """The standard play scene for the game."""

    def __init__(self, game, new=True, character=None, mode='default'):
        """..."""
        self.game = game
        self.create_char = character
        self.mode = mode

        self.alive = False

        self.offset = Position((0, 0))
        self.scrolling = True
        self.game_state = 'loading'
        self.gfx.msg_log.clear()
        self.ignore_regular_update = True

        if new:
            level_session_mgr.new_game(self)
        else:
            level_session_mgr.load_game(self)

        self.alive = True

        if new:
            self.gfx.msg_log.add(
                (
                    'Welcome stranger! '
                    'Prepare to perish in the Tombs of the Ancient Kings.'),
                GAME_COLORS["purple"]
            )
        else:
            self.gfx.msg_log.add(
                ('Welcome back stranger! '
                 'This time you WILL perish in the Tombs of the Ancient'
                 ' Kings!'),
                GAME_COLORS["purple"]
            )
        self.gfx.msg_log.add(
            ('You are at level {} of the dungeon.'.format(
                self.current_level)),
            GAME_COLORS["orange"]
        )
        self.game.disable_fps()
        self.on_update()

    @property
    def gfx(self):
        """..."""
        return self.game.gfx

    @property
    def rooms(self):
        """..."""
        return self.levels[self.current_level]['groups']['rooms']

    @property
    def halls(self):
        """..."""
        return self.levels[self.current_level]['groups']['halls']

    @property
    def width(self):
        """..."""
        return self.levels[self.current_level]['width']

    @property
    def height(self):
        """..."""
        return self.levels[self.current_level]['height']

    @property
    def max_x(self):
        """..."""
        return max(SCREEN_COLS, self.width)

    @property
    def max_y(self):
        """..."""
        return max(SCREEN_ROWS, self.height)

    def rem_obj(self, obj, _type, pos):
        """..."""
        level_dict = self.levels[self.current_level]
        if obj in level_dict['grid'][pos][_type]:
            level_dict['grid'][pos][_type].remove(obj)
        if obj in level_dict['groups'][_type]:
            level_dict['groups'][_type].remove(obj)

    def add_obj(self, obj, _type, pos):
        """..."""
        level_dict = self.levels[self.current_level]
        if obj not in level_dict['grid'][pos][_type]:
            level_dict['grid'][pos][_type].append(obj)
        if obj not in level_dict['groups'][_type]:
            level_dict['groups'][_type].append(obj)

    def get_obj(self, _type, pos):
        """..."""
        grid = self.levels[self.current_level]['grid']

        if _type == "feature":
            return grid[pos][_type]

        for obj in grid[pos][_type]:
            return obj

        return None

    def get_all_at_pos(
            self, pos, _types=["creatures", "objects", "feature"]
    ):
        """..."""
        grid = self.levels[self.current_level]['grid']

        objects = []

        for _type in _types:
            if _type == "feature":
                objects.append(grid[pos][_type])

            for obj in grid[pos][_type]:
                objects.append(obj)

        return objects

    def get_nearest_obj(
        self, _type, pos, max_range=None, visible_only=True, val_callback=None
    ):
        """..."""
        grid = self.levels[self.current_level]['grid']
        target = None
        target_dist = None
        if visible_only:
            for y in range(SCREEN_ROWS):
                for x in range(SCREEN_COLS):
                    for obj in grid[x, y][_type]:
                        if not grid[x, y]['feature'].visible:
                            continue

                        if val_callback and not val_callback(obj):
                            continue

                        distance = self.map_mgr.distance(pos, (x, y))
                        if max_range and distance > max_range:
                            continue
                        elif target is None:
                            target = obj
                        else:
                            if distance < target_dist:
                                target = obj
        return target

    def validate_pos(self, pos):
        """Assure that the *relative* position is valid."""
        x, y = pos
        x = max(0, x)
        x = min(self.max_x - SCREEN_COLS, x)

        y = max(0, y)
        y = min(self.max_y - SCREEN_ROWS, y)
        print("pos val")

        return Position((x, y))

    def set_offset(self, object):
        """Center the view around an object.

        Adjustments are made to better show map edges.
        """
        x = object.x - SCREEN_COLS // 2
        y = object.y - SCREEN_ROWS // 2

        x = min(self.max_x - SCREEN_COLS, x)
        x = max(1, x)

        y = min(self.max_y - SCREEN_ROWS, y)
        y = max(1, y)

        self.offset = Position((x, y))
        print("Player {}=={}, offset {}=={}, SCREEN_COLS {}, SCREEN_ROWS {}".format(self.player.pos, object.pos, self.offset, (x, y), SCREEN_COLS, SCREEN_ROWS))

    def scroll(self, rel):
        """Scroll map using relative coordinates."""
        if not self.scrolling:
            return

        x, y = [self.offset[0] + rel[0], self.offset[1] + rel[1]]

        self.offset = self.validate_pos((x, y))

    def new_turn(self):
        """..."""
        self.turn += 1
        print("Turn {}".format(self.turn))

        self.tile_fx.update()

        self.player.active = True

        level_dict = self.levels[self.current_level]
        for creature in level_dict['groups']['creatures']:
            creature.active = True

    def handle_turn(self):
        """..."""
        if self.alive:
            level_dict = self.levels[self.current_level]
            if self.game_state == 'playing':
                for creature in level_dict['groups']['creatures']:
                    if creature.ai and creature.active and creature.visible:
                        old_pos = creature.get_rect
                        creature.ai.take_turn()
                        new_pos = creature.get_rect

                        if creature.visible:

                            self.gfx.draw(
                                ord(creature.combat.name[0]),
                                (creature.x, creature.y),
                                color=creature.color)

                            pygame.display.update([old_pos, new_pos])

                    if creature is not self.player:
                        creature.active = False

                if not self.player.active:
                    self.new_turn()
        self.on_update()

    def update_pos(self, pos, scr_pos):
        """Logic for redrawing specific positions of the screen."""
        x, y = scr_pos
        grid = self.levels[self.current_level]['grid']
        tile = grid[pos]
        draw = self.gfx.draw

        if tile["feature"].visible or tile["feature"].explored:
            draw(tile["feature"].id, (x, y),
                 color=tile["feature"].color,
                 tiling_index=tile["feature"].tiling_index,
                 tile_variation=tile["feature"].tile_variation)
            fx_color = self.tile_fx.get(coord=pos)
            if fx_color:
                draw(ord(','), (x, y), color=fx_color)

            for obj in tile["objects"]:
                if isinstance(obj, sprite.DngFeature):
                    draw(obj.id, (x, y), obj.color)

            if not tile["feature"].visible:
                self.gfx.draw_fog((x, y))
            else:
                if len(tile["objects"]) > 1:
                    draw(ord("&"), (x, y), (168, 168, 0))
                else:
                    if tile["objects"]:
                        obj = tile["objects"][0]
                        draw(obj.id, (x, y), obj.color)

                for creature in tile['creatures']:
                    draw(ord(creature.combat.name[0]),
                         (x, y), color=creature.color)

    def update_tiles(self):
        """..."""
        if self.alive:
            # loop all tiles
            for y in range(SCREEN_ROWS):
                for x in range(SCREEN_COLS):
                    # draw tile
                    pos = self.offset + (x, y)
                    scr_pos = (x, y)
                    self.update_pos(pos, scr_pos)

    def update_gui(self):
        """..."""
        if self.alive:
            self.gfx.draw_hud()

            if self.game_state == 'inventory':
                self.gfx.inventory.draw()
            elif self.game_state == 'choice':
                self.gfx.choice.draw()
            elif self.game_state == 'dead':
                self.gfx.msg.draw("The End?")
        elif self.game_state == 'saving':
            self.gfx.msg.draw("Saving your game (Don't panic!)")

    def on_update(self, tiles=True, gui=True):
        """..."""
        game = self.game
        game.screen.fill((0, 0, 0))

        if tiles:
            self.update_tiles()
        if gui:
            self.update_gui()

        self.game.draw_fps()

        game.display.flip()

    def choice(self, title, items, callback):
        """..."""
        self.gfx.choice.set_list(title, items, callback)
        self.game_state = 'choice'

    def quit(self, save=True):
        """..."""
        self.alive = False
        if save:
            level_session_mgr.save_game(self)
        self.game.enable_fps()
        self.game.set_scene(scene=main_menu.MainMenu)

    def on_key_press(self, event):
        """Input is handled by level_input."""
        level_input.on_key_press(self, event)

    def on_mouse_press(self, event):
        """..."""
        level_input.on_mouse_press(self, event)

    def on_mouse_scroll(self, event):
        """..."""
        level_input.on_mouse_scroll(self, event)

    def new_level(self, level=0):
        """..."""
        level_session_mgr.new_level(self, level)

    def screenshot(self, fname=None, map_cols=None, map_rows=None):
        """..."""
        map_cols = map_cols or self.width
        map_rows = map_rows or self.height
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
    from game import Game
    from constants import LIMIT_FPS
    Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
