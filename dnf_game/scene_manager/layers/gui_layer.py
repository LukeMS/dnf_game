"""..."""

from array import array

import sdl2

from dnf_game.dnf_main.data_handler import get_color
from dnf_game.scene_manager.layers.base_layers import Layer, LayerMultiLayer
from dnf_game.util.ext import gfxdraw
from dnf_game.util.ext.rect import Rect


class GUILayer(LayerMultiLayer):
    """..."""

    def __init__(self, *, parent, **kwargs):
        """..."""
        super().__init__(parent=parent, **kwargs)

    def create_button(self, **kwargs):
        """..."""
        button = GuiButton(parent=self, **kwargs)
        self.insert_layer(button)

    def create_textbox(self, **kwargs):
        """..."""
        textbox = GuiTextbox(parent=self, **kwargs)
        self.insert_layer(textbox)


class GuiElementBase(Layer):
    """Base for GUI elements."""


class GuiButton(GuiElementBase):
    """Button GUI element."""

    clicked = False
    hovered = False
    disabled = False

    radius = 15
    click_sound = None
    hover_sound = None

    states = ["regular", "clicked", "hovered", "disabled"]

    regular_color = (160, 160, 160)
    regular_color_mod = None
    regular_alpha_mod = None

    clicked_color = None
    clicked_color_mod = (160, 160, 180)
    clicked_alpha_mod = None

    hovered_color = None
    hovered_color_mod = (255, 255, 160)
    hovered_alpha_mod = None

    disabled_color = None
    disabled_color_mod = 0.7
    disabled_alpha_mod = 127

    regular_text = None
    regular_font = "caladea-regular.ttf"
    regular_font_size = 16
    regular_font_color = (31, 31, 63)
    regular_font_color_mod = None

    clicked_text = None
    clicked_font = None
    clicked_font_size = None
    clicked_font_color = None
    clicked_font_color_mod = None

    hovered_text = None
    hovered_font = "caladea-bold.ttf"
    hovered_font_size = None
    hovered_font_color = (7, 7, 15)
    hovered_font_color_mod = None

    disabled_text = None
    disabled_font = "caladea-italic.ttf"
    disabled_font_size = None
    disabled_font_color = None
    disabled_font_color_mod = 0.7

    def __init__(self, rect, command, **kwargs):
        """Initialization."""
        super().__init__(rect=rect, **kwargs)
        self.__dict__.update(kwargs)

        self.sprites = {}
        self.command = command

        self.create_buttons()
        self.create_text()

    def create_buttons(self):
        """Create the button sprites."""
        sdlrenderer = self.sdlrenderer
        new_render_target = self.factory.new_render_target
        from_new_texture = self.factory.from_new_texture

        rad = self.radius
        size = self.size
        rect = Rect(0, 0, *size)
        color = self.regular_color

        # e.g. regular_color, regular_color_mod
        for state in self.states:
            sprite = from_new_texture(*size)
            sprite_color = getattr(self, "%s_color" % state) or color
            color_mod = getattr(self, "%s_color_mod" % state)
            alpha_mod = getattr(self, "%s_alpha_mod" % state)
            with new_render_target(sprite.texture):
                gfxdraw.rounded_box(sdlrenderer,
                                    rect, rad, sprite_color)
            sprite.set_color_mod(color_mod)
            sprite.set_alpha_mod(alpha_mod)

            sprite.position = self.topleft

            self.sprites[state] = [sprite]

    def create_text(self):
        """Create the text sprites."""
        fonts = self.manager.fonts

        text = self.regular_text
        font = self.regular_font
        color = self.regular_font_color
        size = self.regular_font_size

        # e.g. regular_text, regular_font, regular_font_size,
        # regular_font_color, regular_font_color_mod
        for state in self.states:
            sprite_text = getattr(self, "%s_text" % state) or text
            sprite_font = getattr(self, "%s_font" % state) or font
            sprite_size = getattr(self, "%s_font_size" % state) or size
            sprite_color = getattr(self, "%s_font_color" % state) or color
            sprite_color_mod = getattr(self, "%s_font_color_mod" % state)

            sprite = fonts.render(text=sprite_text, name=sprite_font,
                                  size=sprite_size, color=sprite_color)

            sprite.set_color_mod(sprite_color_mod)

            button_sprite = self.sprites[state][0]
            sprite.center_on(button_sprite)

            self.sprites[state] = (button_sprite, sprite)

    def on_update(self):
        """super__doc__."""
        if self.disabled:
            state = "disabled"
        elif self.clicked:
            state = "clicked"
        elif self.hovered:
            state = "hovered"
        else:
            state = "regular"

        self.manager.spriterenderer.render(sprites=self.sprites[state])

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        if self.collidepoint(x=x, y=y):
            if not self.hovered and self.hover_sound:
                self.hover_sound.play()
            self.hovered = True
            self.on_update()
        else:
            self.hovered = False

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        if self.collidepoint(x=x, y=y):
            if button == "RIGHT":
                self.disabled = not self.disabled
            else:
                self.clicked = True
                self.command()
                self.on_update()
        else:
            self.clicked = False

    def texture_loader(self):
        """..."""
        pass


