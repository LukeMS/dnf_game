"""..."""

import random

from dnf_game.data.constants import TILE_W, TILE_H
from dnf_game.util import Position
from dnf_game.util.ext.rect import Rect
from dnf_game.dnf_main.components import (
    ai, ArmorComponent, ItemComponent, FeatureComponent, WeaponComponent)
from dnf_game.dnf_main.components.combat import char_roll, creatures
from dnf_game.dnf_main.data_handler.template_handler import TemplateableObject
from dnf_game.dnf_main.data_handler import get_color


class MapEntityAbstract(TemplateableObject):
    """Generic map entity, supposed to be inherited by specific."""

    id = None
    color = None
    name = None
    active = True
    block_mov = False
    block_sight = False
    ai = None
    item = None
    combat = None
    dng_feat = None
    equipment = None
    test = False
    _sprite = None
    tiling_index = None
    tile_variation = None

    def __init__(self, *, name, scene, pos, **kwargs):
        """..."""
        [setattr(v, 'owner', self) for v in kwargs.values()
         if hasattr(v, 'owner')]
        self.name = name
        self.set_template(name)
        self.__dict__.update(kwargs)
        self._rect = Rect(pos, (TILE_W, TILE_H))
        self.scene = scene
        self.default_ai = self.ai
        self.default_color = self.color
        if self.scene:
            self.scene.add_obj(
                obj=self, pos=pos)

    @property
    def rect(self):
        """..."""
        return self._rect

    @property
    def pos(self):
        """..."""
        return Position((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, value):
        """..."""
        self.rect.topleft = value

    @property
    def size(self):
        """..."""
        return self.rect.size

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

    @property
    def left(self):
        """..."""
        return self.rect.left

    @property
    def right(self):
        """..."""
        return self.rect.right

    @property
    def top(self):
        """..."""
        return self.rect.top

    @property
    def bottom(self):
        """..."""
        return self.rect.bottom

    @property
    def topleft(self):
        """..."""
        return self.rect.topleft

    @property
    def current_level(self):
        """..."""
        return self.scene.current_level

    @property
    def visible(self):
        """..."""
        return self.current_level[self.pos].feature.visible

    @property
    def sprite(self):
        """..."""
        if self._sprite is None:
            self._sprite = self.scene.manager.factory.from_tileset(
                tile=self.name,
                pos=self.tiling_index,
                var=self.tile_variation,
                _id=self.id,
                color=self.color)
            self._sprite.__parent = self
        return self._sprite

    def __getstate__(self):
        """Replace __dict__ with the return value when picked."""
        return {k: v
                for k, v in self.__dict__.items()
                if k not in ['scene', '_sprite']}

    def clicked(self):
        """..."""
        return (pygame.mouse.get_pressed()[0] and
                self.rect.collidepoint(pygame.mouse.get_pos()))

    @property
    def next_to_vis(self):
        """..."""
        return any(self.current_level[pos].feature.visible
                   for pos in self.current_level.get_neighbors(self.pos))

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


class TileEntity(MapEntityAbstract):
    """A tile of the map and its properties."""

    tile_variation = 0
    tiling_index = 0
    max_var = 0
    visible = False
    explored = False

    def set_template(self, name):
        """..."""
        templates = self.get_templates(name=name)
        template = templates[self.__class__.__name__]
        self.__dict__.update(template)

    def change_feature(self, *, pos=None, template=None):
        """..."""
        if pos:
            self._rect = Rect((pos), (TILE_W, TILE_H))
        if template:
            self.name = template
            self.set_template(template)

    def __str__(self):
        """..."""
        return chr(self.id)


class DungeonObjectsAbstract(MapEntityAbstract):
    """..."""

    def set_template(self, name):
        """..."""
        templates = self.get_templates(name=name)
        if "ItemComponent" not in templates:
            templates["ItemComponent"] = {"name": name}
        try:
            for cmp_type, temp in templates.items():
                if cmp_type == "FeatureComponent":
                    self.dng_feat = FeatureComponent(temp, owner=self)
                elif cmp_type == "WeaponComponent":
                    self.equipment = WeaponComponent(temp, owner=self)
                elif cmp_type == "ArmorComponent":
                    self.equipment = ArmorComponent(temp, owner=self)
                elif cmp_type == "ItemComponent":
                    self.item = ItemComponent(temp, owner=self)
                [setattr(self, field, temp[field])
                 for field in ['id', 'color']
                 if field in temp]
        except ValueError:
            from pprint import pprint
            pprint(templates, indent=4)
            raise


class FeatureEntity(DungeonObjectsAbstract):
    """..."""

    pass


class ItemEntity(DungeonObjectsAbstract):
    """..."""

    def update(self):
        """..."""
        if self.visible:
            super().update()


class CreatureEntityAbstract(MapEntityAbstract):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        self.inventory = []
        super().__init__(**kwargs)
        self.id = ord(self.name[0])

    def set_template(self, *args, **kwargs):
        """Not applicable to creatures."""
        pass

    def move(self, pos=None):
        """..."""
        self.scene.rem_obj(self, self.pos)

        status = None

        if pos and not self.current_level.is_blocked(pos, self) \
                and not self.current_level.is_occupied(pos):
            self.pos = pos
            status = True

        self.scene.add_obj(self, self.pos)

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
            path = self.current_level.a_star_pathfinder(
                start_pos, end_pos)
            next_step = Position(path[1])
            if self.move(next_step):
                return path
            else:
                return None
        except KeyError:
            # print("the path must be blocked")
            return self.move_rnd()

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
                str(self.combat.level) + '!', get_color("cyan"))
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
            get_color("cyan"))


