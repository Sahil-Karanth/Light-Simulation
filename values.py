import numpy as np


class Values:

    CELL_SIZE = 50

    values = {
        # fixed
        "CELL_SIZE": CELL_SIZE,
        "SCREEN_WIDTH": CELL_SIZE * 20,
        "SCREEN_HEIGHT": CELL_SIZE * 20,
        "MOVEMENT_SPEED": 0.8,
        "Refractive_Index": 2,

        # adjustable in settings
        "Number_Of_Rays": 1,
        "Max_Reflections": 0,
        "Decay_Factor": 1.5,
        "Field_Of_View": np.pi / 6,

        "Reflection_Mode": "reflection",
        "Reflection_Type": "specular",
        "Cast_Type": "Primitive_Cast"
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
            Values.set_value("Cast_Type", "Primitive_Cast")
        elif value == "DDA_Cast":
            Values.set_value("Cast_Type", "DDA_Cast")
        else:
            raise ValueError("Invalid toggle value.")
    

# sweeping along bottom from left to right

# good detect Vector([17.981726958102346, 19.001139204461822]) Vector([17.91363742801092, 18.92790112767161])
# bad detect Vector([18.06259638362433, 19.062485341963374]) Vector([17.994442632952854, 18.98930702366205])
# good detect Vector([18.076307730275673, 19.049703378861583]) Vector([18.00808507836474, 18.97658929153062])