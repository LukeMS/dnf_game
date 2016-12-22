"""..."""

import string

from dnf_game.scene_manager.layers.base_layers import Layer
from dnf_game.util.ext import gfxdraw


class GUILayer(Layer):
    """..."""

    def __init__(self, *, parent, **kwargs):
        """..."""
        super().__init__(parent=parent, **kwargs)
        self.buttons = []
        self.textboxes = []

    def create_button(self, **kwargs):
        """..."""
        button = GuiButton(parent=self, **kwargs)
        self.buttons.append(button)

    def create_textbox(self, **kwargs):
        """..."""
        textbox = GuiButton(parent=self, **kwargs)
        self.textboxes.append(textbox)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        [element.on_key_press(event, mod)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        [element.on_key_release(event, mod)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_mouse_drag(self, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged."""
        [element.on_mouse_drag(x, y, dx, dy, button)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        [element.on_mouse_motion(x, y, dx, dy)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        [element.on_mouse_press(event, x, y, button, double)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        [element.on_mouse_scroll(event, offset_x, offset_y)
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.active]

    def on_update(self):
        """Graphical logic."""
        [element.on_update()
         for group in [self.buttons, self.textboxes]
         for element in group
         if element.visible]


class GuiElementBase(Layer):
    """..."""

    pass


class GuiButton(GuiElementBase):
    """Button GUI element."""

    def __init__(self, rect, command, **kwargs):
        """Initialization.

        Optional kwargs and their defaults:
            "color"             : pg.Color('red'),
            "text"              : None,
            "font"              : None, #pg.font.Font(None,16),
            "call_on_release"   : True,
            "hover_color"       : None,
            "clicked_color"     : None,
            "font_color"        : pg.Color("white"),
            "hover_font_color"  : None,
            "clicked_font_color": None,
            "click_sound"       : None,
            "hover_sound"       : None,
            'border_color'      : pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled'          : False,
            'disabled_color'     : pg.Color('grey'),
            'radius'            : 3,

        Values:
            self.command = command
            self.clicked = False
            self.hovered = False
            self.hover_text = None
            self.clicked_text = None
        """
        super().__init__(rect=rect, **kwargs)
        self.command = command

        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None

        self.process_kwargs(kwargs)

        self.render_text()

    def process_kwargs(self, kwargs):
        """..."""
        settings = {
            "color": pg.Color('red'),
            "text": None,
            "font": None,  # pg.font.Font(None,16),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": pg.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            'border_color': pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled': False,
            'disabled_color': pg.Color('grey'),
            'radius': 3,
        }
        self.__dict__.update({**settings, **kwargs})

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def get_event(self, event):
        """ Call this on your event loop

            for event in pg.event.get():
                Button.get_event(event)
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            # if user is still within button rect upon mouse release
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def draw(self, surface):
        """
        Args:
            surface: screen
        Call once on your main game loop
        """
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text

            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color

        if self.radius:
            rad = self.radius
        else:
            rad = 0
        manager = self.manager
        factory = manager.factory
        renderer = manager.renderer
        self.sprite = factory.from_new_texture(*self.rect.size)
        texture = self.sprite.texture

        with factory.new_render_target(texture):
            gfxdraw.rounded_box(renderer.sdlrenderer,
                                self.rect, rad, color)
        if self.text:
            text_sprite = manager.fonts.render(
                text=self.text, name=self.font_name, size=self.font_size,
                color=self.font_color)
            text_sprite_rect = text_sprite.get_rect()
            text_sprite_rect.center = self.rect.center
            text_sprite.set_rect = text_sprite_rect

            renderer.render(sprites=(self.sprite, text_sprite))


class GuiTextBox(object):
    """
    Example can found in run_textbox.py.py

    """

    def __init__(self, rect, **kwargs):
        """Initialization.

        Optional kwargs and their defaults:
            "id": None,
            "command": None,
                function to execute upon enter key
                Callback for command takes 2 args, id and final (the string
                in the textbox)
            "active" : True,
                textbox active on opening of window
            "color" : pg.Color("white"),
                background color
            "font_color" : pg.Color("black"),
            "outline_color" : pg.Color("black"),
            "outline_width" : 2,
            "active_color" : pg.Color("blue"),
            "font" : pg.font.Font(None, self.rect.height+4),
            "clear_on_enter" : False,
                remove text upon enter
            "inactive_on_enter" : True
            "blink_speed": 500
                prompt blink time in milliseconds
            "delete_speed": 500
                backspace held clear speed in milliseconds

        Values:
            self.buffer = []
            self.final = None
            self.rendered = None
            self.render_rect = None
            self.render_area = None
            self.blink = True
            self.blink_timer = 0.0
            self.delete_timer = 0.0
            self.accepted = (string.ascii_letters + string.digits +
                             string.punctuation + " ")
        """
        super().__init__(rect=rect, **kwargs)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.delete_timer = 0.0
        self.accepted = (string.ascii_letters + string.digits +
                         string.punctuation + " ")
        self.process_kwargs(kwargs)

    def process_kwargs(self, kwargs):
        """..."""
        defaults = {"id": None,
                    "command": None,
                    "active": True,
                    "color": pg.Color("white"),
                    "font_color": pg.Color("black"),
                    "outline_color": pg.Color("black"),
                    "outline_width": 2,
                    "active_color": pg.Color("blue"),
                    "font": pg.font.Font(None, self.rect.height + 4),
                    "clear_on_enter": False,
                    "inactive_on_enter": True,
                    "blink_speed": 500,
                    "delete_speed": 75}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("TextBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self, event, mouse_pos=None):
        """Call this on your event loop.

            for event in pg.event.get():
                TextBox.get_event(event)
        """
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not mouse_pos:
                mouse_pos = pg.mouse.get_pos()
            self.active = self.rect.collidepoint(mouse_pos)

    def execute(self):
        """..."""
        if self.command:
            self.command(self.id, self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def switch_blink(self):
        """..."""
        if pg.time.get_ticks() - self.blink_timer > self.blink_speed:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def update(self):
        """
        Call once on your main game loop
        """
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x + 2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width - 6:
                offset = self.render_rect.width - (self.rect.width - 6)
                self.render_area = pg.Rect(offset, 0, self.rect.width - 6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))
        self.switch_blink()
        self.handle_held_backspace()

    def handle_held_backspace(self):
        if pg.time.get_ticks() - self.delete_timer > self.delete_speed:
            self.delete_timer = pg.time.get_ticks()
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                if self.buffer:
                    self.buffer.pop()

    def draw(self, surface):
        """
        Call once on your main game loop
        """
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(
            self.outline_width * 2, self.outline_width * 2)
        surface.fill(outline_color, outline)
        surface.fill(self.color, self.rect)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,
                         (curse.right + 1, curse.y, 2, curse.h))
