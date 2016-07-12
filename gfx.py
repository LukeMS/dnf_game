import os

import pygame

from constants import TILE_W, TILE_H
import resources
import gui


class PygameGFX:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        pygame.font.init()

        self.images = resources.Images(path="resources")
        self.tileset_mgr = resources.Tilesets()
        self.fonts = resources.Fonts()

        self.hp_bar = gui.Bar(name="Health", value=100, maximum=100, gfx=self)
        self.msg_log = gui.MsgLog(gfx=self)
        self.fps_time_label = gui.Hud(gfx=self)
        self.inventory = gui.Inventory(gfx=self)
        self.choice = gui.Choice(gfx=self)
        self.msg = gui.Msg(gfx=self)

    def draw_hud(self):
        self.hp_bar.draw()
        self.msg_log.draw()

    def draw(self, id, xy, color=None,
             tiling_index=0, tile_variation=0):
        x, y = xy

        dest = pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

        src, surface = resources.Tilesets.get_tile(
            id, color,
            tiling_index, tile_variation)

        self.screen.blit(
            source=surface, dest=dest, area=src)

    def __getstate__(self):
        """Class will be ignored by pickle."""
        return None
