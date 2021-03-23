BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PURPLE = (205, 180, 219)
PINK = (255, 175, 204)
BABY_BLUE = (162, 210, 255)
BABY_ORANGE = (254, 216, 177)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
DRONE_DIRECTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]

ROWS = 30
COLUMNS = 20

SQUARE_SIDE_SIZE = 20
SQUARE_WIDTH = 20
SQUARE_HEIGHT = 20

# steps the drone can move before the battery dies
INDIVIDUAL_LIFETIME = 100
POPULATION_SIZE = 5000
GENERATIONS = 1000

MUTATE_PROBABILITY = 0.04
CROSSOVER_PROBABILITY = 0.8

STEADY_STATE_NO_OFFSPRINGS = 1000
ERROR_FACTOR = 0