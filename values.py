import numpy as np


class Values:

    CELL_SIZE = 50

    values = {
        # fixed
        "CELL_SIZE": CELL_SIZE,
        "SCREEN_WIDTH": CELL_SIZE * 20,
        "SCREEN_HEIGHT": CELL_SIZE * 20,
        "MOVEMENT_SPEED": 0.8,
        "Refractive_Index": 1.5,

        # adjustable in settings
        "Number_Of_Rays": 1,
        "Max_Reflections": 5,
        "Decay_Factor": 1.5,
        "Field_Of_View": np.pi / 6,

        "Reflection_Mode": "Reflection",
        "TIR_Mode": "TIR_ON"
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

        elif value == "TIR_On":
            Values.set_value("TIR_Mode", "TIR_ON")
        
        elif value == "TIR_Off":
            Values.set_value("TIR_Mode", "TIR_OFF")
            
        else:
            raise ValueError("Invalid toggle value.")
    

# sweeping along bottom from left to right

# good detect Vector([17.981726958102346, 19.001139204461822]) Vector([17.91363742801092, 18.92790112767161])
# bad detect Vector([18.06259638362433, 19.062485341963374]) Vector([17.994442632952854, 18.98930702366205])
# good detect Vector([18.076307730275673, 19.049703378861583]) Vector([18.00808507836474, 18.97658929153062])