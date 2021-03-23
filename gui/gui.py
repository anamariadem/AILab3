# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, time
from domain.constants import *
from domain.map import *
from controller.controller import Controller


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("..\\Assets\\logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
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


def movingDrone(currentMap, path, speed=1, markSeen=True):
    # animation of a drone on a path

    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

    drona = pygame.image.load("drona.png")

    for i in range(len(path)):
        screen.blit(currentMap.image(), (0, 0))

        if markSeen:
            brick = pygame.Surface((20, 20))
            brick.fill(GREEN)
            for j in range(i + 1):
                for var in DRONE_DIRECTIONS:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + var[0] < currentMap.n and
                            0 <= y + var[1] < currentMap.m) and
                           currentMap.surface[x + var[0]][y + var[1]] != 1):
                        x = x + var[0]
                        y = y + var[1]
                        screen.blit(brick, (y * 20, x * 20))

        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)
    closePyGame()

class UI:
    def __init__(self):
        self._controller = Controller()

    @staticmethod
    def displayWithPath(image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    # define a main function
    def main(self):

        # we create the map
        # m.randomMap()
        # m.saveMap("test2.map")

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("..\\Assets\\logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False


            screen.blit(self._controller.mapWithDrone(), (0, 0))
            pygame.display.flip()

            cacat, path = self._controller.solver()


            screen.blit(self._controller.mapWithPath(path), (0, 0))

            pygame.display.flip()
            running = False
        print(path)
        time.sleep(10)
        pygame.quit()


if __name__ == "__main__":
    # initPyGame((COLUMNS * SQUARE_SIDE_SIZE, ROWS * SQUARE_SIDE_SIZE))

    ui = UI()
    ui.main()

