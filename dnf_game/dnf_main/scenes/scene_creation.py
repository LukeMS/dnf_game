"""..."""

import os

import sdl2

from dnf_game.dnf_main.components.combat import char_roll, creatures
from dnf_game.util import get_mod_case, packer, dnf_path
from dnf_game.util.ext.rect import Rect
from dnf_game.scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_game.scene_manager.layers.base_layers import Layer
from dnf_game.util.sftext import SFText


class SceneCreation(SceneMultiLayer):
    """..."""

    def __init__(self, *, target=None, **kwargs):
        """Initialization.

        Parameters:
            target: scene to deliver the character to after creation;
        """
        super().__init__(draw_all=True)

        self.target = target

        self.create_layers()
        print("here")

    def create_layers(self):
        """..."""
        bg = Layer(parent=self)
        bg.create_gradient_surface(color_start=(0, 0, 0, 0),
                                   color_end=(0, 31, 0, 0),
                                   mode="h")
        stats_rect = Rect(
            0,  # left
            0,  # top
            int(self.width * 0.30),  # width
            self.height)  # height

        desc_rect = Rect(
            stats_rect.right,  # left
            0,  # top
            self.width - stats_rect.width,  # width
            self.height)  # height
        self.desc_layer = Description(parent=self, rect=desc_rect)
        self.stats_layer = Stats(parent=self, rect=stats_rect)
        self.insert_layer(bg, self.desc_layer, self.stats_layer)

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()
        elif sym in [sdl2.SDLK_RETURN, sdl2.SDLK_KP_ENTER]:
            if self.target:
                self.manager.set_scene(
                    **self.target, character=self.stats_layer.character)
            else:
                self.quit()
        elif sym in [sdl2.SDLK_PAGEUP, sdl2.SDLK_PAGEDOWN,
                     sdl2.SDLK_HOME, sdl2.SDLK_END]:
            self.desc_layer.on_key_press(event, mod)
        else:
            self.stats_layer.on_key_press(event, mod)

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        self.desc_layer.on_mouse_scroll(event, offset_x, offset_y)


