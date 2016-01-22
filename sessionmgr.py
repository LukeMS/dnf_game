import os

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS
import sprite
import gamemap
import tile_fx


def clear_savedir():

    if os.path.isdir('save'):
        for root, path, files in os.walk('save'):
            for f in files:
                os.remove(os.path.join(root, f))
        os.removedirs('save')


def ensure_savedir():
    if not os.path.exists('save'):
        os.makedirs('save')


def new_game(self):
    clear_savedir()
    self.turn = 0

    self.levels = {}

    self.max_y = max(SCREEN_ROWS, MAP_ROWS)
    self.max_x = max(SCREEN_COLS, MAP_COLS)

    self.new_level()

    self.area_fx = tile_fx.AreaFx()

    self.cursor = sprite.Cursor(scene=self)


def new_level(self, level=0):
    self.game_state = 'loading'

    if level in self.levels:
        # going back to a level

        # clean up
        self.levels[self.current_level]['player_pos'] = self.player.pos
        self.objects.remove(self.player)

        # set the level number, properties will follow it
        self.current_level = level
        #

        # recover player pos - should set it to stairs?
        self.player.pos = self.levels[level]['player_pos']
        self.objects.add(self.player)
        self.player.group = self.objects

    else:
        import rnd_gen
        if len(self.levels) > 0:
            self.levels[self.current_level]['player_pos'] = self.player.pos
            self.objects.remove(self.player)

        # set the level number, properties will follow it
        self.current_level = level
        self.levels[level] = {}
        #

        # going to a new level - or the first one
        self.levels[level]['objects'] = sprite.Group()
        self.levels[level]['remains'] = sprite.Group()

        grid, rooms, halls = rnd_gen.Map().make_map(
            MAP_COLS, MAP_ROWS)

        self.levels[level]['grid'] = grid
        self.levels[level]['rooms'] = rooms
        self.levels[level]['halls'] = halls

        map_mgr = getattr(self, "map_mgr", None)
        if map_mgr is None:
            self.map_mgr = gamemap.Map(scene=self)

        self.map_mgr.place_objects()
        self.objects.add(self.player)

    self.map_mgr.set_fov()

    self.tile_fx = tile_fx.TileFx()

    self.player.active = True
    self.game_state = 'playing'


def load_game(self):
    import zshelve
    import os
    with zshelve.open(os.path.join('save', 'savegame'), 'r') as shelf_file:
        self.levels = shelf_file['levels']

        for att, value in shelf_file['scene'].items():
            setattr(self, att, value)

        self.player = shelf_file['player']
        self.player.pos = self.levels[self.current_level]['player_pos']

        self.objects.add(self.player)

        self.map_mgr = gamemap.Map(scene=self)

        for group in [self.objects, self.remains]:
            for obj in group:
                obj.scene = self
                obj.grid = self.grid
                obj.group = group

        self.map_mgr.set_fov()

        self.tile_fx = tile_fx.TileFx()

        self.area_fx = tile_fx.AreaFx()

        self.cursor = sprite.Cursor(scene=self)

        self.game_state = 'playing'


def save_game(self):
    self.game_state = 'saving'
    ensure_savedir()
    import zshelve
    import os

    with zshelve.open(os.path.join('save', 'savegame'), 'n') as shelf_file:
        self.objects.remove(self.player)
        self.levels[self.current_level]['player_pos'] = self.player.pos
        shelf_file['player'] = self.player

        scene = {}
        for att in ['current_level', 'turn', "max_y", "max_x", "offset"]:
            scene[att] = getattr(self, att)
        shelf_file['scene'] = scene

        shelf_file['levels'] = self.levels
