from numpy import average

from domain.individual import *
from domain.constants import *


class Population:
    def __init__(self, populationSize=POPULATION_SIZE, individualSize=INDIVIDUAL_LIFETIME):
        self._populationSize = populationSize
        self._population = [Individual(individualSize) for _ in range(populationSize)]
        # possible paths for the drone

    def __getitem__(self, item):
        return self._population[item]

    def __setitem__(self, key, value):
        self._population[key] = value

    def setPopulation(self, newPopulation):
        self._population = newPopulation

    def evaluate(self, fitnessFunction):
        for individual in self._population:
            individual.fitness = fitnessFunction(individual.representation)

    def selection(self, numberOfIndividuals=0):
        indexes = set()
        while len(indexes) != numberOfIndividuals:
            indexes.add(randint(0, len(self._population) - 1))

        return [(i, self._population[i]) for i in indexes]

    def bestIndividual(self):
        return max(self._population, key=lambda c: c.fitness)

    def fitnessAverage(self):
        return average([individual.fitness for individual in self._population])
