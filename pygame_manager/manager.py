"""Classes for the game engine and scene templates."""

import os

import pygame


def default_window_skin(size=32):
    """Return the default window skin."""
    path = os.path.join(os.path.dirname(__file__),
                        "skins", "default", "window_{}px.png".format(size))
    return pygame.image.load(path).convert_alpha()


class BaseScene:
    """Represents a scene of the game.

    Scenes must be created inheriting this class attributes
    in order to be used afterwards as menus, introduction screens,
    etc.
    """

    def __init__(self, game):
        """..."""
        self.game = game

        # If set to True the update will not be called by Game.
        # Useful for cases where the scene needs to handle itself.
        self.ignore_regular_update = False

    @property
    def screen(self):
        """..."""
        return self.game.screen

    @property
    def width(self):
        """..."""
        return getattr(self, '_height', None) or self.screen.get_width()

    @property
    def height(self):
        """..."""
        return getattr(self, '_height', None) or self.screen.get_height()

    @width.setter
    def width(self, value):
        """..."""
        self._width = value

    @height.setter
    def height(self, value):
        """..."""
        self._height = value

    def start(self):
        """..."""
        pass

    def clear(self):
        """..."""
        pass

    def on_update(self):
        """Called from Game, should be redefined on the subclasses."""
        pass

    def post_update(self):
        """..."""
        pass

    def on_event(self, event):
        """Called when a specific event is detected in the loop.

        Deliver those events to their specific methods.
        """
        if event.type == pygame.KEYDOWN:
            # print('key pressed')
            self.on_key_press(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button <= 3:
                self.on_mouse_press(event)
            else:
                self.on_mouse_scroll(event)

    def on_mouse_press(self, event):
        """..."""
        pass

    def on_mouse_scroll(self, event):
        """..."""
        pass

    def on_key_press(self, event):
        """..."""
        pass

    def on_key_held(self):
        """..."""
        pass

    def quit(self):
        """..."""
        self.game.alive = False

    def __getstate__(self):
        """..."""
        return None


class MultiLayer(BaseScene):
    """..."""

    def __init__(self, game, draw_all=False):
        """..."""
        super().__init__(game)

        self.draw_all = draw_all
        self.layers = []

    def insert_layer(self, obj):
        layer = obj(parent=self)
        self.layers.append(layer)

    def remove_layer(self, obj):
        self.layers.remove(obj)

    def on_update(self):
        """..."""
        if self.draw_all:
            for layer in self.layers:
                layer.on_update()
        else:
            self.layers[-1].on_update()

    def post_update(self):
        """..."""
        if self.draw_all:
            for layer in self.layers:
                layer.post_update()
        else:
            self.layers[-1].post_update()

    def on_key_press(self, event):
        """..."""
        self.layers[-1].on_key_press(event)


class Layer(BaseScene):
    """..."""

    bottom_color = (15, 15, 31)
    top_color = (0, 0, 0)

    def __init__(self, parent):
        """..."""
        self.parent = parent

    @property
    def game(self):
        """..."""
        return self.parent.game

    @property
    def gfx(self):
        """..."""
        return self.parent.game.gfx

    @property
    def screen(self):
        """..."""
        return self.parent.screen

    def remove(self):
        """..."""
        self.parent.remove_layer(self)

    def create_solid_surface(self, color=(0, 0, 0)):
        """..."""
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)

    def create_gradient(self):
        """..."""
        bottom_color = self.bottom_color
        top_color = self.top_color

        if getattr(self, 'width', None) is None:
            if getattr(self, 'screen', None) is None:
                self.screen = pygame.display.get_surface()
            self.height = self.screen.get_height()
            self.width = self.screen.get_width()

        self.surface = pygame.Surface((self.width, self.height))

        ar = pygame.PixelArray(self.surface)

        # Do some easy gradient effect.
        for y in range(self.height):

            r = int((bottom_color[0] - top_color[0]) *
                    y / self.height +
                    top_color[0])
            g = int((bottom_color[1] - top_color[1]) *
                    y / self.height +
                    top_color[1])
            b = int((bottom_color[2] - top_color[2]) *
                    y / self.height +
                    top_color[2])

            ar[:, y] = (r, g, b)
        del ar

    def flip_surface(self):
        """..."""
        ar = pygame.PixelArray(self.surface)
        ar[:] = ar[:, ::-1]
        del ar


