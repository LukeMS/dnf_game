import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import manager
from manager.scenes import base_scenes


class Test(base_scenes.SceneBase):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

        self.create_surface()

    def create_surface(self):
        """..."""
        self.surface = pygame.Surface((self.width, self.height))

        ar = pygame.PixelArray(self.surface)
        r, g, b = 0, 0, 0

        # Do some easy gradient effect.
        for y in range(self.height):
            scale = int(y / self.height * 255)
            r, g, b = scale // 2, scale // 2, scale
            ar[:, y] = (r, g, b)
        del ar

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
if __name__ == '__main__':
    """
    import os
    import sys
    path = os.path.join(os.path.dirname(__file__), "..", "resources", "fonts",
                        'DejaVuSansMono-Bold32.png')
    print(path)
    print(os.path.isfile(path))
    exit()
    """
    g = manager.Game()
    g.set_scene(Test)
    g.execute()
