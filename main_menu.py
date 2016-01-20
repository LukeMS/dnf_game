import pygame

from game import BaseScene
import gui
import level


class MainMenu(BaseScene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.selection = 0
        self.create_items()
        self.gui = gui.Menu(
            gfx=self.game.gfx, title="Caves & Lizards Roguelike",
            items=[item["text"] for item in self._menu])

    def on_update(self):
        self.gui.draw()

    def create_items(self):
        self._menu = [
            {
                "text": "New Game",
                "kwargs": {
                    "scene": level.LevelScene
                }
            },
            {
                "text": "Load Game",
                "kwargs": {
                    "scene": level.LevelScene,
                    'new': False
                }
            },
            {
                "text": "Options",
                "action": "quit",
                "kwargs": {}
            },
            {
                "text": "Quit",
                "action": "quit",
                "kwargs": {}
            }
        ]

    def change_selection(self, value):
        self.selection += value
        self.selection = self.selection % len(self._menu)
        self.gui.select(self.selection)

    def on_key_press(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
        if event.key == pygame.K_UP:
            self.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            getattr(
                self.game,
                "set_scene"
            )(**self._menu[self.selection]['kwargs'])

    def clear(self):
        self.gui.clear()
        del self.gui

    def __getstate__(self):
        return None


if __name__ == '__main__':
    from game import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game = Game(
        scene=MainMenu, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
