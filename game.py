import os
import threading
import time

import pygame

import gfx


class BaseScene:
    """Represents a scene of the game.

    Scenes must be created inheriting this class attributes
    in order to be used afterwards as menus, introduction screens,
    etc."""

    def __init__(self, game):
        self.game = game

    def start(self):
        pass

    def clear(self):
        pass

    def on_update(self):
        "Called from the game and defined on the subclass."
        "Precedes on_draw, so this can be used for you logic"
        pass

    def post_update(self):
        pass

    def on_event(self, event):
        "Called when a specific event is detected in the loop."
        "Handle event types to their own methods"
        if event.type == pygame.KEYDOWN:
            # print('key pressed')
            self.on_key_press(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button <= 3:
                self.on_mouse_press(event)
            else:
                self.on_mouse_scroll(event)

    def on_mouse_press(self, event):
        pass

    def on_mouse_scroll(self, event):
        pass

    def on_key_press(self, event):
        pass

    def on_key_held(self):
        pass

    def quit(self):
        self.game.alive = False

    def __getstate__(self):
        return None


class Game:
    """Represents the main object of the game.

    The Game object keeps the game on, and takes care of updating it,
    drawing it and propagate events.

    This object must be used with Scene objects that are defined later."""

    def __init__(
        self, scene=BaseScene, framerate=30, width=1024, height=768,
        show_fps=True, show_play_time=False,
        *args, **kwargs
    ):
        self.framerate = framerate
        self.playtime = 0

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(
            (width, height),
            pygame.NOFRAME|pygame.HWSURFACE|pygame.DOUBLEBUF)
        # pygame.display.set_caption("libtcod tutorial")
        self.gfx = gfx.PygameGFX(game=self)

        self.show_fps = show_fps
        self.show_play_time = show_play_time

        self.set_scene(scene=scene, *args, **kwargs)

        self.alive = True
        self.clock = pygame.time.Clock()

        self.LOCK = threading.Lock()

        self.execute()

    def execute(self):
        "Main game loop."
        self.ms = 0
        while self.alive:

            threading.Thread(target=self.on_update, daemon=True).start()
            self.on_event()

            self.ms = self.clock.tick(self.framerate)

    def on_event(self):
        # Exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            else:
                # Handles events to the current scene
                self.current_scene.on_event(event)

    def on_update(self):
        # self.LOCK.acquire()
        # Update scene
        self.screen.fill((0, 0, 0))
        self.current_scene.on_update()

        if self.show_fps or self.show_play_time:
            self.draw_fps(self.ms)

        # Draw the screen
        pygame.display.flip()

        self.current_scene.post_update()
        # self.LOCK.release()

    def draw_fps(self, ms):
        self.playtime += ms / 1000.0
        if self.show_fps and self.show_play_time:
            text = "FPS: {:.3}, PLAYTIME: {:.3} SECONDS".format(
                self.clock.get_fps(), self.playtime)
        elif self.show_fps:
            text = "FPS: {:.3}".format(self.clock.get_fps())
        else:
            text = "PLAYTIME: {:.3} SECONDS".format(self.playtime)
        self.gfx.fps_time_label.text = text
        self.gfx.fps_time_label.draw()

    def set_scene(self, scene=None, *args, **kwargs):
        if scene is None:
            self.quit()
        else:
            if "current_scene" in self.__dict__:
                self.old_scene = self.current_scene
                self.current_scene = scene(game=self, *args, **kwargs)
                self.clear_scene()
            else:
                self.current_scene = scene(game=self, *args, **kwargs)

            self.start_scene()

    def clear_scene(self):
        self.old_scene.clear()
        del self.old_scene

    def start_scene(self):
        self.current_scene.start()

    def quit(self):
        self.alive = False
        self.current_scene.quit()

    def __getstate__(self):
        return None


if __name__ == '__main__':
    class Test(BaseScene):
        def __init__(self, game):
            self.game = game
            self.screen = pygame.display.get_surface()
            (self.width, self.height) = self.screen.get_size()

            self.create_surface()

        def create_surface(self):

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
            ar = pygame.PixelArray(self.surface)
            ar[:] = ar[:, ::-1]
            del ar

        def on_update(self):
            screen = self.screen
            surface = self.surface

            screen.fill((255, 255, 255))
            screen.blit(surface, (0, 0))

        def on_mouse_press(self, event):
            self.flip_surface()

        def on_key_press(self, event):
            if event.key == pygame.K_ESCAPE:
                self.quit()
if __name__ == '__main__':
    Game(scene=Test)
