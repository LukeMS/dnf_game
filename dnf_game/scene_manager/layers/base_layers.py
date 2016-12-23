"""..."""

import sdl2

from dnf_game.data.constants import COLORS
from dnf_game.scene_manager.base_entity import (EntityBase,
                                                MultiLayeredEntityBase)
from dnf_game.util import roundrobin, Font, LBPercentTable
from dnf_game.util.ext import time
from dnf_game.util.ext.rect import Rect


class LogicLayer(EntityBase, Rect):
    """A basic layer without the most of the graphical functions."""

    active = True
    visible = True

    def __new__(cls, *, parent, **kwargs):
        """Create a new instance of a layer.

        A reference to the manager is stored before returning it.

        Args:
            parent (EntityBase subclass): the scene or layer that hold this
            entity.
            manager (dnf_game.scene_manager.manager.Manager): a instance
            of the Manager
        """
        layer = super().__new__(cls)
        layer.parent = parent
        layer.manager = parent.manager
        return layer

    def __init__(self, *, rect=None, **kwargs):
        """..."""
        parent = self.parent
        rect = rect or (0, 0, parent.width, parent.height)
        Rect.__init__(self, rect)

    def __repr__(self):
        """..."""
        return "%s(%d, %d, %d, %d)" % (
            self.__class__.__name__, self.x, self.y, self.w, self.h)


class Layer(LogicLayer):
    """A basic graphical layer."""

    @property
    def cols(self):
        """The number of columns, considering the current tile width."""
        return self._cols

    @cols.setter
    def cols(self, value):
        self._cols = value

    @property
    def rows(self):
        """The number of rows, considering the current tile height."""
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def hide(self):
        """Set visible to False."""
        self.visible = False
        return self

    def show(self):
        """Set visible to True."""
        self.visible = True
        return self

    def activate(self):
        """Set active to True."""
        self.active = True
        return self

    def deactivate(self):
        """Set active to False."""
        self.active = False
        return self

    def on_update(self):
        """Graphical logic.

        Method is called by the parent scene.
        """
        try:
            self.manager.spriterenderer.render(sprites=self.surface)
        except AttributeError:
            pass

    def create_solid_surface(self, *, color, rect=None, **kwargs):
        """..."""
        factory = self.manager.factory
        rect = rect or self
        self.surface = factory.from_color(color=color, rect=rect, **kwargs)

    def create_gradient_surface(self, rect=None, **kwargs):
        """..."""
        factory = self.manager.factory
        rect = rect or self
        self.surface = factory.from_gradient(rect=rect, **kwargs)


class LayerMultiLayer(MultiLayeredEntityBase, Layer):
    """Scene with child entities (e.g.:layers)."""

    def __init__(self, *, draw_all=True, **kwargs):
        """..."""
        Layer.__init__(self, **kwargs)
        MultiLayeredEntityBase.__init__(self, draw_all=draw_all, **kwargs)


