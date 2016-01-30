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

    def contain_pos(self, pos):
        for sprite in self.__iter__():
            xy = (sprite.rect.x, sprite.rect.y)
            if pos == xy:
                return True
        return False


class GameObject:
    # (pygame.sprite.Sprite)
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.

    def __init__(
        self, scene, x, y, id, color,
        name=None, blocks=True, combat=None, ai=None, item=None, active=True,
        dng_feat=None, equipment=None, test=False,
        **kwargs
    ):
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
            value = eval(arg)

            # component initialization
            if hasattr(value, 'owner'):  # if it is a component
                value.owner = self  # set its owner

            setattr(self, arg, value)
        #

        self.default_ai = self.ai
        self.default_color = self.color

    @property
    def visible(self):
        return self.scene.grid[self.pos].visible

    def __getstate__(self):
        d = dict(self.__dict__)
        for key in ['scene']:
            if key in d:
                del d[key]
        return d

    def is_clicked(self):
        return (
            pygame.mouse.get_pressed()[0]
            and self.rect.collidepoint(pygame.mouse.get_pos()))

    # next to a visible tile
    def set_next_to_vis(self):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                n = self.pos + (x, y)
                if self.scene.grid[n].visible:
                    self.next_to_vis = True
                    return
        self.next_to_vis = False

    @property
    def pos(self):
        return Position((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, value):
        if isinstance(value, tuple):
            self.rect.x, self.rect.y = value
        else:
            self.rect.x, self.rect.y = value.x, value.y

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    def __floordiv__(self, n):
        if isinstance(n, tuple):
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x // n), int(self.y // n))

    def move(self, pos=None):
        if self.name != 'cursor':
            self.scene.rem_obj(self, 'creatures', self.pos)

        status = None

        if pos is not None and not self.scene.map_mgr.is_blocked(pos, self):
            self.pos = pos
            self.set_next_to_vis()
            status = True

        if self.name != 'cursor':
            self.scene.add_obj(self, 'creatures', self.pos)

        return status

    def move_rnd(self):
        start_pos = self.pos
        next_step = random.choice(self.scene.map_mgr.get_neighbors(start_pos))
        return self.move(next_step)

    def move_towards(self, target):
        start_pos = self.pos
        end_pos = target.pos

        try:
            path = self.scene.map_mgr.a_path(
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
        if pos2 is None:
            pos2 = self.pos
        return self.scene.map_mgr.distance(pos1.pos, pos2)

    def update(self):
        self.scene.gfx.draw(
            self.id,
            (
                self.rect.x - self.scene.offset[0],
                self.rect.y - self.scene.offset[1]
            ),
            color=self.color)

    def gain_xp(self, value):
        """First, select your new class level. You must be able to qualify for
        this level before any of the following adjustments are made. Second,
        apply any ability score increases due to gaining a level. Third,
        integrate all of the level's class abilities and then roll for
        additional hit points. Finally, add new skills and feats."""

        def gain_ability():
            self.scene.gfx.msg_log.add(
                'Your battle skills grow stronger! You reached level ' +
                str(self.combat.level) + '!', GAME_COLORS["cyan"])
            self.scene.choice(
                title='Level up! Choose a stat to raise:',
                items=[
                    'Constitution, +10 HP (current: {})'.format(
                        self.combat.max_hp),
                    'Strength, +1 attack (current: {})'.format(
                        self.combat.base_power),
                    'Agility, +1 defense (current: {})'.format(
                        self.combat.base_defense)
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

        # see if the creature's experience is enough to level-up
        """CHANGE XP CALC. """
        level = self.combat.level
        xp = self.combat.xp
        if xp >= char_roll.level_adv[level][0]:
            # it is! level up
            self.combat.level += 1

            if not self.combat.level % 4:
                gain_ability()

            if self.combat.level % 2:
                gain_feat()

    def increase_stat(self, choice):
        id, desc = choice

        if id == 0:
            self.combat.base_max_hp += 10
            self.update_hp()

        elif id == 1:
            self.combat.base_power += 1

        elif id == 2:
            self.combat.base_defense += 1

        else:
            raise AttributeError
        self.scene.gfx.msg_log.add(
            desc.replace("current", "previous"),
            GAME_COLORS["cyan"])


class NPC(GameObject):

    path = None

    def __init__(self, template, **kwargs):

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
        if self.scene.grid[self.pos].visible:
            super().update()

    def update_hp(self):
        pass


class Player(GameObject):

    def __init__(
            self, id=ord('@'), color=GAME_COLORS["yellow"], **kwargs):

        kwargs['combat'] = creatures.Character()

        super().__init__(
            id=id, color=color, **kwargs)
        self.scene.add_obj(self, 'creatures', self.pos)
        self.inventory = []
        self.scene.gfx.hp_bar.set_value(self.combat.hit_points_current,
                                        self.combat.hit_points_total)

    def update_hp(self):
        # max_hp
        self.scene.gfx.hp_bar.set_value(self.combat.hit_points_current,
                                        self.combat.hit_points_total)

    def action(self, dx=0, dy=0, action='std', key=None):
        pos = self.pos + (dx, dy)
        if action is 'std':
            if not (dx == 0 == dy):
                # the coordinates the player is moving to/attacking

                # try to find an attackable object there
                target = self.scene.get_obj('creatures', pos)

                if target is not None and target.combat:
                    self.combat.attack(target)
                else:
                    if self.move(pos):
                        self.scene.map_mgr.set_fov()
        elif action is 'get':
            target = self.scene.get_obj('objects', pos)
            if target is not None and target.item:
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


class DngFeature(GameObject):
    templates = {
        'stair_up': {
            'id': "<",
            'color': GAME_COLORS["gray"],
            'blocks': False
        },
        'stair_down': {
            'id': "<",
            'color': GAME_COLORS["gray"],
            'blocks': False
        }
    }

    def __init__(self, template, **kwargs):
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)
        if template in obj_components.DngFeat.templates:
            new_obj['dng_feat'] = obj_components.DngFeat(template)
        super().__init__(
            **new_obj, name=str(template).capitalize())
        self.scene.add_obj(self, 'objects', self.pos)


class Item(GameObject):

    def __init__(self, template, test=False, **kwargs):
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
        if self.scene.grid[self.pos].visible:
            super().update()

    @classmethod
    def test(cls):
        def dummy(*args, **kwargs):
            pass

        class Dummy:
            pass

        class Owner:
            inventory = []

            scene = Dummy()
            scene.rem_obj = dummy

            scene.gfx = Dummy()
            scene.gfx.msg_log = Dummy()
            scene.gfx.msg_log.add = print

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

    def __init__(self, scene):
        super().__init__(
            scene=scene, x=1, y=1, id=None, color=None,
            name='cursor')

    def move(self, pos, rel_pos):
        self.pos = rel_pos
        return self.cursor_collision()

    def cursor_collision(self):
        for _type in ['creatures', 'objects', 'feature']:
            target = self.scene.get_obj(_type, self.pos)
            if target and target.visible:
                return target

if __name__ == '__main__':
    Item.test()
