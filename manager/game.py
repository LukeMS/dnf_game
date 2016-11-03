"""Classes for the game engine and scene templates."""
import os

import pygame

import constants
from manager import Images, Tilesets, Fonts


class Game(object):
    """Handle scenes and input."""

    _alive = False

    def __new__(cls, **kwargs):
        """Prevent creation of more then one instance."""
        if not hasattr(cls, '_instance'):
            print("Starting", cls.__name__)
            cls._instance = super().__new__(cls)
        else:
            raise NotImplemented
        return cls._instance

    def __init__(
        self, *, framerate=constants.LIMIT_FPS,
        width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT,
        show_fps=True, show_play_time=False, set_mode=None, **kwargs
    ):
        """..."""
        self.framerate = framerate

        self.tile_width = constants.TILE_W
        self.tile_height = constants.TILE_H

        self._scene = None

        self.scheduled_tasks = []

        pygame.init()

        info_object = pygame.display.Info()
        width = width or info_object.current_w
        height = height or info_object.current_h

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        set_mode = set_mode or (
            pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode((width, height), set_mode)

        self.clock = pygame.time.Clock()

        self.show_fps = show_fps
        self.ms = 0
        self.playtime = 0

        self.show_play_time = show_play_time

        pygame.font.init()
        self.images = Images()
        self.tilesets = Tilesets()
        self.fonts = Fonts()

        self._alive = False
        if 'scene' in kwargs:
            if 'scene_args' in kwargs:
                self.set_scene(kwargs['scene'], **kwargs['scene_args'])
            else:
                self.set_scene(kwargs['scene'])
            self.execute()

    @property
    def display(self):
        """..."""
        return pygame.display

    @property
    def alive(self):
        """..."""
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    def execute(self):
        """Main game loop."""
        self.alive = True
        # print("self.alive:", self.alive)
        # i = 1
        while self.alive:

            self.on_event()

            [task() for task in self.scheduled_tasks if task]
            self.on_update()

            self.ms = self.clock.tick(self.framerate)
            # if not i % 100:
            #    print("iterations of Game.execute:", i)
            # i += 1
        # print("self.alive:", self.alive)

    def on_event(self):
        """..."""
        for event in pygame.event.get():
            # Exit events
            if event.type == pygame.QUIT:
                print('pygame.QUIT')
                self.quit()
            else:
                # Deliver events to the current scene
                if self._scene:
                    self._scene.on_event(event)

    def disable_fps(self):
        """..."""
        self.update_on_time = False

    def enable_fps(self):
        """..."""
        self.update_on_time = True

    def schedule(self, task):
        """..."""
        self.scheduled_tasks.append(task)

    def unschedule(self, task):
        """..."""
        self.scheduled_tasks.remove(task)

    def on_update(self):
        """Update scene unless specified not to do so."""
        if self.alive and self._scene and not getattr(
            self._scene, "ignore_regular_update", False
        ):
            self.screen.fill((0, 0, 0))

            if self._scene:
                self._scene.on_update()
            else:
                print('no scene')
                print('self.alive:', self.alive)

            if self.show_fps:
                self.draw_fps()

            # Draw the screen
            pygame.display.flip()

            # self._scene.post_update()

    def draw_fps(self):
        """Draw the fps display."""
        ms = self.ms
        if self.show_fps and hasattr(self, "fps_hud"):
            text = "FPS: {:.3}".format(self.clock.get_fps())
            self.fps_hud.text = text
            self.fps_hud.draw()

    def set_scene(self, scene=None, **kwargs):
        """..."""
        if not scene:
            raise TypeError(scene, "is not a valid scene.")
        else:
            print("Loading scene:", scene)

        if self._scene:
            self._scene.clear()

        print(scene)
        self._scene = scene(**kwargs)

    def quit(self):
        """..."""
        self.alive = False
        self._scene.quit()

    def __getstate__(self):
        """..."""
        return None


if __name__ == '__main__':
    pass