class GuiTextbox(GuiButton):
    """Textbox GUI element."""

    states = ["regular", "disabled"]

    radius = 0

    regular_color = get_color("darkest_grey")
    regular_color_mod = None
    regular_alpha_mod = None

    regular_font_color = get_color("green")

    outline_color = get_color("black")
    outline_width = 2
    clear_on_execute = False  # remove text upon enter
    disable_on_execute = True
    blink_speed = 500  # prompt blink time in milliseconds
    delete_speed = 60  # backspace held clear speed in milliseconds

    def __init__(self, rect, command, **kwargs):
        """Initialization.

        Args.:
            command (method): callback to execute when enter key is pressed.
                Callback will receive 2 arguments: id and final (the string
                in the textbox).
        """
        self.buffer = array("B")
        self.blink = True
        self.blink_timer = 0.0
        self.delete_timer = 0.0

        super().__init__(rect=rect, command=command, **kwargs)

        self.create_cursor()
        self.manager.set_text_input(True, self)

    def on_text_input(self, event):
        """..."""
        if event.type == sdl2.SDL_TEXTINPUT:
            self.buffer.append(ord(event.text.text))
            self.create_text()

    def on_key_press(self, event, mod):
        """super__doc__."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_BACKSPACE:
            self.handle_backspace()

    def on_key_release(self, event, mod):
        """super__doc__."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_RETURN:
            self.execute()

    def on_mouse_motion(self, x, y, dx, dy):
        """super__doc__."""
        if self.collidepoint(x=x, y=y):
            self.disabled = False
        else:
            self.disabled = True

    def on_mouse_press(self, event, x, y, button, double):
        """super__doc__."""
        if self.collidepoint(x=x, y=y):
            self.disabled = False
        else:
            self.disabled = True

    def execute(self):
        """..."""
        if self.command:
            self.command(self, self.regular_text)
        self.active = not self.disable_on_execute
        if self.clear_on_execute:
            del self.buffer[:]

    def switch_blink(self):
        """..."""
        ticks = sdl2.SDL_GetTicks()
        if ticks - self.blink_timer > self.blink_speed:
            self.blink = not self.blink
            self.blink_timer = ticks

    def handle_backspace(self):
        """..."""
        ticks = sdl2.SDL_GetTicks()
        if ticks - self.delete_timer > self.delete_speed:
            self.delete_timer = ticks
            try:
                self.buffer.pop()
            except IndexError:
                pass
            else:
                self.create_text()

    @property
    def regular_text(self):
        """..."""
        return self.buffer.tobytes().decode("utf-8") or " "

    def create_cursor(self):
        """..."""
        self.cursor = self.fonts.render(
            text="|", name=self.regular_font, size=self.regular_font_size,
            color=self.regular_font_color)
        self.cursor.set_color_mod(self.regular_font_color_mod)

    def on_update(self):
        """super__doc__."""
        self.switch_blink()
        if self.disabled:
            state = "disabled"
        elif self.clicked:
            state = "clicked"
        elif self.hovered:
            state = "hovered"
        else:
            state = "regular"

        sprites = self.sprites[state]

        text_sprite = sprites[1]

        rect = text_sprite.get_rect()

        if self.blink:
            sprites = (*sprites, self.cursor)
            self.cursor.position = rect.topright

        self.manager.spriterenderer.render(sprites=sprites)

    def create_text(self):
        """Create the text sprites."""
        fonts = self.manager.fonts
        text_size = fonts.text_size

        text = self.regular_text
        font = self.regular_font
        color = self.regular_font_color
        size = self.regular_font_size

        # e.g. regular_text, regular_font, regular_font_size,
        # regular_font_color, regular_font_color_mod
        for state in self.states:
            start = 0
            sprite_text = getattr(self, "%s_text" % state) or text
            sprite_font = getattr(self, "%s_font" % state) or font
            sprite_size = getattr(self, "%s_font_size" % state) or size
            sprite_color = getattr(self, "%s_font_color" % state) or color
            sprite_color_mod = getattr(self, "%s_font_color_mod" % state)
            while (text_size(sprite_text[start:],
                             sprite_font,
                             sprite_size
                             )[0] > (self.width - 6)):
                start += 1
            sprite_text = sprite_text[start:]

            sprite = fonts.render(text=sprite_text, name=sprite_font,
                                  size=sprite_size, color=sprite_color)

            sprite.set_color_mod(sprite_color_mod)

            button_sprite = self.sprites[state][0]
            sprite.center_on(button_sprite)

            self.sprites[state] = (button_sprite, sprite)

if __name__ == '__main__':
    from dnf_game.scene_manager import Manager
    from dnf_game.scene_manager.scenes import base_scenes
    from dnf_game.scene_manager.layers import base_layers
    from dnf_game.scene_manager.layers import gui_layer

    class SceneLayerGuiTextboxTest(base_scenes.SceneMultiLayer):
        """..."""

        def __init__(self, **kwargs):
            """..."""
            super().__init__(**kwargs)
            frame = base_layers.Layer(parent=self)
            frame.create_gradient_surface()
            gui = gui_layer.GUILayer(parent=self)
            rect = Rect(0, 0, 150, 30)
            # rect.bottomleft = (gui.left, gui.height)
            rect.bottomright = (self.width, self.height)
            gui.create_textbox(rect=rect,
                               command=print_on_enter,
                               disable_on_execute=False)
            self.insert_layer(frame, gui)

    def print_on_enter(id, final):
        """Sample callback function that prints a message to the screen."""
        locals()["manager"] = Manager()
        print('enter pressed, textbox contains "{}"'.format(final))
        try:
            eval(final)
        except SyntaxError:
            print("not a valid command.")

    Manager(scene=SceneLayerGuiTextboxTest, test=False).execute()
