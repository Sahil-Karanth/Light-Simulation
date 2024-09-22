import numpy as np


class Values:

    CELL_SIZE = 50

    values = {
        # fixed
        "CELL_SIZE": CELL_SIZE,
        "SCREEN_WIDTH": CELL_SIZE * 14,
        "SCREEN_HEIGHT": CELL_SIZE * 14,
        "MOVEMENT_SPEED": 0.8,
        "Refractive_Index": 2,

        # adjustable in settings
        "Number_Of_Rays": 1,
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

    def set_toggle_value(value):
        if value == "Reflection_Mode":
            Values.set_value("Reflection_Mode", "Reflection")
        elif value == "Refraction_Mode":
            Values.set_value("Reflection_Mode", "Refraction")
        elif value == "Specular_Reflection":
            Values.set_value("Reflection_Type", "Specular")
        elif value == "Diffuse_Reflection":
            Values.set_value("Reflection_Type", "Diffuse")
        elif value == "Primitive_Cast":
            Values.set_value("Cast_Type", "Primitive")
        elif value == "DDA_Cast":
            Values.set_value("Cast_Type", "DDA")
        else:
            raise ValueError("Invalid toggle value.")
    
