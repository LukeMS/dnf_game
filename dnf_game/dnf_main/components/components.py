"""..."""

from dnf_game.dnf_main.data_handler import get_color
from dnf_game.util.interpreter import interpreter


class ComponentAbstract:
    """..."""

    def __init__(self, template, owner=None, test=False):
        """..."""
        self.__dict__.update(template)
        self.owner = owner

    @property
    def scene(self):
        """..."""
        return self.owner.scene

    @property
    def player(self):
        """..."""
        return self.scene.player

    @classmethod
    def test(cls):
        """..."""
        from mylib.data_tree import tk_tree_view
        tk_tree_view(cls.templates)


class FeatureComponent(ComponentAbstract):
    """..."""

    def use(self, who):
        """..."""
        if self.use_function is None:
            self.scene.msg_log.add(
                'This ' + self.owner.name + ' cannot be used.')
        else:
            if self.direction:
                return self.use_function(who=who, direction=self.direction)
            else:
                return self.use_function(who=who)


class ItemComponent(ComponentAbstract):
    """..."""

    possessor = None

    def pick_up(self, getter):
        """..."""
        msg_log = self.scene.msg_log

        # add to the player's inventory and remove from the map
        if len(getter.inventory) >= 26:
            if getter == self.player:
                self.scene.msg_log.add(
                    'Your inventory is full, cannot pick up ' +
                    self.owner.name + '.', get_color("yellow"))
        else:
            self.scene.rem_obj(self.owner, 'objects', self.owner.pos)

            getter.inventory.append(self.owner)
            self.possessor = getter

            msg_log.add(
                'You picked up a ' + self.owner.name + '!',
                get_color("blue"))

    def drop(self, dropper):
        """Add to the map and remove from the player's inventory.

        Also, place  it at the player's coordinates.
        If it is an equipment, unequip it first.
        """
        if self.owner.equipment:
            self.owner.equipment.unequip()

        self.scene.add_obj(self.owner, 'objects', self.owner.pos)
        dropper.inventory.remove(self.owner)
        self.possessor = None

        self.scene.msg_log.add(
            'You dropped a ' + self.owner.name + '.', get_color("yellow"))
        return 'dropped'

    def use(self, user, target=None):
        """..."""
        # special case: if the object has the Equipment component, the "use"
        # action is to equip/unequip
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return 'equipped'

        # just call the "use_function" if it is defined
        if self.use_function is None:
            self.scene.msg_log.add(
                'The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(who=user, target=target) != 'cancelled':
                user.inventory.remove(self.owner)
                # destroy after use, unless it was cancelled for some reason
                return 'used'
            else:
                return 'cancelled'


class EquipmentComponentAbstract(ComponentAbstract):
    """An object that can be equipped, yielding bonuses."""

    is_equipped = False
    slot = None

    action_lists = {
        "on_hit": "on_hit_actions",
        "on_turn": "on_turn_actions",
    }

    @property
    def possessor(self):
        """..."""
        return self.owner.item.possessor

    def toggle_equip(self):
        """Toggle equip/unequip status."""
        if self.is_equipped:
            self.unequip()
            interpreter(self, self.on_unequip)
            self.owner.item.possessor.combat.feats.on_unequip()
        else:
            self.equip()
            interpreter(self, self.on_equip)
            self.owner.item.possessor.combat.feats.on_equip()

    def add_to(self, category, actions):
        """Add one or more actions to the category's list."""
        action_list = getattr(self, self.action_lists[category])

        for action in actions:
            if action not in action_list:
                action_list.append(action)

    def remove_from(self, category, actions):
        """Remove one or more actions from the category's list."""
        action_list = self.action_lists[category]

        for action in actions:
            if action in action_list:
                action_list.remove(action)

    def equip(self):
        """Should be overwritten by subclass."""
        pass

    def unequip(self):
        """Unequip object and show a message about it."""
        if not self.is_equipped:
            return
        self.is_equipped = False

        self.scene.msg_log.add(
            'Unequipped ' + self.owner.name + ' from ' +
            self.slot + '.', get_color("light_yellow"))
        self.slot = None


class WeaponComponent(EquipmentComponentAbstract):
    """..."""

    def __init__(self, template, **kwargs):
        """Create an instance based on a template."""
        super().__init__(template, **kwargs)
        self.name = self.melee_desc

    def toggle_equip(self):
        """Toggle equip/unequip status."""
        super().toggle_equip()

        self.owner.item.possessor.combat.set_melee_atk()

    def equip(self):
        """Equip object and show a message about it.

        If the slot is already being used, unequip whatever is there first.
        """
        equipped_in_slot = self.possessor.combat.equipped_in_slot

        if self.type == 'two-handed melee weapons':
            for slot in ['right hand', 'left hand']:
                old_equipment = equipped_in_slot(slot)
                if old_equipment:
                    old_equipment.unequip()
            self.slot = 'right hand'
        else:
            for slot in ['right hand', 'left hand']:
                old_equipment = equipped_in_slot(slot)
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
                old_equipment = equipped_in_slot(self.slot)
                old_equipment.unequip()

        self.is_equipped = True
        self.scene.msg_log.add(
            'Equipped ' + self.owner.name + ' on ' +
            self.slot + '.', get_color("light_green"))

    # 'light melee weapons', 'one-handed melee weapons',
    # 'two-handed melee weapons'}

    @classmethod
    def test(cls):
        """..."""
        class Owner():
            inventory = []

        from mylib.data_tree import tk_tree_view

        weapon = WeaponComponent("aklys")
        tk_tree_view(weapon.__dict__)


class ArmorComponent(EquipmentComponentAbstract):
    """..."""

    def __init__(self, template, **kwargs):
        """Create an instance based on a template."""
        self.type = template["family"]
        super().__init__(template, **kwargs)

    def equip(self):
        """Equip object and show a message about it.

        If the slot is already being used, unequip whatever is there first.
        """
        equipped_in_slot = self.possessor.combat.equipped_in_slot

        self.slot = 'left hand' if self.type == 'shields' else 'body'

        old_equipment = equipped_in_slot(self.slot)
        if old_equipment:
            old_equipment.unequip()

        self.is_equipped = True
        self.scene.msg_log.add(
            'Equipped ' + self.owner.name + ' on ' +
            self.slot + '.', get_color("light_green"))

    # 'light melee weapons', 'one-handed melee weapons',
    # 'two-handed melee weapons'}

    @classmethod
    def test(cls):
        """..."""
        class Owner():
            inventory = []

        from mylib.data_tree import tk_tree_view

        weapon = WeaponComponent("aklys")
        tk_tree_view(weapon.__dict__)