class Window(Layer):
    """..."""

    def __init__(self, parent, x=0, y=0, w=None, h=None, tile_size=32):
        """..."""
        self.parent = parent
        if w % tile_size:
            self.width = ((w or parent.width) // 32 + 1) * 32
            self.x = max(x - (self.width - w) // 2, 0)
        else:
            self.width = w or parent.width
            self.x = x
        if h % tile_size:
            self.height = ((h or parent.height) // 32 + 1) * 32
            self.y = max(y - (self.height - y) // 2, 0)
        else:
            self.height = h or parent.height
            self.y = y

        self.tile_size = tile_size
        self.window_skin = default_window_skin(tile_size)

    def hide(self):
        """NOT IMPLEMENTED."""
        return
        self.visible = False

    def set_margin(self, v):
        """..."""
        self.width += v * 2
        self.height += v * 2
        self.x = max(self.x - v, 0)
        self.y = max(self.y - v, 0)

    def draw_window(self):
        """..."""
        max_x = self.width // self.tile_size
        max_y = self.height // self.tile_size

        for x in range(0, max_x):
            for y in range(0, max_y):
                tile_pos = [1, 1]
                if y == 0:
                    tile_pos[1] = 0
                elif y == max_y - 1:
                    tile_pos[1] = 2
                if x == 0:
                    tile_pos[0] = 0
                elif x == max_x - 1:
                    tile_pos[0] = 2

                self.draw_tile(tile_pos, (x, y))

    def draw_tile(self, tile_pos, sfc_pos):
        """..."""
        surface = self.screen
        x, y = sfc_pos

        size = self.tile_size

        dest = pygame.Rect(x * size + self.x, y * size + self.y, size, size)

        src_area = tile_pos[0] * size, tile_pos[1] * size, size, size

        src_img = self.window_skin

        surface.blit(source=src_img, dest=dest, area=src_area)

    def on_update(self):
        """..."""
        self.draw_window()


class Hud:
    """..."""

    def __init__(self):
        """..."""
        self.font = pygame.font.Font(None, 18)
        self.screen = pygame.display.get_surface()
        self.x, self.y = self.screen.get_size()
        self.x -= 32
        self.y = 0
        self.text = ""

    def draw(self):
        """..."""
        self.display = self.font.render(
            self.text, False, (127, 255, 127))
        w, h = self.font.size(self.text)
        self.screen.blit(self.display, (self.x - w, self.y + h))


class Manager:
    """Scene Manager.

    Handles the main loop, delivering events (input, graphics updates, etc.)
    to the Scene objects and handling their transitions.
    """

    def __init__(
        self, scene=BaseScene, framerate=30,
        width=None, height=None,
        show_fps=True, set_mode=None, *args, **kwargs
    ):
        """..."""
        self.framerate = framerate
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

        self.set_scene(scene=scene, *args, **kwargs)

        self.alive = True

        self.fps_hud = Hud()

    @property
    def display(self):
        """..."""
        return pygame.display

    def execute(self):
        """Main game loop."""
        while self.alive:

            self.on_event()

            for task in self.scheduled_tasks:
                task()
            self.on_update()

            self.ms = self.clock.tick(self.framerate)

    def on_event(self):
        """..."""
        for event in pygame.event.get():
            # Exit events
            if event.type == pygame.QUIT:
                self.quit()
            else:
                # Deliver events to the current scene
                self.current_scene.on_event(event)

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
        if not self.current_scene.ignore_regular_update:
            self.screen.fill((0, 0, 0))
            self.current_scene.on_update()

            if self.show_fps:
                self.draw_fps()

            # Draw the screen
            pygame.display.flip()

            self.current_scene.post_update()

    def draw_fps(self):
        """Draw the fps display."""
        ms = self.ms
        if self.show_fps:
            text = "FPS: {:.3}".format(self.clock.get_fps())
            self.fps_hud.text = text
            self.fps_hud.draw()

    def set_scene(self, scene=None, *args, **kwargs):
        """..."""
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
        """..."""
        self.old_scene.clear()
        del self.old_scene

    def start_scene(self):
        """..."""
        self.current_scene.start()

    def quit(self):
        """..."""
        self.alive = False
        self.current_scene.quit()

    def __getstate__(self):
        """..."""
        return None


if __name__ == '__main__':
    Manager()
