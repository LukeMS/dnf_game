from constants import GameColor
import effects


class DngFeatComponent:
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

    def __init__(self, template):
        # hp, defense, power, death_func=None):
        for key, value in self.templates[template].items():
            setattr(self, key, value)

    def use(self, who):
        if self.use_function is None:
            self.owner.map.game.gfx.msg_log.add(
                'This ' + self.owner.name + ' cannot be used.')
        else:
            if self.direction:
                return self.use_function(who=who, direction=self.direction)
            else:
                return self.use_function(who=who)

class ItemComponent:
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
        'remains': {
            'use_function': effects.cast_heal
        }
    }

    def __init__(self, template):
        # hp, defense, power, death_func=None):
        for key, value in self.templates[template].items():
            setattr(self, key, value)

    def pick_up(self, getter):
        # add to the player's inventory and remove from the map
        if len(getter.inventory) >= 26:
            if getter == self.owner.map.player:
                self.owner.map.game.gfx.msg_log.add(
                    'Your inventory is full, cannot pick up ' +
                    self.owner.name + '.', GameColor.yellow)
        else:
            getter.inventory.append(self.owner)
            self.owner.group.remove(self.owner)
            self.owner.map.game.gfx.msg_log.add(
                'You picked up a ' + self.owner.name + '!',
                GameColor.blue)

    def drop(self, dropper):
        # add to the map and remove from the player's inventory. also, place
        # it at the player's coordinates
        self.owner.group.add(self.owner)
        dropper.inventory.remove(self.owner)
        self.owner.pos = dropper.pos
        self.owner.map.game.gfx.msg_log.add(
            'You dropped a ' + self.owner.name + '.', GameColor.yellow)
        return 'used'

    def use(self, user, target=None):
        # just call the "use_function" if it is defined
        if self.use_function is None:
            self.owner.map.game.gfx.msg_log.add(
                'The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(who=user, target=target) != 'cancelled':
                user.inventory.remove(self.owner)
                # destroy after use, unless it was cancelled for some reason
                return 'used'
            else:
                return 'cancelled'
