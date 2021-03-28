from random import randint, random

from domain.gene import *


class Individual:
    def __init__(self, size=INDIVIDUAL_LIFETIME, representation= None):
        self._representation = [Gene() for i in range(size)]
        self._size = size
        self._fitness = None

    @property
    def representation(self):
        return self._representation

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, newFitness):
        self._fitness = newFitness

    def mutate(self, mutateProbability=MUTATE_PROBABILITY):
        if random.random() < mutateProbability:
            randomGenePosition = randint(0, self._size - 1)
            self._representation[randomGenePosition] = Gene()


    # def crossover2X2(self, otherParent, crossoverProbability=CROSSOVER_PROBABILITY):
    #     firstOffspring = Individual(self._size)
    #     secondOffspring = Individual(self._size)
    #     if random() < crossoverProbability:
    #         index = randint(1, self._size - 2)
    #         firstOffspring._representation = self.representation[:index] + otherParent.representation[index:]
    #         secondOffspring._representation = self.representation[index:] + otherParent.representation[:index]
    #         return firstOffspring, secondOffspring
    #
    #     return self, otherParent

    def crossover(self, otherParent, crossoverProbability=CROSSOVER_PROBABILITY):
        if random.random() < crossoverProbability:
            index = randint(1, len(self._representation) - 2)
            newRepresentation = self._representation[:index] + otherParent.representation[index:]

            return Individual(self._size, newRepresentation)
        return self

