import os

import pygame
"""..."""

import game
import char_creation
import gui


class Main(game.MultiLayer):
    """..."""

    def __init__(self, game, draw_all=False):
        """..."""
        super().__init__(game)
        self.insert_layer(MainMenu)


class Options(game.Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent)
        self.gfx.choice.set_list(
            title='Level up! Choose a stat to raise:',
            items=[
                'Str',
                'Dex',
                'Int',
                'Wis'
            ],
            callback=self.remove
        )

    def remove(self, choice):
        """..."""
        print(choice)
        super().remove()

    def on_update(self):
        """..."""
        self.gfx.choice.draw()

    def on_key_press(self, event):
        """..."""
        choice = self.gfx.choice

        if event.key == pygame.K_ESCAPE:
            pass
            # level.game_state = 'playing'
            # choice.clear()
        elif event.key == pygame.K_UP:
            choice.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            choice.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            choice.confirm()
            choice.clear()


class MainMenu(game.Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent)
        self.selection = 0

        self.create_items()

        self.gui = gui.Menu(
            gfx=self.game.gfx, title="Caves & Lizards Roguelike",
            items=[item["text"] for item in self._menu])

    def on_update(self):
        """..."""
        self.gui.draw()

    def create_items(self):
        """..."""
        self._menu = [
         {
                "text": "New character",
                "action": self.parent.insert_layer,
                "kwargs": {
                    "obj": char_creation.Create
                },
            },
            {
                "text": "Options",
                "action": self.parent.insert_layer,
                "kwargs": {
                    "obj": Options
                }
            },
            {
                "text": "Quit",
                "action": quit,
                "kwargs": {}
            }
        ]

    def change_selection(self, value):
        """..."""
        self.selection += value
        self.selection = self.selection % len(self._menu)
        self.gui.select(self.selection)

    def on_key_press(self, event):
        """..."""
        if event.key == pygame.K_ESCAPE:
            self.quit()
        if event.key == pygame.K_UP:
            self.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            self._menu[self.selection]['action'](
                **self._menu[self.selection]['kwargs'])

    def clear(self):
        """..."""
        self.gui.clear()
        del self.gui

    def quit(self):
        exit()

    def __getstate__(self):
        """..."""
        return None


if __name__ == '__main__':
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game.Game(
        scene=Main, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
