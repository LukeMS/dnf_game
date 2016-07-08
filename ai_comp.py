import random
from constants import GAME_COLORS
from constants import CONFUSE_NUM_TURNS


class Ai:
    owner = None
    locked = False
    effect = None


class Confused(Ai):
    """AI for a temporarily confused monster.
    It reverts to previous AI after a while)."""

    def __init__(self, num_turns=CONFUSE_NUM_TURNS):
        self.num_turns = num_turns
        self.effect = True

    def take_turn(self):
        # some kind of lock to prevent double calling AND queueing of
        # same objects on a single turn.
        if self.locked:
            return
        self.locked = True

        monster = self.owner

        monster.path = None

        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns
            # confused
            if monster.scene.grid[monster.pos].visible:
                monster.scene.gfx.msg_log.add(
                    (monster.name + " looks confused"), GAME_COLORS["pink"])
            if random.randint(1, 100) > 33:
                monster.move_rnd()
            else:
                monster.move()
            self.num_turns -= 1

        # restore the previous AI (this one will be deleted because it's not
        # referenced anymore)
        else:
            self.effect = False
            monster.ai = monster.default_ai
            monster.color = monster.default_color
            monster.scene.gfx.msg_log.add(
                'The ' + monster.name + ' is no longer confused!',
                GAME_COLORS["yellow"])

        self.locked = False


class Basic(Ai):
    """AI for a basic monster."""

    def take_turn(self):
        """A basic monster takes its turn."""

        # some kind of lock to prevent double calling AND queueing of
        # same objects on a single turn.
        if self.locked:
            return
        self.locked = True
        #

        monster = self.owner
        target = monster.scene.player
        distance = monster.distance_to(monster.scene.player)

        # move towards player if far away
        if distance >= 2:  # implement reach here
            if monster.path:
                # continue following the path
                try:
                    old_path = list[monster.path]
                    moved = monster.move(monster.path.pop(1))
                except:
                    moved = False
                else:
                    monster.scene.tile_fx.add(
                        coord=old_path[2:-1],
                        color=GAME_COLORS["green"],
                        duration=1)
            else:
                moved = False

            if not moved:
                # find a new path
                monster.path = monster.move_towards(target=target)
                try:
                    monster.scene.tile_fx.add(
                        coord=monster.path[2:-1],
                        color=GAME_COLORS["green"],
                        duration=1)
                except:
                    monster.scene.pathing = []

        # close enough, attack! (if the player is still alive.)
        elif target.combat.hit_points_current > 0:
            monster.combat.attack(target)

        self.locked = False
