import numpy as np


class Values:

    CELL_SIZE = 50

    values = {
        # fixed
        "CELL_SIZE": CELL_SIZE,
        "SCREEN_WIDTH": CELL_SIZE * 20,
        "SCREEN_HEIGHT": CELL_SIZE * 20,
        "MOVEMENT_SPEED": 0.8,

        # adjustable in settings
        "Number_Of_Rays": 1,
        "Max_Reflections": 5,
        "Decay_Factor": 1.5,
        "Field_Of_View": np.pi / 6,
        "Refractive_Index": 1.5,

        "Reflection_Mode": "Reflection",
    }

    def get_value(key):
        return Values.values[key]
    
    def set_value(key, value):
        Values.values[key] = value

    def set_toggle_value(value):
        if value == "Reflection_Mode":
            Values.set_value("Reflection_Mode", "Reflection")
        elif value == "Refraction_Mode":
            Values.set_value("Reflection_Mode", "Refraction")
        else:
            raise ValueError("Invalid toggle value.")
    
