import numpy as np


class Values:

    CELL_SIZE = 50

    values = {
        # fixed
        "CELL_SIZE": CELL_SIZE,
        "SCREEN_WIDTH": CELL_SIZE * 14,
        "SCREEN_HEIGHT": CELL_SIZE * 14,
        "MOVEMENT_SPEED": CELL_SIZE / 250,

        # adjustable in settings
        "Number_Of_Rays": 5,
        "Max_Reflections": 2,
        "Decay_Factor": 1.5,
        "Field_Of_View": np.pi / 6,

        "Reflection_Mode": "reflection",
        "Reflection_Type": "specular",
        "Cast_Type": "primitive"
    }

    def get_value(key):
        return Values.values[key]
    
    def set_value(key, value):
        Values.values[key] = value
    
