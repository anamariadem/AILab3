import random

from domain.constants import *


class Gene:
    def __init__(self):
        self._choice = random.choice(DRONE_DIRECTIONS)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, value):
        self._choice = value
