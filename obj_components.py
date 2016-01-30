from constants import GAME_COLORS
import effects
from data.equipment.weapons import weapons_db
from data.equipment.items import items_db


class Component:

    owner = None
    _base = {}
    templates = {}

    def __init__(self, template, test=False):
        component = dict(self._base)
        component.update(self.templates[template])
        for key, value in component.items():
            setattr(self, key, value)
        if test:
            from pprint import pprint
            pprint(component)

    @classmethod
    def test(cls):
        from mylib.data_tree import tk_tree_view
        tk_tree_view(cls.templates)


class Item(Component):

    var_name = "item"
    possessor = None
    use_function = None

    templates = items_db.keys()

    def __init__(self, template):
        try:
            component = items_db[template]
            self.__dict__.update(component)
            self.name = template.capitalize()
        except KeyError:
            # no usable functions or item definitions for this item
            pass

    def pick_up(self, getter):
        scene = self.owner.scene
        msg_log = self.owner.scene.gfx.msg_log

        # add to the player's inventory and remove from the map
        if len(getter.inventory) >= 26:
            if getter == self.owner.scene.player:
                self.owner.scene.gfx.msg_log.add(
                    'Your inventory is full, cannot pick up ' +
                    self.owner.name + '.', GAME_COLORS["yellow"])
        else:
            scene.rem_obj(self.owner, 'objects', self.owner.pos)

            getter.inventory.append(self.owner)
            self.possessor = getter

            msg_log.add(
                'You picked up a ' + self.owner.name + '!',
                GAME_COLORS["blue"])

    def drop(self, dropper):
        """Add to the map and remove from the player's inventory.
        Also, place  it at the player's coordinates.
        If it is an equipment, unequip it first."""

        scene = self.owner.scene

        if self.owner.equipment:
            self.owner.equipment.unequip()

        scene.add_obj(self.owner, 'objects', self.owner.pos)
        dropper.inventory.remove(self.owner)
        self.possessor = None

        self.owner.scene.gfx.msg_log.add(
            'You dropped a ' + self.owner.name + '.', GAME_COLORS["yellow"])
        return 'dropped'

    def use(self, user, target=None):
        # special case: if the object has the Equipment component, the "use"
        # action is to equip/unequip
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        # just call the "use_function" if it is defined
        if self.use_function is None:
            self.owner.scene.gfx.msg_log.add(
                'The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(who=user, target=target) != 'cancelled':
                user.inventory.remove(self.owner)
                # destroy after use, unless it was cancelled for some reason
                return 'used'
            else:
                return 'cancelled'


class DngFeat(Component):

    var_name = 'dng_feat'

    templates = {
        'stair_up': {
            'use_function': effects.change_dng_level,
            'direction': "up"
        },
        'stair_down': {
            'use_function': effects.change_dng_level,
            'direction': "down"
        }
    }

    def use(self, who):
        if self.use_function is None:
            self.owner.scene.gfx.msg_log.add(
                'This ' + self.owner.name + ' cannot be used.')
        else:
            if self.direction:
                return self.use_function(who=who, direction=self.direction)
            else:
                return self.use_function(who=who)


class Equipment(Component):
    """An object that can be equipped, yielding bonuses."""

    is_equipped = False
    slot = None

    def toggle_equip(self):
        """Toggle equip/unequip status."""
        if self.is_equipped:
            self.unequip()
        else:
            self.equip()
        self.owner.item.possessor.combat.set_melee_atk()

    def equip(self):
        """Equip object and show a message about it.
        If the slot is already being used, unequip whatever is there first."""

        if self.type == 'two-handed melee weapons':
            for slot in ['right hand', 'left hand']:
                old_equipment = self.equipped_in_slot(slot)
                if old_equipment:
                    old_equipment.unequip()
            self.slot = 'right hand'
        else:
            for slot in ['right hand', 'left hand']:
                old_equipment = self.equipped_in_slot(slot)
                if old_equipment and \
                        old_equipment.type == 'two-handed melee weapons':
                    old_equipment.unequip()
                    self.slot = 'right hand'
                    break
                elif not old_equipment:
                    self.slot = slot
                    break

            if self.slot is None:
                self.slot = 'right hand'
                old_equipment = self.equipped_in_slot(self.slot)
                old_equipment.unequip()

        self.is_equipped = True
        self.owner.scene.gfx.msg_log.add(
            'Equipped ' + self.owner.name + ' on ' +
            self.slot + '.', GAME_COLORS["light_green"])

    def unequip(self):
        """Unequip object and show a message about it."""
        if not self.is_equipped:
            return
        self.is_equipped = False
        self.owner.scene.gfx.msg_log.add(
            'Unequipped ' + self.owner.name + ' from ' +
            self.slot + '.', GAME_COLORS["light_yellow"])
        self.slot = None

    def equipped_in_slot(self, slot):
        """Returns the equipment in a slot, or None if it's empty."""
        inventory = self.owner.item.possessor.inventory

        for obj in inventory:
            if (
                obj.equipment and obj.equipment.slot == slot and
                obj.equipment.is_equipped
            ):
                return obj.equipment
        return None


class Weapon(Equipment):
    var_name = "equipment"
    templates = weapons_db.keys()

    _default = {
        "id": ord("|"),
        "color": GAME_COLORS["grey"]
    }

    def __init__(self, template):
        component = weapons_db[template]
        [component.setdefault(key, value)
            for key, value in self._default.items()]
        self.__dict__.update(component)
        self.slot = None
        self.name = component["melee_desc"]

        # every weapon is an item (can be picked up, etc.)

    # 'light melee weapons', 'one-handed melee weapons',
    # 'two-handed melee weapons'}

    @classmethod
    def test(cls):

        class Owner():
            inventory = []

        from mylib.data_tree import tk_tree_view

        weapon = Weapon("aklys")
        tk_tree_view(weapon.__dict__)


class TemplateHandler:
    templates = {}
    for _component in [Item, DngFeat, Weapon]:
        for cmp_template in _component.templates:
            templates.setdefault(cmp_template, [])
            templates[cmp_template].append({
                'type': _component,
                'name': _component.var_name})
            # every weapon is an item
            if _component == Weapon and len(templates[cmp_template]) == 1:
                templates[cmp_template].append({
                    'type': Item,
                    'name': Item.var_name})

    @classmethod
    def get(cls, value):
        return cls.templates[value]


if __name__ == '__main__':
    print(TemplateHandler.templates["aklys"])
