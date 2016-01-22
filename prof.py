from level import LevelScene
from game import Game

from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)


if __name__ == '__main__':
    import cProfile
    cProfile.run('main()', "profile.tmp")

    import pstats
    stream = open('profile.txt', 'w')
    p = pstats.Stats('profile.tmp', stream=stream)

    # `time`, `cumulative`
    p.sort_stats('ncalls', 'cumulative', 'time').print_stats()
