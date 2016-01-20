import time

from constants import GameColor, HEAL_AMOUNT, LIGHTNING_DAMAGE, \
    LIGHTNING_RANGE, CONFUSE_RANGE, FIREBALL_RADIUS, FIREBALL_DAMAGE

import ai_comp


def cast_heal(who, target=None):
    if target is None:
        target = who
    elif not hasattr(target, 'fighter'):
        who.game.gfx.msg_log.add(
            "You can't heal the " + target.name + " .", GameColor.yellow)
        return 'cancelled'

    # heal the target
    if target.fighter.hp == target.fighter.max_hp:
        who.game.gfx.msg_log.add(
            'You are already at full health.', GameColor.yellow)
        return 'cancelled'

    target.fighter.heal(HEAL_AMOUNT)
    who.game.gfx.msg_log.add(
        'Your wounds start to feel better!', GameColor.light_violet)


def cast_lightning(who, target=None):
    # find closest enemy (inside a maximum range) and damage it
    monster = who.fighter.closest_monster(
        who=who, max_range=LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        who.game.gfx.msg_log.add(
            'No enemy is close enough to strike.', GameColor.yellow)
        return 'cancelled'

    # zap it!
    who.game.gfx.msg_log.add(
        'A lighting bolt strikes the ' + monster.name +
        ' with a loud thunder! The damage is '
        + str(LIGHTNING_DAMAGE) + ' hit points.', GameColor.light_blue)
    monster.fighter.take_damage(LIGHTNING_DAMAGE)


def cast_fireball(who, target):
    if target is None:
        return 'cancelled'
    who.game.gfx.msg_log.add(
        'The fireball explodes, burning everything within ' +
        str(FIREBALL_RADIUS) + ' tiles!', GameColor.yellow)

    for obj in who.map.objects:
        # damage every fighter in range, including the player
        if (
            who.distance_to(target, obj) <= FIREBALL_RADIUS and
            obj.fighter and obj.next_to_vis
        ):
            who.game.gfx.msg_log.add(
                'The ' + obj.name + ' gets burned for ' +
                str(FIREBALL_DAMAGE) + ' hit points.', GameColor.orange)
            obj.fighter.take_damage(FIREBALL_DAMAGE)
    tile_fx_coord = who.map.map.get_area(target.pos, FIREBALL_RADIUS)
    tile_fx_color = [GameColor.orange for x in tile_fx_coord]

    who.map.tile_fx_coord.extend(tile_fx_coord)
    who.map.tile_fx_color.extend(tile_fx_color)


def cast_confuse(who, target=None):
    status = 'ok'
    if target is None or not hasattr(target, 'fighter'):
        status = 'cancelled'
    elif target.fighter is None:
        status = 'cancelled'

    if status == 'cancelled':
        who.game.gfx.msg_log.add("Thats not a valid target.", GameColor.yellow)
        return 'cancelled'
    else:
        # replace the monster's AI with a "confused" one; after some turns
        # it will restore the old AI
        target.ai = ai_comp.Confused()
        target.ai.owner = target  # tell the new component who owns it
        target.color = GameColor.pink

        who.game.gfx.msg_log.add(
            'The eyes of the ' + target.name +
            ' look vacant, as he starts to stumble around!',
            GameColor.pink)


def change_dng_level(who, direction):
    if direction == "down":
        who.game.gfx.msg_log.add(
            'There are stairs going {} here.'.format(direction) +
            "You descend deeper into the heart of the dungeon...",
            GameColor.orange)
        who.map.new_level(who.map.map.level + 1)
    return 1


def rnd_cast_confuse(who, target=None):
    # find closest enemy in-range and confuse it
    monster = who.fighter.closest_monster(
        who=who, max_range=CONFUSE_RANGE)
    if monster is None:  # no enemy found within maximum range
        who.game.gfx.msg_log.add(
            'No enemy is close enough to confuse.', GameColor.yellow)
        return 'cancelled'
    # replace the monster's AI with a "confused" one; after some turns it will
    # restore the old AI
    monster.ai = ai_comp.Confused()
    monster.ai.owner = monster  # tell the new component who owns it
    monster.color = GameColor.pink

    who.game.gfx.msg_log.add(
        'The eyes of the ' + monster.name +
        ' look vacant, as he starts to stumble around!', GameColor.light_green)
