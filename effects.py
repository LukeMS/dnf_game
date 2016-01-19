from constants import GameColor, HEAL_AMOUNT


def cast_heal(who, target=None):
    if target is None:
        target = who
    # heal the target
    if target.fighter.hp == target.fighter.max_hp:
        who.game.gfx.msg_log.add(
            'You are already at full health.', GameColor.yellow)
        return 'cancelled'

    target.fighter.heal(HEAL_AMOUNT)
    who.game.gfx.msg_log.add(
        'Your wounds start to feel better!', GameColor.light_violet)
