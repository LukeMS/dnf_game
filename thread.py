import time
import threading

import pygame
from pygame.color import Color


def nexter1():
    counter = 0
    while 1:
        print('myThread1:', counter)
        counter += 1
        time.sleep(10)


def nexter2():
    counter = 0
    while 1:
        print('myThread2:', counter)
        counter += 1
        time.sleep(5)


pygame.init()

screen = pygame.display.set_mode([640, 640])
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 25, True)
count = 0
pygame.display.set_caption("Test")

done = False
while not done:
    screen.fill(Color('black'))
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True

    # Create new threads
    thread1 = threading.Thread(target=nexter1)
    thread2 = threading.Thread(target=nexter2)

    # Start new Threads
    thread1.start()
    thread2.start()

    output_string = "ACTUAL          %s" % count
    text = font.render(output_string, True, Color('red'))
    screen.blit(text, [250, 420])
    clock.tick(20)
    pygame.display.flip()
