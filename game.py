"""Classes for the game engine and scene templates."""

import time

import pygame
from pygame_manager import manager

import gfx
import constants


class BaseScene(manager.BaseScene):
    pass


class MultiLayer(manager.MultiLayer):
    pass


class Layer(manager.Layer):
    pass

class Window(manager.Window):
    pass

class Game(manager.Manager):
    """The main class for the game engine.

    Handles the game loop, delivering events (input, graphics updates, etc.)
    to the Scene objects and handling their transitions.
    """

    def __init__(
        self, scene=BaseScene, framerate=constants.LIMIT_FPS,
        width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT,
        show_fps=True, show_play_time=False, *args, **kwargs
    ):
        """..."""
        super().__init__(framerate=framerate,
                         width=width, height=height,
                         show_fps=show_fps)

        self.playtime = 0

        self.show_play_time = show_play_time

        self.gfx = gfx.PygameGFX(game=self)

        self.fps_hud = self.gfx.fps_time_label

        self.set_scene(scene)

        self.execute()

    def __getstate__(self):
        """..."""
        return None


if __name__ == '__main__':
    class Test(BaseScene):
        """..."""

        def __init__(self, game):
            """..."""
            super().__init__(game)
            self.game = game

            self.create_surface()

        def create_surface(self):
            """..."""
            self.surface = pygame.Surface((self.width, self.height))

            ar = pygame.PixelArray(self.surface)
            r, g, b = 0, 0, 0

            t1 = time.time()
            # Do some easy gradient effect.
            for y in range(self.height):
                scale = int(y / self.height * 255)
                r, g, b = scale // 2, scale // 2, scale
                ar[:, y] = (r, g, b)
            del ar

            t2 = time.time()
            print(t2 - t1)

        def flip_surface(self):
            """..."""
            ar = pygame.PixelArray(self.surface)
            ar[:] = ar[:, ::-1]
            del ar

        def on_update(self):
            """..."""
            screen = self.screen
            surface = self.surface

            screen.fill((255, 255, 255))
            screen.blit(surface, (0, 0))

        def on_mouse_press(self, event):
            """..."""
            self.flip_surface()

        def on_key_press(self, event):
            """..."""
            if event.key == pygame.K_ESCAPE:
                self.quit()

    Game(scene=Test)
