from constants import GameColor
import effects


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


class Equipment(Component):
    """An object that can be equipped, yielding bonuses."""

    _base = {
        'is_equipped': False,
        'power_bonus': 0,
        'defense_bonus': 0,
        'max_hp_bonus': 0
    }
    templates = {
        "dagger": {
            'slot': 'right hand',
            'power_bonus': 1
        },
        "short sword": {
            'slot': 'right hand',
            'power_bonus': 2
        },
        "sword": {
            'slot': 'right hand',
            'power_bonus': 3
        },
        "shield": {
            'slot': 'left hand',
            'defense_bonus': 1
        }
    }

    def toggle_equip(self):
        """Toggle equip/unequip status."""
        if self.is_equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        """Equip object and show a message about it.
        If the slot is already being used, unequip whatever is there first."""
        old_equipment = self.equipped_in_slot(self.slot)
        if old_equipment:
            old_equipment.unequip()

        self.is_equipped = True
        self.owner.scene.gfx.msg_log.add(
            'Equipped ' + self.owner.name + ' on ' +
            self.slot + '.', GameColor.light_green)

    def unequip(self):
        """Unequip object and show a message about it."""
        if not self.is_equipped:
            return
        self.is_equipped = False
        self.owner.scene.gfx.msg_log.add(
            'Unequipped ' + self.owner.name + ' from ' +
            self.slot + '.', GameColor.light_yellow)

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


class Item(Component):

    _base = {
        'possessor': None,
        'use_function': None
    }

    templates = {
        'healing potion': {
            'use_function': effects.cast_heal
        },

        'scroll of lightning bolt': {
            'use_function': effects.cast_lightning
        },

        'scroll of confusion': {
            'use_function': effects.cast_confuse
        },

        'scroll of fireball': {
            'use_function': effects.cast_fireball
        },

        "dagger": {},
        "short sword": {},
        "sword": {},

        'shield': {},

        'remains': {
            'use_function': effects.cast_heal
        }
    }

    def pick_up(self, getter):
        scene = self.owner.scene
        msg_log = self.owner.scene.gfx.msg_log

        # add to the player's inventory and remove from the map
        if len(getter.inventory) >= 26:
            if getter == self.owner.scene.player:
                msg_log.add(
                    'Your inventory is full, cannot pick up ' +
                    self.owner.name + '.', GameColor.yellow)
        else:
            scene.rem_obj(self.owner, 'objects', self.owner.pos)

            getter.inventory.append(self.owner)
            self.possessor = getter

            msg_log.add(
                'You picked up a ' + self.owner.name + '!',
                GameColor.blue)

        """special case: automatically equip, if the corresponding equipment
        slot is unused"""
        equipment = self.owner.equipment
        if equipment:
            if not equipment.equipped_in_slot(equipment.slot):
                equipment.equip()

    def drop(self, dropper):
        """Add to the map and remove from the player's inventory.
        Also, place  it at the player's coordinates.
        If it is an equipment, unequip it first."""
        scene = self.owner.scene
        msg_log = self.owner.scene.gfx.msg_log

        if self.owner.equipment:
            self.owner.equipment.unequip()

        scene.add_obj(self.owner, 'objects', dropper.pos)
        dropper.inventory.remove(self.owner)
        self.possessor = None
        self.owner.pos = dropper.pos
        msg_log.add('You dropped a ' + self.owner.name + '.', GameColor.yellow)

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


class Fighter(Component):
    """Combat-related properties and methods (monster, player, NPC)."""

    _base = {
        "damage": 0,
        "xp": 0,
        "level": 1
    }

    templates = {
        "player": {
            "base_max_hp": 30,
            "base_defense": 1,
            "base_power": 3,
            "xp_value": 50,
            "death_func": effects.player_death
        },
        "orc": {
            "base_max_hp": 10,
            "base_defense": 0,
            "base_power": 3,
            'xp_value': 35,
            "death_func": effects.monster_death
        },
        "troll": {
            "base_max_hp": 16,
            "base_defense": 1,
            "base_power": 4,
            'xp_value': 100,
            "death_func": effects.monster_death
        }
    }

    @property
    def power(self):
        return self.base_power + self.equipment_bonus('power_bonus')

    @property
    def defense(self):
        return self.base_defense + self.equipment_bonus('defense_bonus')

    @property
    def max_hp(self):
        return self.base_max_hp + self.equipment_bonus('max_hp_bonus')

    def equipment_bonus(self, bonus):
        return sum(
            getattr(item.equipment, bonus) for item in self.all_equipped())

    def all_equipped(self):
        return [
            item for item in self.owner.inventory if
            item.equipment and item.equipment.is_equipped
        ]

    @property
    def hp(self):
        return self.max_hp - self.damage

    def take_damage(self, damage, atkr=None):
        # apply damage if possible
        if damage > 0:
            self.damage += damage

        # check for death. if there's a death function, call it
        if self.hp <= 0:
            if self.death_func is not None:
                self.death_func(self.owner, atkr=atkr)
            if hasattr(atkr, 'gainxp'):
                atkr.gain_xp(self.xp_value)

        self.owner.update_hp()

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.damage -= amount
        self.damage = max(0, self.damage)  # no negative damage
        self.owner.update_hp()

    def attack(self, target):
        """A simple formula for attack damage."""
        damage = self.power - target.fighter.defense

        if self.owner.ai:
            color = GameColor.red  # I'm a monster!
        else:
            color = None  # I'm the player

        if damage > 0:
            # make the target take some damage
            self.owner.scene.gfx.msg_log.add(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' for ' + str(damage) + ' hit points.', color)
            target.fighter.take_damage(damage=damage, atkr=self.owner)
        else:
            self.owner.scene.gfx.msg_log.add(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' but it has no effect!', color)

    def closest_monster(self, who, max_range):
        def val_callback(target):
            return target.fighter and not target == who
        # find closest enemy, up to a maximum range, and in the player's FOV
        closest_enemy = self.owner.scene.get_nearest_obj(
            _type='creatures',
            pos=self.owner.pos,
            max_range=max_range,
            visible_only=True,
            val_callback=val_callback)

        return closest_enemy

if __name__ == '__main__':
    for component in [Equipment, Item, DngFeat, Fighter]:
        print("#" * 6)
        print("Component:", component)
        for template in component.templates.keys():
            print("_" * 3)
            print("Template:", template)
            component(template=template, test=True)
