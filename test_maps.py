"""..."""

import os
import sys

import pygame

import level
import gamemap
import sprite
import resources
from constants import MAP_COLS, MAP_ROWS, TILE_W, TILE_H

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'old_src'))

from pygametiles.worm import worm


class MapMgrDummy(gamemap.MapMgr):
    """..."""

    def set_fov(self):
        """..."""
        self.__dict__.setdefault('all_clear', False)
        if not self.all_clear:
            for pos in self.grid.keys():
                self.grid[pos].visible = True

            self.__dict__['all_clear'] = True

    def place_objects(self):
        """..."""
        self.rooms[0]

        x, y = self.rooms[0].random_point(_map=self.grid)
        player = getattr(self, 'player', None)
        if player:
            self._scene.rem_obj(self.player, 'creatures',
                                self.player.pos)

            self.player.pos = (x, y)

            self._scene.add_obj(self.player, 'creatures',
                                self.player.pos)
        else:
            self.player = sprite.Player(
                scene=self._scene, x=x, y=y)


class PlayerDummy(sprite.Player):
    """..."""

    def action(self, dx=0, dy=0, action='std', key=None):
        """..."""
        pos = self.pos + (dx * 2, dy * 2)
        pos = self.scene.validate_pos(pos)
        self.pos = pos
        self.scene.set_offset(self)
        self.scene.on_update()


class MapTest(level.LevelScene):
    """..."""

    def __init__(self, game):
        """..."""
        gamemap.MapMgr.place_objects = MapMgrDummy.place_objects
        gamemap.MapMgr.set_fov = MapMgrDummy.set_fov
        sprite.Player.action = PlayerDummy.action

        super().__init__(game, new=True)

        grid = self.levels[self.current_level]['grid']

        # self.screenshot('map-default.png')

        m = worm.main(map_width=MAP_COLS, map_lenght=MAP_ROWS)
        print("worm:{}={}x, {}={}y?".format(
            len(m[0]), MAP_COLS,
            len(m), MAP_ROWS))
        for j, y in enumerate(m):
            for i, x in enumerate(y):
                if x == 1:
                    feature = ord("#")
                else:
                    feature = ord(".")

                grid[(i, j)]["feature"].id = feature
        self.map_mgr.set_tiling_index()

        self.screenshot('map-worm.png')

        exit()


    def _on_key_press(self, event):
        """..."""
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def screenshot(self, fname):
        """..."""
        grid = self.levels[self.current_level]['grid']

        canvas = pygame.Surface((TILE_W * MAP_COLS, TILE_H * MAP_ROWS))

        for x in range(0, MAP_COLS - 1):
            for y in range(0, MAP_ROWS - 1):
                tile = grid[(x, y)]["feature"]
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
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    Game(
        scene=MapTest, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
