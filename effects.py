"""Spell-like effects, used for spells, potions, skills, etc."""

import random

from constants import GAME_COLORS, HEAL_AMOUNT, LIGHTNING_DAMAGE, \
    LIGHTNING_RANGE, CONFUSE_RANGE, FIREBALL_RADIUS, FIREBALL_DAMAGE

import ai_comp


def cast_heal(who, target=None):
    if target is None:
        target = who
    elif not hasattr(target, 'combat'):
        who.scene.msg_log.add(
            "You can't heal the " + target.name + " .", GAME_COLORS["yellow"])
        return 'cancelled'

    # heal the target
    if target.combat.hit_points_current == target.combat.hit_points_total:
        who.scene.msg_log.add(
            'You are already at full health.', GAME_COLORS["yellow"])
        return 'cancelled'

    target.combat.heal(HEAL_AMOUNT)
    who.scene.msg_log.add(
        'Your wounds start to feel better!', GAME_COLORS["light_violet"])


def cast_lightning(who, target=None):
    # find closest enemy (inside a maximum range) and damage it
    monster = who.combat.closest_monster(
        who=who, max_range=LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        who.scene.msg_log.add(
            'No enemy is close enough to strike.', GAME_COLORS["yellow"])
        return 'cancelled'

    # zap it!
    who.scene.msg_log.add(
        'A lighting bolt strikes the ' + monster.name +
        ' with a loud thunder! The damage is '
        + str(LIGHTNING_DAMAGE) + ' hit points.', GAME_COLORS["light_blue"])
    monster.combat.receive_dmg(LIGHTNING_DAMAGE)


def cast_fireball(who, target):
    """..."""
    if target is None:
        return 'cancelled'

    current_level = who.current_level
    msg_log = who.scene.msg_log

    msg_log.add(
        'The fireball explodes, burning everything within ' +
        str(FIREBALL_RADIUS) + ' tiles!', GAME_COLORS["yellow"])

    area = current_level.get_area(pos=target.pos, radius=FIREBALL_RADIUS)

    for pos in area:
        for creature in current_level[pos].creatures:
            if creature.combat:
                msg_log.add("The {} gets burned for {} hit points.".format(
                    creature.name, FIREBALL_DAMAGE), GAME_COLORS["orange"])
                creature.combat.receive_dmg(FIREBALL_DAMAGE, source=who)

    who.scene.tile_fx.add(
        coord=area,
        color=GAME_COLORS["orange"],
        duration=1)

    return True


def cast_confuse(who, target=None):
    status = 'ok'
    if target is None or not hasattr(target, 'combat'):
        status = 'cancelled'
    elif target.combat is None:
        status = 'cancelled'

    if status == 'cancelled':
        who.scene.msg_log.add("Thats not a valid target.",
                                  GAME_COLORS["yellow"])
        return 'cancelled'
    else:
        # replace the monster's AI with a "confused" one; after some turns
        # it will restore the old AI
        target.ai = ai_comp.Confused()
        target.ai.owner = target  # tell the new component who owns it
        target.color = GAME_COLORS["pink"]

        who.scene.msg_log.add(
            'The eyes of the ' + target.name +
            ' look vacant, as he starts to stumble around!',
            GAME_COLORS["pink"])


def change_dng_level(who, direction):
    if direction == "down":
        who.scene.msg_log.add(
            'There are stairs going {} here.'.format(direction) +
            "You descend deeper into the heart of the dungeon...",
            GAME_COLORS["orange"])
        who.scene.new_level(who.scene.current_level + 1)
        return True


def rnd_cast_confuse(who, target=None):
    # find closest enemy in-range and confuse it
    monster = who.combat.closest_monster(
        who=who, max_range=CONFUSE_RANGE)
    if monster is None:  # no enemy found within maximum range
        who.scene.msg_log.add(
            'No enemy is close enough to confuse.', GAME_COLORS["yellow"])
        return 'cancelled'
    # replace the monster's AI with a "confused" one; after some turns it will
    # restore the old AI
    monster.ai = ai_comp.Confused()
    monster.ai.owner = monster  # tell the new component who owns it
    monster.color = GAME_COLORS["pink"]

    who.scene.msg_log.add(
        'The eyes of the ' + monster.name +
        ' look vacant, as he starts to stumble around!',
        GAME_COLORS["light_green"])


def player_death(victim):
    """..."""
    # the game ended!
    victim.scene.msg_log.add('You died!')
    victim.scene.state = 'dead'

    # for added effect, transform the player into a corpse!
    victim.id = ord('%')
    victim.color = GAME_COLORS["dark_red"]


def monster_death(victim):
    """..."""
    import obj_components
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    victim.scene.msg_log.add('{} is dead! You gain {} xp'.format(
        victim.name.capitalize(), victim.combat.xp_award), GAME_COLORS["cyan"])

    victim.scene.rem_obj(victim, 'creatures', victim.pos)
    if random.randint(1, 100) > 66:
        victim.id = ord('%')
        victim.color = GAME_COLORS["dark_red"]
        victim.item = obj_components.Item('remains')
        victim.item.owner = victim
        victim.name = 'remains of ' + victim.name

        victim.scene.add_obj(victim, 'objects', victim.pos)

    """TODO: standardize death as method."""
    victim.blocks = False
    victim.combat = None
    victim.ai = None
