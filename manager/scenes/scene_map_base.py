import pygame

from constants import TILE_W, TILE_H
from manager.scenes import base_scenes
from manager.windows import base_windows
from manager import Tilesets


class SceneMapBase(base_scenes.SceneMultiLayer):
    """..."""

    @property
    def tile_width(self):
        """..."""
        return self.game.tile_width

    @property
    def tile_height(self):
        """..."""
        return self.game.tile_height

    @property
    def cols(self):
        """..."""
        return self.width // self.tile_width

    @property
    def rows(self):
        """..."""
        return self.height // self.tile_height

    def create_layers(self):
        """..."""
        self.hp_bar = base_windows.Bar(parent=self, name="Health")
        self.msg_log = base_windows.MsgLog(parent=self)
        self.fps_time_label = base_windows.Hud(parent=self)
        self.inventory = base_windows.Inventory(parent=self)
        self.choice = base_windows.Choice(parent=self)
        self.msg = base_windows.Msg(parent=self)

        for layer in [self.hp_bar, self.msg_log, self.fps_time_label,
                      self.inventory, self.choice, self.msg]:
            self.insert_layer(layer)

    def draw_tile(
        self, id, xy, color=None, tiling_index=0, tile_variation=0
    ):
        """..."""
        x, y = xy

        dest = pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

        src, surface = Tilesets.get_tile(
            id, color,
            tiling_index, tile_variation)

        self.screen.blit(
            source=surface, dest=dest, area=src)

    def draw_fog(self, xy):
        """..."""
        x, y = xy

        dest = pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

        # the size of your rect
        surface = pygame.Surface((TILE_W, TILE_H))

        # alpha level
        surface.set_alpha(191)

        # this fills the entire surface
        surface.fill((0, 0, 7))

        self.screen.blit(source=surface, dest=dest)

    def on_key_press(self, event):
        """..."""
        [layer.on_key_press(event)
         for layer in self.layers if layer.active]

    def on_mouse_press(self, event):
        """..."""
        # pos, rel_pos = self.level_layer.cursor_pos()
        [layer.on_mouse_press(event)
         for layer in self.layers if layer.active]

    def on_mouse_scroll(self, event):
        """..."""
        [layer.on_mouse_scroll(event)
         for layer in self.layers if layer.active]

    def on_update(self):
        """..."""
        [layer.on_update() for layer in self.layers if layer.visible]
