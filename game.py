import os

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


class Game:
    """Represents the main object of the game.

    The Game object keeps the game on, and takes care of updating it,
    drawing it and propagate events.

    This object must be used with Scene objects that are defined later."""

    def __init__(
        self, scene=BaseScene, framerate=60, width=1024, height=768,
        show_fps=True, show_play_time=False,
        *args, **kwargs
    ):
        self.framerate = framerate
        self.playtime = 0

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        # pygame.display.set_caption("libtcod tutorial")
        self.gfx = gfx.PygameGFX(game=self)

        self.show_fps = show_fps
        self.show_play_time = show_play_time

        self.set_scene(scene=scene, *args, **kwargs)

        self.alive = True
        self.clock = pygame.time.Clock()

        self.execute()

    def execute(self):
        "Main game loop."
        while self.alive:

            self.on_event()

            self.on_update()

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

    def on_event(self):
        # Exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            else:
                # Handles events to the current scene
                self.current_scene.on_event(event)

    def on_update(self):
        # Update scene
        self.screen.fill((0, 0, 0))
        self.current_scene.on_update()

        ms = self.clock.tick(self.framerate)
        if self.show_fps or self.show_play_time:
                self.draw_fps(ms)

        # Draw the screen
        pygame.display.flip()

        self.current_scene.post_update()

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
        self.current_scene.quit()
        self.alive = False
