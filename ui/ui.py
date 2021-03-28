import time
from matplotlib import pyplot

from ui.guiMethods import *
from controller.controller import *


class UI:
    def __init__(self):
        self._controller = Controller()
        self._isMapLoaded = False
        self._areParametersSetup = False
        self._isProgramSolved = False
        self._populationSize = None
        self._individualLifetime = None
        self._numberOfGenerations = None
        self._path = None
        self._fitnessAverages = None
        self._bestIndividuals = None
        self._numberOfDetectedPositions = None

    @staticmethod
    def printMainMenu():
        print("1. Map options")
        print("2. Evolutionary algorithm options")
        print("0. Exit")

    @staticmethod
    def printMapMenu():
        print("1. Create a random map")
        print("2. Load a map")
        print("3. Save a map")
        print("4. Visualise map")

    @staticmethod
    def printAlgorithmMenu():
        print("1. Parameters setup")
        print("2. Run the solver once")
        print("3. Run the solver multiple times and compute statistics")
        print("4. Visualise the statistics")
        print("5. View the drone on a path")

    def setupParameters(self):
        self._areParametersSetup = True
        self._populationSize = int(input("Give population size: "))
        self._individualLifetime = int(input("Give individual lifetime: "))
        self._numberOfGenerations = int(input("Give number of generations: "))

    def runSolverOnce(self):
        if not self._areParametersSetup:
            print("Parameters not set up")
            return
        if self._isProgramSolved:
            print("Program already solved")
            return

        self._fitnessAverages, self._path, self._bestIndividuals, _, self._numberOfDetectedPositions = \
            self._controller.solver(MUTATE_PROBABILITY, CROSSOVER_PROBABILITY, self._populationSize,
                                    self._individualLifetime, self._numberOfGenerations)

        print(f"Evolutionary algorithm took {self._controller.executionTime} seconds")
        print(f"It found a run with {len(self._path) - 1} moves and discovered {self._numberOfDetectedPositions} cells")
        self._isProgramSolved = True

    def runSolverMultipleTimes(self):
        if not self._areParametersSetup:
            print("Parameters not set up")
            return

        fitnessValues = []
        for i in range(30):
            seed(i)
            _, _, _, bestIndividual, _ = self._controller.solver(MUTATE_PROBABILITY, CROSSOVER_PROBABILITY,
                                                                 self._populationSize,
                                                                 self._individualLifetime,
                                                                 self._numberOfDetectedPositions)
            fitnessValues.append(bestIndividual.fitness)

        averageFitness = statistics.mean(fitnessValues)
        fitnessStandardDeviation = statistics.stdev(fitnessValues)
        print(f"Average solution fitness is {averageFitness} and it has a standard deviation of "
              f"{fitnessStandardDeviation}")

        pyplot.plot(fitnessValues)
        pyplot.ylim([0, None])
        pyplot.show()

    def visualiseStatistics(self):
        if not self._isProgramSolved:
            print("Program not yet solved")
            return
        pyplot.plot(self._fitnessAverages)
        pyplot.plot(self._bestIndividuals)
        pyplot.show()

    def droneOnPath(self):
        if not self._isProgramSolved:
            print("Please run the solver first")
            return
        movingDrone(self._controller.getMap(), self._path)

    def handleMapOptions(self):
        self.printMapMenu()
        choice = input(">")
        if choice == '1':
            self._isMapLoaded = True
            self._controller.randomMap()
        elif choice == '2':
            self._isMapLoaded = True
            self._controller.loadMap()
        elif choice == '3':
            if self._isMapLoaded:
                self._controller.saveMap()
            else:
                print("Please load map first")
        elif choice == '4':
            if self._isMapLoaded:
                mapWithDrone(self._controller.getMap(), self._controller.getDronePosition())
            else:
                print("Please load map first")
        else:
            print("Invalid choice")

    def handleAlgorithmOptions(self):
        self.printAlgorithmMenu()
        choice = input(">")
        if choice == '1':
            self.setupParameters()
        elif choice == '2':
            self.runSolverOnce()
        elif choice == '3':
            self.runSolverMultipleTimes()
        elif choice == '4':
            self.visualiseStatistics()
        elif choice == '5':
            self.droneOnPath()
        else:
            print("Invalid choice")

    def run(self):
        while True:
            self.printMainMenu()
            choice = input(">")

            if choice == '1':
                self.handleMapOptions()
            elif choice == '2':
                self.handleAlgorithmOptions()
            elif choice == '0':
                return
            else:
                print("Invalid choice")