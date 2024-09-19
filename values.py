import numpy as np


class Values:

    CELL_SIZE = 50
    SCREEN_WIDTH = CELL_SIZE * 14
    SCREEN_HEIGHT = CELL_SIZE * 14
    MOVEMENT_SPEED = CELL_SIZE / 250
    NUM_RAYS = 5
    MAX_REFLECTIONS = 10
    DECAY_FACTOR_REFLECTION = 2
    FOV = np.pi / 6