class Stats(Layer):
    """..."""
    bottom_color = (15, 15, 31)
    top_color = (0, 0, 0)

    def __init__(self, parent, rect):
        """..."""
        super().__init__(rect=rect)
        self.character = creatures.Character()
        self.create_structure()
        self.create_text()

    def create_structure(self):
        """..."""
        self.selection = 0

        self.att_names = char_roll.att_names
        self.fields = ['name', 'gender', 'race', 'class',
                       'alignment', 'age', 'height', 'weight']
        self.fields.extend(self.att_names)

    def change_selection(self, value):
        """..."""
        selection = self.selection + value
        selection = selection % len(self.fields)
        self.selection = selection
        self.create_text()
        # print(self.fields[selection])

        if selection > 7:
            group = 'stats'
            key = self.fields[selection]
        elif selection == 2:
            group = 'races'
            key = self.character.race
        elif selection == 3:
            group = 'classes'
            key = self.character._class
        elif selection == 4:
            group = 'alignment'
            key = '*'
        else:
            self.desc_layer.create_text()
            return

        self.desc_layer.create_text(group=group, key=key)

    def change_value(self, v):
        """Handle the change if the player attemp to modify a field.

        Age, Height and Weight can't be changed.
        """
        selection = self.selection

        if selection == 0:
            self.character.change_name()
        elif selection == 1:
            self.character.change_gender()
            self.character.change_height_weight()
        elif selection == 2:
            self.character.change_race(v)
        elif selection == 3:
            self.character.change_class(v)
        elif selection == 4:
            self.character.change_alignment(v)
        elif selection > 7:
            self.change_stats(v)
        else:
            return

        self.create_text()
        self.change_selection(0)

    def change_stats(self, v):
        """Swap attributes."""
        i0 = (self.selection - 8) % 6
        i1 = (self.selection + v - 8) % 6
        att = self.character._base_att
        att[i0], att[i1] = att[i1], att[i0]

    @property
    def desc_layer(self):
        return self.parent.desc_layer

    @property
    def available_alignments(self):
        return char_roll.alignments[self.character._class]

    @property
    def available_classes(self):
        return sorted(self.character.classes)

    @property
    def current_alignment_i(self):
        return self.available_alignments.index(self.character.alignment)

    @property
    def current_class_i(self):
        return self.available_classes.index(self.character._class)

    def create_text(self):
        """..."""
        def fancy_field(string):
            return string[:1].upper() + string[1:]

        def name():
            if self.selection == 0:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Name:" + ul + c + "{style}" +
                    " {}".format(self.character.name) +
                    "\n\n")

        def gender():
            if self.selection == 1:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Gender:" + ul + c + "{style}" +
                    " {}".format(fancy_field(self.character.gender)) +
                    "\n\n")

        def race():
            if self.selection == 2:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Race:" + ul + c + "{style}" +
                    " {}".format(fancy_field(self.character.race)) +
                    "\n\n")

        def _class():
            if self.selection == 3:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Class:" + ul + c + "{style}" +
                    " {}".format(fancy_field(self.character._class)) +
                    "\n\n")

        def alignment():
            if self.selection == 4:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Alignment:" + ul + c + "{style}" +
                    " {}".format(self.character.alignment) +
                    "\n\n")

        def age():
            if self.selection == 5:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Age:" + ul + c + "{style}" +
                    " {}".format(str(self.character.age)) +
                    "\n\n")

        def height():
            if self.selection == 6:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Height:" + ul + c + "{style}" +
                    " {:.2f}".format(self.character.height, 2) + 'm.' +
                    "\n\n")

        def weight():
            if self.selection == 7:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""
            return ("Weight:" + ul + c + "{style}" +
                    " {:.2f}".format(self.character.weight, 2) + 'kg.' +
                    "\n\n")

        def att(i):
            character = self.character
            if self.selection == 8 + i:
                ul = "{underline True}"
                c = "{color (255, 255, 0)}"
            else:
                ul = ""
                c = ""

            v = self.character.attributes[i]
            if v > 11:
                c2 = "{color (0, 255, 0)}"
            elif v < 10:
                c2 = "{color (255, 0, 0)}"
            else:
                c2 = ""
            bonus = ""
            if character.race_mod[i]:
                if character.race_mod[i] > 0:
                    bonus = "+{}={}".format(character.race_mod[i], v)
                else:
                    bonus = "{}={}".format(character.race_mod[i], v)

            return ("{}:".format(fancy_field(self.att_names[i])) +
                    ul + c + "{style}" +
                    " {}{}".format(character._base_att[i], bonus) + c2 +
                    "\n\n")

        mystyle = {'size': 18, 'color': (223, 223, 255)}

        text = ''.join(
            [t for t in [
                "\n",
                name(), gender(), race(), _class(), alignment(), age(),
                height(), weight(), ''.join(
                    [att(i) for i in range(len(self.att_names))])]])
        manager = self.manager

        self.sftext = SFText(text=text, style=mystyle, rect=self,
                             fonts=manager.fonts, manager=manager)

    def on_update(self):
        """..."""
        super().on_update()
        self.sftext.on_update()

    def post_update(self):
        """..."""
        # self.sftext.post_update()
        pass

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        sym = event.key.keysym.sym
        if sym == sdl2.SDLK_UP:
            self.change_selection(-1)
            return
        elif sym == sdl2.SDLK_DOWN:
            self.change_selection(+1)
            return
        elif sym == sdl2.SDLK_LEFT:
            self.change_value(-1)
            return
        elif sym == sdl2.SDLK_RIGHT:
            self.change_value(+1)
            return
        elif sym == sdl2.SDLK_F2:
            self.character = creatures.Character()

        if self.selection is 0:
            if sym == sdl2.SDLK_BACKSPACE:
                self.character.name = self.character.name[:-1]
            elif 97 <= sym <= 122:
                input_text = get_mod_case(event)
                self.character.name += input_text

        self.create_text()
        self.change_selection(0)


class Description(Layer):
    """..."""

    bottom_color = (31, 15, 15)
    top_color = (0, 0, 0)

    def __init__(self, parent, rect):
        """..."""
        super().__init__(rect=rect)
        fname = os.path.join(dnf_path(), 'data', 'descriptions.bzp')
        self.db = packer.unpack_json(fname)
        # self.create_solid_surface(color=(31, 0, 63))
        self.create_text()

    def selection(self):
        return

    def create_text(self, group=None, key="character creation"):
        if group:
            text = self.db[group][key]
        else:
            text = self.db[key]

        try:
            old_text = self.sftext.text
        except AttributeError:
            old_text = None

        if old_text != text:
            manager = self.manager
            self.sftext = SFText(text=text, rect=self,
                                 fonts=manager.fonts, manager=manager)

    def on_update(self):
        """..."""
        super().on_update()
        self.sftext.on_update()

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        self.sftext.on_key_press(event, mod)

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        self.sftext.on_mouse_scroll(event, offset_x, offset_y)
