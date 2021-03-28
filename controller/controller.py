from random import randint, seed
import pygame
import time
import numpy as np
import statistics

from repository.mapRepository import *
from repository.population import *
from repository.algorithmDataRepository import *
from domain.drone import *


class Controller:
    def __init__(self):
        self._mapRepository = MapRepository()
        # self._algorithmDataRepository = AlgorithmDataRepository()
        self._population = None

        self.position = randint(0, ROWS - 1), randint(0, COLUMNS - 1)
        while self._mapRepository[self.position] != 0:
            self.position = randint(0, ROWS - 1), randint(0, COLUMNS - 1)

        self._drone = Drone(self.position[0], self.position[1])
        self._executionTime = None

    def getDronePosition(self):
        return self._drone.position

    def get_initial_pos(self):
        return self.position

    def randomMap(self):
        self._mapRepository.randomMap()

    def loadMap(self):
        self._mapRepository.readFromFile(file="../Assets/test1.map")

    def saveMap(self):
        self._mapRepository.saveToFile(file="../Assets/test1.map")

    def getMap(self):
        return self._mapRepository.map

    @property
    def executionTime(self):
        return self._executionTime

    def setDronePosition(self, x, y):
        self._drone.position = x, y

    def detectedPositions(self, path):
        detectedPositions = set()
        for position in path:
            detectedPositions = detectedPositions.union(set(self._mapRepository.readSensors(position)))
        return detectedPositions


    def getPathFromRepresentation(self, representation):
        xPosition, yPosition = self._drone.position
        path = [(xPosition, yPosition)]
        for g in representation:
            xPosition, yPosition = xPosition + g.choice[0], yPosition + g.choice[1]
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
        return len(set(path)) - error * ERROR_FACTOR

    def variationFitness(self, representation):
        count = -1
        prev = None
        for gene in representation:
            if gene != prev:
                count += 1
                prev = gene

        path = self.getPathFromRepresentation(representation)
        return -(count * len(set(path))/len(representation))

    def iteration(self, fitnessFunction, mutateProbability=MUTATE_PROBABILITY,
                  crossoverProbability=CROSSOVER_PROBABILITY,
                  populationSize=STEADY_STATE_NO_OFFSPRINGS):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        # possibleParents = self._population.selection(2 * populationSize)

        for _ in range(populationSize):
            (firstPosition, firstParent), (secondPosition, secondParent) = self._population.selection(2)
            # (firstPosition, firstParent), (secondPosition, secondParent) = \
            #     possibleParents.pop(randint(0, len(possibleParents) - 1)), \
            #     possibleParents.pop(randint(0, len(possibleParents) - 1))
            offspring = firstParent.crossover(secondParent, crossoverProbability)
            offspring.mutate(mutateProbability)

            offspring.fitness = fitnessFunction(offspring.representation)

            if (firstParent.fitness > secondParent.fitness) and (firstParent.fitness > offspring.fitness):
                self._population[firstPosition] = offspring
            if (secondParent.fitness > firstParent.fitness) and (secondParent.fitness > offspring.fitness):
                self._population[secondPosition] = offspring

    # def generationalIteration(self, fitnessFunction):
    #     newPopulation = []
    #     for _ in range(len(self._population)):
    #         (_, firstParent), (_, secondParent) = self._population.selection(2)
    #         offspring = firstParent.crossover(secondParent)
    #         offspring.mutate()
    #
    #         offspring.fitness = fitnessFunction(offspring.representation)
    #
    #         newPopulation.append(offspring)
    #
    #     self._population.setPopulation(newPopulation)

    def run(self, fitnessFunction, mutateProbability=MUTATE_PROBABILITY,
            crossoverProbability=CROSSOVER_PROBABILITY,
            populationSize=STEADY_STATE_NO_OFFSPRINGS,
            numberOfGenerations=GENERATIONS):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information needed for the satistics

        # return the results and the info for statistics

        fitnessAverages = []
        bestIndividuals = []
        bestIndividual = None

        for generation in range(1, numberOfGenerations + 1):
            fitnessAverages.append(self._population.fitnessAverage())
            bestIndividuals.append(self._population.bestIndividual().fitness)
            if bestIndividual is None or bestIndividual.fitness < self._population.bestIndividual().fitness:
                bestIndividual = self._population.bestIndividual()

            self.iteration(fitnessFunction, mutateProbability, crossoverProbability, populationSize)

        return fitnessAverages, bestIndividual, bestIndividuals


    def solver(self, mutateProbability=MUTATE_PROBABILITY,
               crossoverProbability=CROSSOVER_PROBABILITY,
               populationSize=STEADY_STATE_NO_OFFSPRINGS,
               individualSize=INDIVIDUAL_LIFETIME,
               numberOfGenerations=GENERATIONS):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics

        seEd = randint(0, 4000000)
        seed(seEd)

        self._population = Population(populationSize, individualSize)
        self._population.evaluate(self.uniquePositionsFitness)

        startTime = time.time()

        fitnessAverages, bestIndividual, bestIndividuals = self.run(self.uniquePositionsFitness, mutateProbability,
                                                                    crossoverProbability, populationSize,
                                                                    numberOfGenerations)

        self._executionTime = time.time() - startTime

        bestPath = self.getPathFromRepresentation(bestIndividual.representation)
        detectedPositions = self.detectedPositions(bestPath)

        return fitnessAverages, bestPath, bestIndividuals, bestIndividual, len(detectedPositions)

    # def getAlgorithmData(self):
    #     return self._algorithmDataRepository.getData()

    # @staticmethod
    # def computeFitnessStatistics(fitnessAverages):
    #     return np.average(fitnessAverages), np.std(fitnessAverages)
    #
    # @staticmethod
    # def computeDetectedPositionsAverages(numberOfDetectedPositions):
    #     return np.average(numberOfDetectedPositions), np.std(numberOfDetectedPositions)

    def mapWithDrone(self, image=None):
        drone = pygame.transform.scale(pygame.image.load("../Assets/drona.png"), (SQUARE_HEIGHT, SQUARE_WIDTH))
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