class Window(Layer):
    """..."""

    def __init__(self, *, parent, rect, tile_size=32, padding=0):
        """..."""
        super().__init__(parent=parent, rect=rect)
        self.tile_size = tile_size
        self.tiles = set()
        self.default_center = self.center
        self.set_padding(padding)
        self.create_map()
        self.show()

    def create_map(self):
        """..."""
        from_tileset = self.manager.factory.from_tileset
        size = self.tile_size

        cols = self.width // size
        rows = self.height // size

        for c in range(cols):
            for r in range(rows):
                pos = var = 1
                if r == 0:
                    var = 0
                elif r == rows - 1:
                    var = 2
                if c == 0:
                    pos = 0
                elif c == cols - 1:
                    pos = 2

                sprite = from_tileset(tile="ui_window", pos=pos, var=var,
                                      rect=Rect(c * size + self.x,
                                                r * size + self.y,
                                                size,
                                                size))
                self.tiles.add(sprite)

    def set_padding(self, v):
        """..."""
        size = self.tile_size
        if v:
            self.width += v * 2
            self.height += v * 2

        if self.w % self.tile_size:
            self.w = (self.w // size + 1) * size

        if self.h % self.tile_size:
            self.h = (self.h // size + 1) * size

        self.center = self.default_center

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.tiles)


class Menu(Layer):
    """..."""

    def __init__(
        self, *, parent, title, items=None, background=True,
        font='caladea-regular.ttf'
    ):
        """..."""
        super().__init__(parent=parent)
        self._title = title
        self._items = items
        self.header_color = (200, 14, 24)
        self.unselected_color = (255, 245, 238)
        self.selected_color = (255, 215, 0)
        self.shadow_color = (112, 128, 144)
        self.font = font

        self.selection = 0

        self.create_header()
        if items:
            self.create_items()

        if background:
            self.create_background()
        else:
            self.background = None

        self.select()

    def create_background(self):
        """..."""
        (x, y), (w, h) = self.body_rect.topleft, self.body_rect.size
        r = Rect((x, y), (w, h))
        self.background = Window(
            parent=self, rect=r, padding=32)

    def add_item(self, text):
        """..."""
        self._items.append(text)
        self.create_items()
        self.select()

    def remove_item(self, item):
        """..."""
        if isinstance(item, str):
            index = self._items.index(item)
        else:
            index = item
        self._items.pop(index)
        self.create_items()
        self.select()

    def clear(self):
        """..."""
        del self.item_render
        super().clear()

    def create_header(self):
        """..."""
        manager = self.manager
        fonts = manager.fonts
        font = self.font
        screen_size = manager.width, manager.height
        self.head_font_size = font_size = screen_size[1] // 17
        title = self._title
        color = self.header_color

        x, y = screen_size[0] // 2, screen_size[1] // 5

        head_title_sfc = fonts.render(title, font, font_size, color)
        head_title_obj = head_title_sfc.get_rect()
        head_title_obj.center = x, y
        head_title_sfc.set_rect(head_title_obj)

        head_title_shadow_sfc = fonts.render(title, font, font_size,
                                             self.shadow_color)
        head_title_shadow_obj = head_title_sfc.get_rect()
        head_title_shadow_obj.move_ip(2, 2)
        head_title_shadow_sfc.set_rect(head_title_shadow_obj)

        self.head_title_sfc = head_title_sfc
        self.head_title_obj = head_title_obj
        self.head_title_shadow_sfc = head_title_shadow_sfc
        self.screen_size = screen_size

    def select(self, index=0):
        """..."""
        def replace(i, color):
            shadow, old_sfc = self.item_render[i]
            rect = old_sfc.get_rect()
            del old_sfc
            sfc = fonts.render(items[self.selection], font, font_size,
                               color)
            sfc.set_rect(rect)
            self.item_render[i] = shadow, sfc

        fonts = self.manager.fonts
        font = self.font
        items = self._items
        font_size = self.item_font_size

        replace(self.selection, self.unselected_color)
        self.selection = index
        replace(self.selection, self.selected_color)

    def create_items(self):
        """..."""
        manager = self.manager
        fonts = manager.fonts
        font = self.font
        unselected_color = self.unselected_color
        head_title_obj = self.head_title_obj

        items = self._items
        item_render = []

        self.item_font_size = font_size = int(self.head_font_size // 1.1)
        char_size = fonts.text_size("A", font, font_size)

        for i, item in enumerate(items):

            txt_sfc = fonts.render(item, font, font_size,
                                   unselected_color)
            txt_obj = txt_sfc.get_rect()
            x, y = (
                self.screen_size[0] // 2,
                head_title_obj.bottom + head_title_obj.height * 2 +
                char_size[1] * i
            )
            txt_obj.midtop = x, y
            txt_sfc.set_rect(txt_obj)

            txt_shd_sfc = fonts.render(item, font, font_size,
                                       self.shadow_color)
            txt_shd_obj = txt_sfc.get_rect()
            txt_shd_obj.move_ip(2, 2)
            txt_shd_sfc.set_rect(txt_shd_obj)

            item_render.append((txt_shd_sfc, txt_sfc))

            self.item_render = item_render

    @property
    def body_rect(self):
        """..."""
        rects = [sfc.get_rect() for sfc in roundrobin(*self.item_render)]
        r = rects.pop(0)
        return r.unionall(rects)

    def on_update(self):
        """..."""
        self.background.on_update()

        header = [self.head_title_shadow_sfc, self.head_title_sfc]
        batch = header + list(roundrobin(*self.item_render))
        self.manager.spriterenderer.render(sprites=batch)


class ScrollingSubtitle(Layer):
    """..."""

    def __init__(
        self, parent, subtitles, frame_duration=10, show_gap=False,
        step_x=8
    ):
        """..."""
        super().__init__(parent=parent)

        self.subtitles = subtitles
        self.frame_duration = frame_duration
        self.step_x = step_x

        menu_layer = self.parent.menu_layer
        self.font = 'caladea-italic.ttf'
        self.font_size = menu_layer.item_font_size - 8
        self.color = (200, 107, 24)
        self.sub_i = 0

        self.show_gap = show_gap
        self.set_gap()
        self.render_subtitle(first=True)

    @property
    def current_subtitle(self):
        """..."""
        return self.subtitles[self.sub_i]

    def set_gap(self):
        """..."""
        menu_layer = self.parent.menu_layer

        header_rect = menu_layer.head_title_obj
        items_rect = menu_layer.body_rect
        x = min(header_rect.x, items_rect.x)
        y = header_rect.bottom + 1
        w = max(header_rect.right, items_rect.right) - x
        h = items_rect.y - 1 - y
        self.gap = Rect(x, y, w, h)
        self.wait = time.get_time()

    def render_subtitle(self, first=False):
        """..."""
        render = self.parent.manager.fonts.render

        text = self.current_subtitle
        subtitle = render(text, self.font, self.font_size, self.color)
        rect = subtitle.get_rect()
        area = self.gap
        rect.midright = area.midright
        rect.move_ip(0, -rect.height // 2)
        if first:
            subtitle.position = rect.topleft
            self.def_right = rect.right
        else:
            rect.right = 0
            subtitle.set_rect(rect)

        self.subtitle = subtitle
        self.held = False
        if self.show_gap:
            self.gap_view = self.manager.factory.from_color(
                color=(0, 255, 0, 0), rect=area)
            self.sprites = [self.gap_view, self.subtitle]
        else:
            self.sprites = self.subtitle

    def on_update(self):
        """..."""
        def_right = self.def_right
        r = self.subtitle.get_rect()
        if r.x > self.parent.width:
            self.sub_i += 1
            self.sub_i = self.sub_i % len(self.subtitles)
            self.render_subtitle()
            return
        elif (time.get_delta(self.wait) / 1000) < self.frame_duration:
            return
        elif not self.held and r.right >= def_right:
            self.wait = time.get_time()
            self.held = True
            return
        else:
            r.move_ip(self.step_x, 0)
            self.subtitle.set_rect(r)
        self.manager.spriterenderer.render(sprites=self.sprites)


class Choice(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.title_color = (223, 0, 0)

        self.unselected_color = (192, 192, 192)
        self.set_selected_color()

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["choice"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["choice"]:
            return True
        else:
            return False

    def choice(self, title, items, callback):
        """..."""
        self.set_list(title, items, callback)
        self.active = True

    def change_selection(self, value):
        value += self.selection
        value = value % len(self._items)
        self.select(value)

    def confirm(self):
        self.callback(
            (self.selection, self._items[self.selection])
        )

    def set_list(self, title, items, callback):
        self._title = title
        self._items = items
        self.callback = callback

        self.selection = 0

        self.create_head()
        self.create_items()

        self.select(self.selection)

    def set_selected_color(self):
        self.selected_color = (255, 255, 0)
        return
        selected_color = list(self.unselected_color)
        for i in [0, 1]:
            selected_color[i] = (
                (255 - selected_color[i]) // 2 +
                selected_color[i]
            )
        selected_color[2] = selected_color[2] // 3
        self.selected_color = tuple(selected_color)

    def select(self, index=0):
        old_selection = self.item_render[self.selection][0][0]
        self.color_surface(old_selection, self.unselected_color)

        self.selection = index

        new_selection = self.item_render[self.selection][0][0]
        self.color_surface(new_selection, self.selected_color)

    def color_surface(self, surface, color):
        arr = pygame.surfarray.pixels3d(surface)
        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        del arr

    def create_head(self):
        self.screen_size = screen_size = self.screen.get_size()
        self.head_font_size = head_font_size = screen_size[1] // 17
        self.head_font = self.fonts.load(
            'caladea-regular.ttf', head_font_size)

        x, y = (screen_size[0] // 2, screen_size[1] // 5)

        self.head_title_sfc = self.head_font.render(
            self._title, True, self.title_color)
        self.head_title_obj = self.head_title_sfc.get_rect()
        self.head_title_obj.center = (x, y)

        self.head_title_shadow_sfc = self.head_font.render(
            self._title, True, COLORS["darker_gray"])
        self.head_title_shadow_obj = self.head_title_sfc.get_rect()
        self.head_title_shadow_obj.center = (x + 2, y + 2)

    def create_items(self):
        items = self._items
        item_render = []

        main_font_size = int(self.head_font_size // 1.1)
        self.main_font = self.fonts.load(
            'caladea-regular.ttf', main_font_size)
        main_font_size = self.main_font.size("A")

        for i, item in enumerate(items):

            txt_sfc = self.main_font.render(
                item, True, self.unselected_color)
            txt_obj = txt_sfc.get_rect()
            x, y = (
                self.screen_size[0] // 2,
                self.head_title_obj.bottom + self.head_title_obj.height * 2 +
                main_font_size[1] * i
            )

            txt_obj.midtop = x, y

            txt_shd_sfc = self.main_font.render(
                item, True, COLORS["black"])
            txt_shd_obj = txt_shd_sfc.get_rect()
            txt_shd_obj.midtop = x + 2, y + 2

            item_render.append(
                ((txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)))

            self.item_render = item_render

    def on_update(self):
        self.screen.blit(self.head_title_shadow_sfc,
                         self.head_title_shadow_obj)
        self.screen.blit(self.head_title_sfc, self.head_title_obj)

        for (
            (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj)
        ) in self.item_render:
            self.screen.blit(txt_shd_sfc, txt_shd_obj)
            self.screen.blit(txt_sfc, txt_obj)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        if event.key.keysym.sym == sdl2.SDLK_UP:
            self.gfx.choice.change_selection(-1)
        elif event.key.keysym.sym == sdl2.SDLK_DOWN:
            self.gfx.choice.change_selection(+1)
        elif event.key.keysym.sym == sdl2.SDLK_RETURN:
            self.gfx.choice.confirm()
            self.active = False
            self.gfx.choice.clear()

    def __getstate__(self):
        """..."""
        return None


class Msg(Layer):
    """..."""

    def __init__(self, parent, text=None):
        """..."""
        super().__init__(parent=parent)
        self.sprites = []
        self.text = text
        self.text_rendered = None
        self.font = Font(font_size=self.h // 18, color=(127, 0, 0, 127),
                         renderer=parent.manager.fonts)

    @property
    def text(self):
        """..."""
        return self._text

    @text.setter
    def text(self, text):
        """..."""
        self._text = text
        self.parent.on_update()

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return False
        else:
            return True

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return False
        else:
            return True

    def on_update(self):
        """..."""
        text = self.text

        if text is None:
            return

        if self.text_rendered != text or not self.sprites:

            render = self.font.render

            msg_sfc = render(text)
            msg_obj = msg_sfc.get_rect()
            msg_obj.center = self.center
            msg_sfc.set_rect(msg_obj)

            msg_shadow_sfc = render(text, color=COLORS["gray"])
            msg_shadow_sfc.set_rect(msg_obj.move(2, 2))

            self.sprites = [msg_shadow_sfc, msg_sfc]
            self.text_rendered = text

        if self.sprites:
            self.parent.manager.spriterenderer.render(sprites=self.sprites)


class Inventory(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.offset = 0
        self.inv_render = []

        self.create_fonts()
        self.create_head()
        self.create_main()

    def on_update(self):
        """..."""
        batch = [self.head_surface, self.head_title_shadow_sfc,
                 self.head_title_sfc, self.main_surface]
        batch += list(roundrobin(*self.inv_render))

        self.manager.spriterenderer.render(sprites=batch)

    def click_on(self, pos):
        """..."""
        if self.main_rect.collidepoint(pos):
            for (
                (txt_sfc, txt_obj), (txt_shd_sfc, txt_shd_obj), item
            ) in self.inv_render:
                if (
                    txt_obj.collidepoint(pos) or
                    txt_shd_obj.collidepoint(pos)
                ):
                    if self.mode == 'use':
                        result = item.item.use(
                            user=self.holder, target=self.target)
                        if result != 'used':
                            self.set_inventory(
                                self.holder, self.target, self.mode)
                        return result
                    elif self.mode == 'drop':
                        return item.item.drop(
                            dropper=self.holder)
            self.main_surface.flip_sprite(mode="v")

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        parent = self.parent

        if event.key.keysym.sym == sdl2.SDLK_ESCAPE or event.key.keysym.sym == sdl2.SDLK_i:
            self.clean_inventory()
            parent.state = "playing"
            parent.on_update()
            return True

    def on_mouse_press(self, event):
        """Handle mouse press input."""
        parent = self.parent
        pos = event.pos

        result = self.click_on(pos)
        print("on_mouse_press result:", result)
        if result in ['used', "dropped"]:
            parent.state = "playing"
            self.clean_inventory()
            parent.player.action()
            parent.handle_turn()
            return True
        elif result in ['equipped', 'cancelled']:
            return True

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["inventory"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["inventory"]:
            return True
        else:
            return False

    def create_fonts(self):
        """..."""
        fonts = self.fonts
        color = COLORS["chartreuse"]
        self.head_font = Font(font_size=26, color=color, renderer=fonts)
        self.main_font = Font(font_size=18, color=color, renderer=fonts)

    def create_head(self):
        """..."""
        factory = self.manager.factory
        head_font = self.head_font

        h = self.head_font.height * 2
        w = int(self.w * 0.9)
        x, y = int(self.w * 0.05), int(self.h * 0.05)

        head_rect = head_rect = Rect(x, y, w, h)
        self.head_surface = factory.from_gradient(rect=head_rect)

        head_title_sfc = head_font.render("< Inventory >")
        head_title_obj = head_title_sfc.get_rect()
        head_title_obj.center = head_rect.center
        head_title_sfc.set_rect(head_title_obj)

        head_title_shadow_sfc = head_font.render(
            "< Inventory >", color=COLORS["black"])
        head_title_shadow_sfc.set_rect(head_title_obj.move(2, 2))

        self.head_rect = head_rect
        self.head_title_sfc = head_title_sfc
        self.head_title_shadow_sfc = head_title_shadow_sfc

    def create_main(self):
        """..."""
        factory = self.manager.factory
        head_rect = self.head_rect
        main_font = self.main_font

        w = head_rect.width
        h = int(self.h * 0.7) - head_rect.height - 16

        x = head_rect.x
        y = head_rect.bottom + 8

        main_rect = Rect(x, y, w, h)
        self.main_surface = factory.from_gradient(rect=main_rect)

        main_font_w, main_font_h = main_font.get_size("healing potion potion")
        main_item_h = int(main_font_h * 1.2)
        main_item_w = int(main_font_w * 1.1)
        self.rows = main_rect.height // (main_item_h + 1)
        self.cols = main_rect.width // main_item_w

        total_width = main_item_w * self.cols
        self.tab_x = int(main_rect.width - total_width)

    def create_desc(self):
        """..."""
        pass

    def clean_inventory(self):
        """..."""
        del self.inv_render
        self.inv_render = []
        self.holder = None
        self.target = None

    def set_inventory(self, holder, target=None, mode="use"):
        """..."""
        self.holder = holder
        self.target = target
        self.mode = mode
        self.inventory = self.holder.inventory
        self.inv_render = []
        offset = self.offset
        main_font = self.main_font

        limit = self.rows * self.cols
        for i, item in enumerate(self.inventory[offset:offset + limit]):
            row = i % self.rows
            col = i // self.rows

            if item.equipment:
                if item.equipment.is_equipped:
                    text = "*{} ({})".format(item.name, item.equipment.slot)
                else:
                    text = "{} ({})".format(item.name, item.equipment.slot)
                color = item.color
            else:
                text = item.name + str(i)
                color = None

            txt_sfc = main_font.render(text, color)
            txt_obj = txt_sfc.get_rect()
            txt_obj.left = (
                self.main_rect.left + self.tab_x + self.main_item_w * col)
            txt_obj.top = self.main_rect.top + (self.main_item_h * row) + 12
            txt_sfc.set_rect(txt_obj)

            txt_shd_sfc = main_font.render(text, color=COLORS["black"])
            txt_shd_sfc.set_rect(txt_obj.mode(2, 2))

            self.inv_render.append(txt_shd_sfc, txt_sfc)


class MsgLog(Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        super().__init__(parent=parent)
        self.font = Font(renderer=self.fonts, font_size=20)

        self.line_height = self.font.get_height()

        self.ypos = int(self.bottom - self.line_height * 1.2)
        self.clear()

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing", "inventory"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    def clear(self):
        self._history = []

    def add(self, string, color=None):
        if color is None:
            color = COLORS["desaturated_green"]
        print(string)
        img = self.font.render(string, color)
        self._history.append(img)
        self._history = self._history[-5:]
        # (50, 200, 50)

    @property
    def history(self):
        return reversed(self._history)

    def on_update(self):
        ypos = self.ypos
        line_height = self.line_height

        for line in self.history:
            line.position = (10, ypos)
            ypos -= line_height

        self.manager.spriterenderer.render(sprites=self.history)


class Hud(Layer):
    """..."""

    def __init__(self, *, parent, rect=None):
        """..."""
        super().__init__(parent=parent, rect=rect)
        self.text = " "
        self.font = Font(name='caladea-bold.ttf', font_size=14,
                         renderer=parent.manager.fonts,
                         color=COLORS["desaturated_green"])
        self.def_topright = self.parent.manager.width - 8, 8

        self.previous_text = None
        self.surface = None

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    def on_update(self):
        """..."""
        text = self.text
        if self.previous_text == text and self.surface:
            return

        surface = self.font.render(self.text)
        r = surface.get_rect()
        r.topright = self.def_topright
        surface.set_rect(r)
        self.manager.spriterenderer.render(sprites=surface)

        self.surface = surface
        self.text = text


class Bar(Layer):
    """..."""

    def __init__(self, parent, name, alpha=90):
        """..."""
        self.max_width = 160
        super().__init__(parent=parent, rect=Rect(16, 16, self.max_width, 26))

        self.color_table = LBPercentTable(
            default_to_first=True,
            table=(
                (0, (223, 0, 0, 192)),  # red
                (25, (*COLORS["yellow"][:3], 176)),
                (50, (*COLORS["lime"][:3], 160)),
                (75, (*COLORS["green"][:3], 144))
            )
        )
        self.previous_value = None
        self.previous_max = None

    @property
    def visible(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    @property
    def active(self):
        """..."""
        if self.parent.state in ["playing"]:
            return True
        else:
            return False

    @property
    def bar_width(self):
        """..."""
        return int(self.percent * self.max_width)

    @property
    def percent(self):
        """..."""
        return self.value / self.maximum

    @property
    def value(self):
        """..."""
        return self.parent.player.combat.hit_points_current

    @property
    def maximum(self):
        """..."""
        return self.parent.player.combat.hit_points_total

    def render(self):
        """..."""
        value = self.value
        maximum = self.maximum
        if (self.previous_value == value and self.previous_max == maximum and
                self.surface):
            return

        color = self.color_table.get(self.percent * 100)
        self.width = max(self.bar_width, 1)

        self.surface = self.parent.manager.factory.from_color(
            rect=self, color=color)

        self.previous_value = value
        self.previous_max == maximum

    def on_update(self):
        """..."""
        self.render()
        self.manager.spriterenderer.render(sprites=self.surface)


if __name__ == '__main__':
    from dnf_game.scene_manager.manager import Manager
    from dnf_game.scene_manager.scenes.base_scenes import SceneBase
    m = Manager(scene=SceneBase)
    layer = Layer(parent=m._scene)
    layer.topleft
