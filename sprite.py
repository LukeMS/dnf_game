"""..."""

# import traceback  # print(traceback.format_exc())
import random

import pygame
from constants import TILE_W, TILE_H, GAME_COLORS

from game_types import Position
import obj_components
import ai_comp

from combat import creatures
from combat import char_roll


class Group(pygame.sprite.Group):
    """..."""

    def contain_pos(self, pos):
        """..."""
        for sprite in self.__iter__():
            xy = (sprite.rect.x, sprite.rect.y)
            if pos == xy:
                return True
        return False


class GameObject:
    """..."""

    # (pygame.sprite.Sprite)
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.

    def __init__(
            self, scene, x, y, id, color, name=None, blocks=True,
            combat=None, ai=None, item=None, active=True,
            dng_feat=None, equipment=None, test=False, **kwargs
    ):
        """..."""
        if not test:
            super().__init__()

        # some preliminar preparation
            self.rect = pygame.Rect(x, y, TILE_W, TILE_H)
        #
        if test:
            args = ["id", "color", "name", "blocks", "combat", "ai", "item",
                    "equipment", "dng_feat", "active"]
        else:
            args = [
                "scene", "x", "y", "id", "color", "name", "blocks",
                "combat", "ai", "item", "equipment", "dng_feat", "active"
            ]
        # unpack the arguments and store them in the instance
        for arg in args:
            value = locals()[arg]

            # component initialization
            if hasattr(value, 'owner'):  # if it is a component
                value.owner = self  # set its owner

            setattr(self, arg, value)
        #

        self.default_ai = self.ai
        self.default_color = self.color

    @property
    def get_rect(self):
        """..."""
        return tuple((self.x, self.y, TILE_W, TILE_H))

    @property
    def current_level(self):
        """..."""
        return self.scene.current_level

    @property
    def visible(self):
        """..."""
        return self.current_level[self.pos].feature.visible

    def __getstate__(self):
        """..."""
        d = dict(self.__dict__)
        for key in ['scene']:
            if key in d:
                del d[key]
        return d

    def is_clicked(self):
        """..."""
        return (pygame.mouse.get_pressed()[0] and
                self.rect.collidepoint(pygame.mouse.get_pos()))

    @property
    def next_to_vis(self):
        """..."""
        return any(self.current_level[pos].feature.visible
                   for pos in self.current_level.get_neighbors(self.pos))

    @property
    def pos(self):
        """..."""
        return Position((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, value):
        """..."""
        if isinstance(value, tuple):
            self.rect.x, self.rect.y = value
        else:
            self.rect.x, self.rect.y = value.x, value.y

    @property
    def x(self):
        """..."""
        return self.rect.x

    @x.setter
    def x(self, value):
        """..."""
        self.rect.x = value

    @property
    def y(self):
        """..."""
        return self.rect.y

    @y.setter
    def y(self, value):
        """..."""
        self.rect.y = value

    def __floordiv__(self, n):
        """..."""
        if isinstance(n, tuple):
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x // n), int(self.y // n))

    def move(self, pos=None):
        """..."""
        if self.name != 'cursor':
            self.scene.rem_obj(self, 'creatures', self.pos)

        status = None

        if pos and not self.current_level.is_blocked(pos, self) \
                and not self.current_level.is_occupied(pos):
            self.pos = pos
            status = True

        if self.name != 'cursor':
            self.scene.add_obj(self, 'creatures', self.pos)

        return status

    def move_rnd(self):
        """..."""
        start_pos = self.pos
        next_step = random.choice(self.current_level.get_neighbors(start_pos))
        return self.move(next_step)

    def move_towards(self, target):
        """..."""
        start_pos = self.pos
        end_pos = target.pos

        try:
            path = self.current_level.a_path(
                start_pos, end_pos)
            next_step = Position(path[1])
            if self.move(next_step):
                return path
            else:
                return None
        except KeyError:
            # print("the path must be blocked")
            return self.move_rnd()

    def distance_to(self, pos1, pos2=None):
        """..."""
        if pos2 is None:
            pos2 = self.pos
        return self.current_level.distance(pos1.pos, pos2)

    def update(self):
        """..."""
        self.scene.gfx.draw(
            self.id, (self.rect.x - self.scene.offset[0],
                      self.rect.y - self.scene.offset[1]),
            color=self.color)

    def gain_xp(self, value):
        """First, select your new class level. You must be able to qualify for
        this level before any of the following adjustments are made. Second,
        apply any ability score increases due to gaining a level. Third,
        integrate all of the level's class abilities and then roll for
        additional hit points. Finally, add new skills and feats.
        Humans gain 1 additional skill rank per class level.
        Characters who take a level in a favored class have the option of
        gaining 1 additional skill rank or an additional hit point . If you
        select a level in a new class, all of its class skills are
        automatically added to your list of class skills, and you gain a +3
        bonus on these skills if you have ranks in them.
        """

        def gain_ability():
            self.scene.gfx.msg_log.add(
                'Your battle skills grow stronger! You reached level ' +
                str(self.combat.level) + '!', GAME_COLORS["cyan"])
            self.scene.parent.choice(
                title='Level up! Choose a stat to raise:',
                items=[
                    'Strength (current: {})'.format(
                        self.combat._base_att[0]),
                    'Dexterity (current: {})'.format(
                        self.combat._base_att[1]),
                    'Constitution (current: {})'.format(
                        self.combat._base_att[2])
                ],
                callback=self.increase_stat
            )
        self.combat.xp += value

        def set_level_changes():
            # unlock abilitie
            # calc hit dice
            pass

        def gain_feat():
            pass

        def gain_skill():
            pass

        # see if the creature's experience is enough to level-up
        """CHANGE XP CALC. """
        while True:
            if self.combat.xp >= char_roll.level_adv[self.combat.level][0]:
                # it is! level up
                self.combat.level += 1

                if not self.combat.level % 4:
                    gain_ability()

                if self.combat.level % 2:
                    gain_feat()
                continue
            break

    def increase_stat(self, choice):
        """..."""
        id, desc = choice

        self.combat._base_att[id] += 1
        self.update_hp()

        self.scene.gfx.msg_log.add(
            desc.replace("current", "previous"),
            GAME_COLORS["cyan"])


class NPC(GameObject):
    """..."""

    path = None

    def __init__(self, template, **kwargs):
        """..."""
        kwargs['combat'] = creatures.Beast(model=template)
        kwargs['name'] = kwargs['combat'].name
        kwargs['ai'] = ai_comp.Basic()

        super().__init__(
            color=GAME_COLORS['blood_red'],
            id=ord("@"),
            **kwargs)
        self.scene.add_obj(self, 'creatures', self.pos)

        self.inventory = []

    def update(self):
        """..."""
        if self.visible:
            super().update()

    def update_hp(self):
        """..."""
        pass


class Player(GameObject):
    """..."""

    def __init__(self, id=ord('@'), color=GAME_COLORS["yellow"], **kwargs):
        """..."""
        if 'combat' not in kwargs or kwargs['combat'] is None:
            race = kwargs['race'] if 'race' in kwargs else None
            _class = kwargs['_class'] if '_class' in kwargs else None

            kwargs['combat'] = creatures.Character(race=race, _class=_class)

        super().__init__(
            id=id, color=color, **kwargs)
        self.inventory = []

    def set_starting_position(self, pos, header):
        """..."""
        try:
            self.scene.rem_obj(self, 'creatures', self.pos)
        except ValueError as v:
            print(v, "while attempting to remove player.")
        self.pos = pos
        self.last_map = header
        self.scene.add_obj(self, 'creatures', self.pos)

    def update_hp(self):
        """..."""
        # max_hp
        self.scene.hp_bar.refresh()

    def action(self, dx=0, dy=0, action='std', key=None):
        """..."""
        pos = self.pos + (dx, dy)
        if action is 'std':
            if any((dx, dy)):
                # player is moving to/attacking a direction
                # try to find an attackable object there
                creatures = self.scene.get_obj('creatures', pos)
                if creatures:
                    target = random.choice(creatures)
                    if target and target.combat:
                        self.combat.attack(target)
                else:
                    if self.move(pos):
                        self.scene.set_fov()
        elif action is 'get':
            for target in self.current_level[pos].objects:
                if target and target.item:
                    if target.item.pick_up(getter=self):
                        self.active = False
                        return True
            return False
        elif action is 'use':
            target = self.scene.get_obj('objects', pos)
            if target is not None and target.dng_feat:
                if target.dng_feat.use(who=self):
                    self.active = False
                    return True
            return False

        self.active = False
        return True

    def move(self, pos=None):
        old_pos = self.pos
        old_offset = self.scene.level_layer.offset
        status = super().move(pos)
        self.scene.set_offset(self)
        new_pos = self.pos
        new_offset = self.scene.level_layer.offset
        print("Player moving: {}->{}, offset: {}->{}".format(
            old_pos, new_pos, old_offset, new_offset))
        return status


class DngFeature(GameObject):
    """..."""
    templates = {
        'stair_up': {
            'id': "<",
            'color': GAME_COLORS["gray"],
            'blocks': False
        },
        'stair_down': {
            'id': ">",
            'color': GAME_COLORS["gray"],
            'blocks': False
        }
    }

    def __init__(self, template, **kwargs):
        """..."""
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)
        if template in obj_components.DngFeat.templates:
            new_obj['dng_feat'] = obj_components.DngFeat(template)
        super().__init__(
            **new_obj, name=str(template).capitalize())
        self.scene.add_obj(self, 'objects', self.pos)


