"""..."""

import pygame

import game
import level_layer
import level_hud


class Main(game.MultiLayer):
    """..."""

    def __init__(self, game, new=True, character=None, mode='pit'):
        """..."""
        super().__init__(game)

        self.create_layers(new=new, mode=mode)

    @property
    def gfx(self):
        """..."""
        return self.game.gfx

    @property
    def player(self):
        """..."""
        return self.level_layer.player

    @property
    def choice(self):
        """..."""
        return self.choice_layer.choice

    @property
    def transition(self):
        """..."""
        return self.transition_layer.transition

    def create_layers(self, new, mode):
        """..."""

        self.transition_layer = level_hud.TextLayer(parent=self)

        self.level_layer = level_layer.Level(
            parent=self, new=new, mode=mode)
        self.insert_layer(self.level_layer)

        self.inventory_layer = level_hud.InventoryLayer(parent=self)
        self.insert_layer(self.inventory_layer)

        self.choice_layer = level_hud.ChoiceLayer(parent=self)
        self.insert_layer(self.choice_layer)

    def insert_layer(self, obj, pos=None):
        """..."""
        if pos is not None:
            self.layers.insert(pos, obj)
        else:
            self.layers.append(obj)
        self.on_update()

    def on_key_press(self, event):
        """..."""
        for layer in reversed(self.layers):
            if layer.on_key_press(event) is True:
                break

    def on_mouse_press(self, event):
        """..."""
        pos, rel_pos = self.level_layer.cursor_pos()
        for layer in reversed(self.layers):
            if layer.on_mouse_press(event):
                break

    def on_mouse_scroll(self, event):
        """..."""
        for layer in reversed(self.layers):
            if layer.on_mouse_scroll(event):
                break

    def on_update(self):
        """..."""
        self.screen.fill((0, 0, 0))
        [layer.on_update() for layer in self.layers]
        self.game.display.flip()

if __name__ == '__main__':
    game.Game(scene=Main)
