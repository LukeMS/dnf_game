from constants import GameColor
from constants import CONFUSE_NUM_TURNS


class Confused:
    # AI for a temporarily confused monster (reverts to previous AI after a
    # while).

    def __init__(self, num_turns=CONFUSE_NUM_TURNS):
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns
            # confused
            self.owner.move_rnd()
            self.num_turns -= 1

        # restore the previous AI (this one will be deleted because it's not
        # referenced anymore)
        else:
            self.owner.ai = self.owner.default_ai
            self.owner.color = self.owner.default_color
            self.owner.game.gfx.msg_log.add(
                'The ' + self.owner.name + ' is no longer confused!',
                GameColor.yellow)


class Basic:
    # AI for a basic monster.

    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner

        # if monster.map.tiles[monster.pos].visible:
        target = monster.map.player
        # move towards player if far away
        if monster.distance_to(monster.map.player) > 1:
            # print("{} moves".format(monster.name))
            monster.move_towards(target=target)

        # close enough, attack! (if the player is still alive.)
        elif target.fighter.hp > 0:
            monster.fighter.attack(target)

        # monster.active = False
