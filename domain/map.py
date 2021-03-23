import numpy as np
from random import random
import pygame

from domain.constants import *


class DroneMap:
    def __init__(self, n=ROWS, m=COLUMNS):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def image(self, colour=BLACK, background=WHITE):
        imagine = pygame.Surface((SQUARE_WIDTH * COLUMNS, SQUARE_HEIGHT * ROWS))
        brick = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * SQUARE_WIDTH, i * SQUARE_HEIGHT))

        return imagine


    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
