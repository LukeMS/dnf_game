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
        self.load_tileset()

        self.fonts = resources.Fonts(path=os.path.join("resources", "fonts"))

        self.hp_bar = gui.Bar(name="Health", value=100, maximum=100, gfx=self)
        self.msg_log = gui.MsgLog(gfx=self)
        self.fps_time_label = gui.Hud(gfx=self)

    def draw_hud(self):
        self.hp_bar.draw()
        self.msg_log.draw()

    def load_tileset(self):
        _tileset = resources.Tileset.get(None)
        self.tileset_width, self.tileset_height = _tileset.get_size()

    def get_tile(self, char):
        if isinstance(char, str):
            id = ord(char)
        else:
            id = char
        # (self.tileset_width, self.tileset_height)
        y = id // (self.tileset_width // TILE_W)
        x = id % (self.tileset_width // TILE_W)
        return x * TILE_W, y * TILE_H, TILE_W, TILE_H

    def get_image(self, id, color=None):
        src = self.get_tile(id)
        surface = resources.Tileset.get(color)

        return surface, src

    def draw(self, id, xy, color=None):
        x, y = xy

        dest = pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

        surface, src = self.get_image(id, color)

        self.screen.blit(
            source=surface, dest=dest, area=src)
