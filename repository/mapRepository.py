import pickle

from domain.map import DroneMap
from domain.constants import *


class MapRepository:
    def __init__(self, mapFile=None):
        self._map = DroneMap()
        if mapFile is not None:
            self.readFromFile(mapFile)
        else:
            self._map.randomMap()

    @property
    def map(self):
        return self._map

    def readFromFile(self, file):
        with open(file, "rb") as f:
            self._map = pickle.load(f)
            f.close()

    def saveToFile(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self._map, f)
            f.close()

    def randomMap(self):
        self._map.randomMap()

    def mapImage(self):
        return self._map.image()

    def __getitem__(self, item):
        return self._map.surface[item]

    @staticmethod
    def isValidPosition(xPosition, yPosition):
        return 0 <= xPosition < ROWS and 0 <= yPosition < COLUMNS

    def readDirection(self, dronePosition, direction):
        xDirection, yDirection = direction
        xPosition, yPosition = dronePosition

        discoveredPositions = []
        xPosition, yPosition = xPosition + xDirection, yPosition + yDirection

        while self.isValidPosition(xPosition, yPosition) and self._map.surface[(xPosition, yPosition)] == 0:
            discoveredPositions.append((xPosition, yPosition))
            xPosition, yPosition = xPosition + xDirection, yPosition + yDirection

        return discoveredPositions

    def readSensors(self, dronePosition):
        discoveredPositions = [dronePosition]

        for direction in DRONE_DIRECTIONS:
            discoveredPositions += self.readDirection(dronePosition, direction)

        return discoveredPositions

