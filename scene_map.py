"""..."""
import pygame

import fov
from constants import (FOV_RADIUS, SCREEN_ROWS, SCREEN_COLS, GAME_COLORS,
                       TILE_W, TILE_H)
from game_types import Position
from manager.scenes import scene_map_base
import layer_map
import layer_session_mgr
import scene_title


class SceneMap(scene_map_base.SceneMapBase):
    """..."""

    def __init__(self, *, new=True, character=None, mode='pit'):
        """..."""
        super().__init__()

        self.state = 'loading'
        self.create_layers(character)
        self.msg.text = "Creating a world of treasures and dangers..."
        self.on_update()

        self.mode = mode

        self.msg_log.clear()

        if new:
            self.session_mgr.new_game()
        else:
            self.session_mgr.load_game()

        if new:
            self.msg_log.add(
                (
                    'Welcome stranger! '
                    'Prepare to perish in the Tombs of the Ancient Kings.'),
                GAME_COLORS["purple"]
            )
        else:
            self.msg_log.add(
                ('Welcome back stranger! '
                 'This time you WILL perish in the Tombs of the Ancient'
                 ' Kings!'),
                GAME_COLORS["purple"]
            )
        self.msg_log.add(
            ('You are at level {} of the dungeon.'.format(
                self.current_level.header.level)),
            GAME_COLORS["orange"]
        )
        self.game.disable_fps()
        # [layer.__setattr__('visible', False) for layer in self.layers]
        self.on_update()
        # print(self.tiles_on_screen())

    def tiles_on_screen(self):
        """..."""
        offset = self.level_layer.set_offset(self.player)
        cols, rows = self.current_level.cols, self.current_level.rows
        tiles = [(x, y)
                 for x in range(offset.x, min(offset.x + SCREEN_COLS - 1,
                                              cols - 1))
                 for y in range(offset.y, min(offset.y + SCREEN_ROWS - 1,
                                              rows - 1))]
        return tiles

    def on_update(self):
        """..."""
        # print("scene_map.on_update")
        self.screen.fill((0, 0, 0))
        [layer.on_update() for layer in self.layers if layer.visible]
        pygame.display.flip()

    def on_mouse_press(self, event):
        """..."""
        pos = event.pos
        rel_pos = self.cursor_rel_pos(pos=pos)

        if self.player.active and event.button == 3:  # right button
            target = self.cursor.move(pos, rel_pos)

            self.inventory.set_inventory(
                holder=self.player,
                target=target)
            self.state = 'inventory'
            self.on_update()
            return True
        super().on_mouse_press(event)

    def on_key_press(self, event):
        """..."""
        key = event.key
        if self.state == 'dead' and key in [
            pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE
        ]:
            self.quit(save=False)
        elif self.state == 'playing':
            if key in [pygame.K_i, pygame.K_d]:
                if key == pygame.K_i:
                    self.inventory.set_inventory(self.player, mode="use")
                elif event.key == pygame.K_d:
                    self.inventory.set_inventory(self.player, mode="drop")
                self.state = 'inventory'
                self.on_update()
                return True
        super().on_key_press(event)

    def cursor_pos(self):
        """Get the absolute screen position of the cursor."""
        return pygame.mouse.get_pos()

    def cursor_rel_pos(self, pos=None):
        """Get the relative position of the cursor on the grid."""
        if pos is None:
            pos = pygame.mouse.get_pos()
        rel_pos = (
            (pos[0] // TILE_W) + self.level_layer.offset[0],
            (pos[1] // TILE_H) + self.level_layer.offset[1])
        return rel_pos

    def create_layers(self, character):
        """..."""
        self.session_mgr = layer_session_mgr.SessionMgr(self, character)
        self.level_layer = layer_map.LayerMap(parent=self)
        self.insert_layer(self.level_layer)
        super().create_layers()
        self.on_update()

    @property
    def state(self):
        """..."""
        return self._state

    @state.setter
    def state(self, value):
        if value == "dead":
            self.msg.text = "The End?"
        elif value == "saving":
            self.msg.text = "Saving your game (Don't panic!)"
        self._state = value

    @property
    def ignore_regular_update(self):
        """..."""
        if self.state in ["inventory", "loading", "dead"]:
            return False
        return True

    @property
    def set_offset(self):
        """..."""
        return self.level_layer.set_offset

    @property
    def current_level(self):
        """..."""
        return self.maps.current

    @property
    def rooms(self):
        """..."""
        return self.current_level.rooms

    @property
    def halls(self):
        """..."""
        return self.current_level.halls

    @property
    def map_width(self):
        """..."""
        return self.current_level.cols

    @property
    def map_height(self):
        """..."""
        return self.current_level.rows

    @property
    def max_x(self):
        """..."""
        return max(self.cols, self.width)

    @property
    def max_y(self):
        """..."""
        return max(self.rows, self.height)

    def set_fov(self):
        """..."""
        def func_visible(x, y):
            self.current_level[x, y].feature.visible = True
            # if self.distance(self.player.pos, (x, y)) <= EXPLORE_RADIUS:
            self.current_level[x, y].feature.explored = True

        cols, rows = self.current_level.cols, self.current_level.rows

        # print("cols:", cols, ", rows:", rows)
        [self.current_level[x, y].feature.__setattr__("visible", False)
         for (x, y) in self.tiles_on_screen()]

        fov.fieldOfView(self.player.x, self.player.y,
                        cols, rows, FOV_RADIUS,
                        func_visible, self.current_level.blocks_sight)

    def rem_obj(self, obj, _type, pos):
        """..."""
        current_level = self.current_level
        if _type == "creatures":
            current_level[pos].remove_creatures(obj)
        elif _type == "objects":
            current_level[pos].remove_objects(obj)
        else:
            type_error = TypeError("rem_obj(invalid _type):{}".format(
                str(obj)))
            raise type_error

    def add_obj(self, obj, _type, pos):
        """..."""
        current_level = self.current_level
        if _type == "creatures":
            current_level[pos].add_creatures(obj)
        elif _type == "objects":
            current_level[pos].add_objects(obj)
        else:
            type_error = TypeError("add_obj(invalid _type):{}".format(
                str(obj)))
            raise type_error

    def get_obj(self, _type, pos):
        """..."""
        tile = self.current_level[pos]

        if _type == "feature":
            return tile.feature
        elif _type == "creatures":
            return tile.creatures
        elif _type == "objects":
            return tile.objects

    def get_all_at_pos(
            self, pos, _types=None
    ):
        """..."""
        _types = _types if _types else ["creatures", "objects", "feature"]
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
        current_level = self.current_level
        target = None
        target_dist = None
        if visible_only:
            for y in range(self.rows):
                for x in range(self.cols):
                    if not current_level[x, y].feature.visible:
                        continue
                    for obj in current_level[x, y].get_by_type(_type):
                        if val_callback and not val_callback(obj):
                            continue
                        distance = current_level.distance(pos, (x, y))
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
        x = min(self.max_x - self.cols, x)

        y = max(0, y)
        y = min(self.max_y - self.rows, y)
        # print("pos val")

        return Position((x, y))

    def new_turn(self):
        """..."""
        self.turn += 1
        print("Turn {}".format(self.turn))

        self.tile_fx.update()

        self.player.active = True

        for creature in self.current_level.creatures:
            creature.active = True

    def handle_turn(self):
        """..."""
        current_level = self.current_level
        if self.state == 'playing':
            for creature in current_level.creatures:
                if creature.ai and creature.active and creature.visible:
                    old_pos = creature.get_rect
                    creature.ai.take_turn()
                    new_pos = creature.get_rect

                    if creature.visible:

                        self.draw_tile(
                            ord(creature.combat.name[0]),
                            (creature.x, creature.y),
                            color=creature.color)

                        pygame.display.update([old_pos, new_pos])

                if creature is not self.player:
                    creature.active = False

            if not self.player.active:
                self.new_turn()
        self.on_update()

    def new_level(self, level=0):
        """..."""
        self.session_mgr.new_level(level)

    def quit(self, save=True):
        """..."""
        if save:
            self.session_mgr.save_game()
        self.game.enable_fps()
        self.game.set_scene(scene=scene_title.MainMenu)

if __name__ == '__main__':
    from manager import Game
    Game(scene=SceneMap)
