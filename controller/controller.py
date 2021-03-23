from random import randint, seed
import pygame

from repository.mapRepository import *
from repository.population import *
from domain.drone import *


class Controller:
    def __init__(self):
        self._mapRepository = MapRepository()
        self._population = None

        position = randint(0, ROWS - 1), randint(0, COLUMNS - 1)
        while self._mapRepository[position] != 0:
            position = randint(0, ROWS - 1), randint(0, COLUMNS - 1)

        self._drone = Drone(position[0], position[1])


    def getPathFromRepresentation(self, representation):
        xPosition, yPosition = self._drone.position
        path = [(xPosition, yPosition)]
        for xDirection, yDirection in representation:
            xPosition, yPosition = xPosition + xDirection, yPosition + yDirection
            if self._mapRepository.isValidPosition(xPosition, yPosition) and \
                    self._mapRepository[(xPosition, yPosition)] == 1:
                break
            path.append((xPosition, yPosition))
        return path

    # def simpleFitness(self, representation):
    #     path = self.getPathFromRepresentation(representation)
    #     error = len(representation) - len(path)
    #     return -(len(self.detectedPositions(path)) - error * ERROR_FACTOR)

    def uniquePositionsFitness(self, representation):
        path = self.getPathFromRepresentation(representation)
        error = len(representation) - len(path)
        return -(len(set(path)) - error * ERROR_FACTOR)

    def variationFitness(self, representation):
        count = -1
        prev = None
        for gene in representation:
            if gene != prev:
                count += 1
                prev = gene

        path = self.getPathFromRepresentation(representation)
        return -(count * len(set(path))/len(representation))

    def iteration(self, fitnessFunction):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        for _ in range(STEADY_STATE_NO_OFFSPRINGS):
            (firstPosition, firstParent), (secondPosition, secondParent) = self._population.selection(2)
            offspring = firstParent.crossover(secondParent)
            offspring.mutate()

            offspring.fitness = fitnessFunction(offspring.representation)

            if (firstParent.fitness > secondParent.fitness) and (firstParent.fitness > offspring.fitness):
                self._population[firstPosition] = offspring
            if (secondParent.fitness > firstParent.fitness) and (secondParent.fitness > offspring.fitness):
                self._population[secondPosition] = offspring

    def generationalIteration(self, fitnessFunction):
        newPopulation = []
        for _ in range(len(self._population)):
            (_, firstParent), (_, secondParent) = self._population.selection(2)
            offspring = firstParent.crossover(secondParent)
            offspring.mutate()

            offspring.fitness = fitnessFunction(offspring.representation)

            newPopulation.append(offspring)

        self._population.setPopulation(newPopulation)

    def run(self, fitnessFunction):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information needed for the satistics

        # return the results and the info for statistics

        fitnessAverages = []
        bestIndividual = None

        for generation in range(1, GENERATIONS + 1):
            fitnessAverages.append(self._population.fitnessAverage())
            if bestIndividual is None or bestIndividual.fitness < self._population.bestIndividual().fitness:
                bestIndividual = self._population.bestIndividual()

            self.iteration(fitnessFunction)

        return fitnessAverages, bestIndividual


    def solver(self):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics

        seEd = randint(0, 4000000)
        seed(seEd)

        self._population = Population()
        self._population.evaluate(self.uniquePositionsFitness)

        fitnessAverages, bestIndividual = self.run(self.uniquePositionsFitness)

        bestPath = self.getPathFromRepresentation(bestIndividual.representation)

        return fitnessAverages, bestPath


    def mapWithDrone(self, image=None):
        drone = pygame.transform.scale(pygame.image.load("Resources/drona.png"), (SQUARE_HEIGHT, SQUARE_WIDTH))
        if image is None:
            image = self._mapRepository.mapImage()
        image.blit(drone, (self._drone.position[1] * SQUARE_HEIGHT, self._drone.position[0] * SQUARE_WIDTH))
        return image

    def mapWithPath(self, path, image=None, color=PINK):
        markPath = pygame.Surface((SQUARE_HEIGHT, SQUARE_WIDTH))
        markPath.fill(color)
        if image is None:
            image = self._mapRepository.mapImage()

        for move in path:
            image.blit(markPath, (move[1] * SQUARE_HEIGHT, move[0] * SQUARE_WIDTH))
        return image