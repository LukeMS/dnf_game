"""..."""

import os
import sys

import sdl2

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from util import Position
from util.ext import fov
from data.constants import (FOV_RADIUS, SCR_ROWS, SCR_COLS, GAME_COLORS,
                            TILE_W, TILE_H)
from scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_main.layers import layer_map, layer_session_mgr
from scene_manager.layers import base_layers
from dnf_main.scenes import scene_title
from dnf_main.map_entities import (PCreature, NPCreature, FeatureEntity,
                                   ItemEntity, Cursor)


class SceneMap(SceneMultiLayer):
    """..."""

    def __init__(self, *, new=True, character=None, mode='RndMap2', **kwargs):
        """..."""
        super().__init__()

        self.mode = mode
        self.create_layers(character=character, new=new,
                           msg="Creating a world of treasures and dangers...")
        self.set_fov()
        self.on_update()

        self.msg_log.clear()

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
        # self.manager.disable_fps()
        # [layer.__setattr__('visible', False) for layer in self.layers]
        self.on_update()
        # print(self.tiles_on_screen())

    @property
    def cols(self):
        """..."""
        return self.width // self.tile_width

    @property
    def rows(self):
        """..."""
        return self.height // self.tile_height

    @property
    def tile_width(self):
        """..."""
        return self.manager.tile_size

    @property
    def tile_height(self):
        """..."""
        return self.manager.tile_size

    def tiles_on_screen(self):
        """..."""
        offset = self.level_layer.set_offset(self.player)
        cols, rows = self.current_level.cols, self.current_level.rows
        tiles = [(x, y)
                 for x in range(offset.x, min(offset.x + SCR_COLS - 1,
                                              cols - 1))
                 for y in range(offset.y, min(offset.y + SCR_ROWS - 1,
                                              rows - 1))]
        return tiles

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

    def create_layers(self, character, new, msg):
        """..."""
        self.msg = base_layers.Msg(parent=self, text=msg)
        self.state = 'loading'
        self.layers = [self.msg]
        self.on_update()

        self.session_mgr = layer_session_mgr.SessionMgr(
            parent=self, character=character, new=new)

        self.level_layer = layer_map.LayerMap(parent=self)

        self.hp_bar = base_layers.Bar(parent=self, name="Health")
        self.msg_log = base_layers.MsgLog(parent=self)
        self.fps_time_label = base_layers.Hud(parent=self)
        self.inventory = base_layers.Inventory(parent=self)
        self.choice = base_layers.Choice(parent=self)

        self.layers = [self.level_layer, self.hp_bar, self.msg_log,
                       self.fps_time_label, self.inventory, self.choice,
                       self.msg]

    @property
    def state(self):
        """..."""
        return self._state

    @state.setter
    def state(self, value):
        if value == "dead":
            self.msg.text = "The End?"
        elif value == "loading":
            self.msg.text = "Creating a world of treasures and dangers..."
        elif value == "saving":
            self.msg.text = ("Fear not, for your deeds shall not be"
                             "forgotten...")
        self._state = value

    @property
    def ignore_regular_update(self):
        """..."""
        """
        if self.state in ["inventory", "loading", "dead"]:
            return False
        """
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

    def rem_obj(self, obj, pos):
        """..."""
        _type = obj.__class__
        current_level = self.current_level
        if _type in (PCreature, NPCreature):
            current_level[pos].remove_creatures(obj)
        elif _type in (FeatureEntity, ItemEntity):
            current_level[pos].remove_objects(obj)
        else:
            raise TypeError("rem_obj(invalid _type):{}".format(str(obj)))

    def add_obj(self, obj, pos):
        """..."""
        _type = obj.__class__
        current_level = self.current_level
        if _type in (PCreature, NPCreature):
            current_level[pos].add_creatures(obj)
        elif _type in (FeatureEntity, ItemEntity):
            current_level[pos].add_objects(obj)
        elif _type == Cursor:
            pass
        else:
            raise TypeError("add_obj(invalid _type):{}".format(str(obj)))

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
                    creature.ai.take_turn()

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
        # self.manager.enable_fps()
        self.manager.set_scene(scene=scene_title.SceneTitle)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym
        if self.state == 'dead' and sym in [
            sdl2.SDLK_ESCAPE, sdl2.SDLK_RETURN, sdl2.SDLK_SPACE
        ]:
            self.quit(save=False)
        elif self.state == 'playing':
            if sym in {sdl2.SDLK_i, sdl2.SDLK_d}:
                if sym == sdl2.SDLK_i:
                    self.inventory.set_inventory(self.player, mode="use")
                elif sym == sdl2.SDLK_d:
                    self.inventory.set_inventory(self.player, mode="drop")
                self.state = 'inventory'
                self.on_update()
                return True
        print("scene passing on_key_press")
        [layer.on_key_press(event, mod)
         for layer in self.layers if layer.active]

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        [layer.on_key_release(event, mod)
         for layer in self.layers if layer.active]

    def on_mouse_drag(self, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged."""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        pass

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        pos = x, y
        rel_pos = self.cursor_rel_pos(pos=pos)

        if self.player.active and event.button == "RIGHT":  # right button
            target = self.cursor.move(pos, rel_pos)

            self.inventory.set_inventory(
                holder=self.player,
                target=target)
            self.state = 'inventory'
            self.on_update()
            return True
        [layer.on_mouse_press(event, x, y, button, double)
         for layer in self.layers if layer.active]

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        [layer.on_mouse_scroll(event, offset_x, offset_y)
         for layer in self.layers if layer.active]

    def on_update(self):
        """..."""
        def update_layers():
            [layer.on_update() for layer in self.layers if layer.visible]

        if self.ignore_regular_update:
            self.manager.renderer.clear()
            update_layers()
            self.manager.present()
        else:
            update_layers()

if __name__ == '__main__':
    from scene_manager import Manager
    m = Manager(scene=SceneMap).execute()
