import time

import pygame

from domain.constants import *

def initPygame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("Assets/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Evolutionary drone exploration")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePygame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()


def movingDrone(currentMap, path, speed=0.5, markSeen=True):
    # animation of a drone on a path
    screen = initPygame((currentMap.m * SQUARE_WIDTH, currentMap.n * SQUARE_HEIGHT))
    drona = pygame.image.load("Assets/drona.png")
    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))
        if markSeen:
            brick = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT))
            brick.fill(PINK)
            for j in range(i + 1):
                for direction in DRONE_DIRECTIONS:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + direction[0] < currentMap.n and
                            0 <= y + direction[1] < currentMap.m) and
                           currentMap.surface[x + direction[0]][y + direction[1]] != WALL):
                        x = x + direction[0]
                        y = y + direction[1]
                        screen.blit(brick, (y * SQUARE_WIDTH, x * SQUARE_HEIGHT))

        screen.blit(drona, (path[i][1] * SQUARE_WIDTH, path[i][0] * SQUARE_HEIGHT))
        pygame.display.flip()
        time.sleep(speed)
    closePygame()


def mapWithDrone(currentMap, dronePosition):
    screen = initPygame((currentMap.m * SQUARE_WIDTH, currentMap.n * SQUARE_HEIGHT))
    screen.blit(image(currentMap), (0, 0))
    drone = pygame.image.load("Assets/drona.png")
    screen.blit(drone, (dronePosition[1] * SQUARE_WIDTH, dronePosition[0] * SQUARE_HEIGHT))
    for _ in range(1000):
        pygame.display.flip()
    closePygame()


def image(currentMap, colour=BLACK, background=WHITE):
    imagine = pygame.Surface((currentMap.m * SQUARE_WIDTH, currentMap.n * SQUARE_HEIGHT))
    brick = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * SQUARE_WIDTH, i * SQUARE_HEIGHT))
    return imagine