class Item(GameObject):
    """..."""

    def __init__(self, template, test=False, **kwargs):
        """..."""
        for component in obj_components.TemplateHandler.get(template):
            # item = Item(template),
            # equipment = Weapon(template),
            # etc.
            kwargs[component['name']] = component['type'](template)
            for field in ['id', 'color', 'name']:
                try:

                    # kwargs["color"] = weapon.color
                    # etc.
                    kwargs[field] = getattr(kwargs[component['name']], field)
                except:
                    # it doesn't have that field defined
                    pass
        # print(kwargs)

        super().__init__(**kwargs, blocks=False, test=test)
        if not test:
            self.scene.add_obj(self, 'objects', self.pos)

    def update(self):
        """..."""
        if self.visible:
            super().update()

    @classmethod
    def test(cls):
        """..."""
        owner = Owner()

        item1 = Item("aklys", test=True, x=0, y=0, scene=None)
        item1.rect = Dummy()
        item1.rect.x = 0
        item1.rect.y = 0
        item1.owner = owner
        item1.scene = owner.scene
        item1.item.pick_up(owner)
        item1.item.use(owner)
        item1.item.use(owner)
        item1.item.use(owner)

        item2 = Item("falchion", test=True, x=0, y=0, scene=None)
        item2.rect = Dummy()
        item2.rect.x = 0
        item2.rect.y = 0
        item2.owner = owner
        item2.scene = owner.scene
        item2.item.pick_up(owner)
        item2.item.use(owner)

        item1.item.use(owner)


class Cursor(GameObject):
    """..."""

    def __init__(self, scene):
        """..."""
        super().__init__(
            scene=scene, x=1, y=1, id=None, color=None,
            name='cursor')

    def move(self, pos, rel_pos):
        """..."""
        self.pos = rel_pos
        return self.cursor_collision()

    def cursor_collision(self):
        """..."""
        for _type in ['creatures', 'objects', 'feature']:
            targets = self.scene.get_obj(_type, self.pos)
            targets = [targets] if _type == 'feature' else targets
            for target in targets:
                if target and target.visible:
                    return target

if __name__ == '__main__':
    Item.test()
