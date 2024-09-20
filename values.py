import numpy as np


class Values:

    CELL_SIZE = 50
    SCREEN_WIDTH = CELL_SIZE * 14
    SCREEN_HEIGHT = CELL_SIZE * 14
    MOVEMENT_SPEED = CELL_SIZE / 250
    NUM_RAYS = 20
    MAX_REFLECTIONS = 2
    DECAY_FACTOR_REFLECTION = 2
    FOV = np.pi / 6
    REFLECTION_MODE = "reflection"
    REFLECTION_TYPE = "specular"
    CAST_TYPE = "primitive"
    