class PCreature(CreatureEntityAbstract):
    """Playable creature."""

    def __init__(self, **kwargs):
        """..."""
        combat = kwargs.pop("combat", None)
        if combat is None:
            race = kwargs.pop("race", None)
            _class = kwargs.pop('_class', None)
            combat = creatures.Character(race=race, _class=_class, owner=self)
        self.combat = combat

        self.color = get_color("yellow")
        super().__init__(name=combat.name, **kwargs)

    def set_starting_position(self, pos, header):
        """..."""
        try:
            self.scene.rem_obj(self, self.pos)
        except ValueError:
            print("Failed to remove player...")
        self.pos = pos
        self.last_map = header
        self.scene.add_obj(self, self.pos)

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
        """..."""
        old_pos = self.pos
        old_offset = self.scene.level_layer.offset
        status = super().move(pos)
        self.scene.set_offset(self)
        """
        """
        new_pos = self.pos
        new_offset = self.scene.level_layer.offset
        print("Player moving: {}->{}, offset: {}->{}".format(
            old_pos, new_pos, old_offset, new_offset))
        return status


class NPCreature(CreatureEntityAbstract):
    """Non-playable creature."""

    path = None

    def __init__(self, name, **kwargs):
        """..."""
        self.combat = creatures.Beast(model=name, owner=self)
        self.color = get_color('blood_red')
        self.ai = ai.Basic(owner=self)
        super().__init__(name=self.combat.name, **kwargs)

    def update(self):
        """..."""
        if self.visible:
            super().update()

    def update_hp(self):
        """..."""
        pass


class Cursor(MapEntityAbstract):
    """..."""

    def __init__(self, scene):
        """..."""
        super().__init__(scene=scene, pos=(0, 0), id=None, color=None,
                         name='cursor')

    def set_template(self, *args, **kwargs):
        """Not applicable to a cursor."""
        pass

    def move(self, pos, rel_pos):
        """..."""
        self.pos = rel_pos
        return self.cursor_collision()

    def cursor_collision(self):
        """..."""
        # TODO: redo this thing
        for _type in ['creatures', 'objects', 'feature']:
            targets = self.scene.get_obj(_type, self.pos)
            targets = [targets] if _type == 'feature' else targets
            for target in targets:
                if target and target.visible:
                    return target
