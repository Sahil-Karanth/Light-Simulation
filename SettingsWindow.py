import FreeSimpleGUI as sg
from values import Values
import numpy as np

sg.theme("SystemDefault")

class SettingsWindow:

    TOGGLE_PAIRS = {
        "Reflection_Mode": "Refraction_Mode",
        "Refraction_Mode": "Reflection_Mode",
        "Specular_Reflection": "Diffuse_Reflection",
        "Diffuse_Reflection": "Specular_Reflection",
        "Primitive_Cast": "DDA_Cast",
        "DDA_Cast": "Primitive_Cast"
    }

    def __init__(self):
        self.window = sg.Window("Settings", self.__create_layout())
        self.selected_buttons = ["Reflection_Mode", "Specular_Reflection", "Primitive_Cast"]

    def __create_slider(self, min_value, max_value, step, label):

        key = label.lower().replace(" ", "_")
        print(key)
        slider = sg.Slider(
            key=key,
            range=(min_value, max_value),
            orientation="h",
            size=(15, 15),
            default_value=(min_value + max_value) // 2,
            resolution=step,
        )

        label_text = sg.Text(label)

        layout = [
            [label_text],
            [slider],
        ]

        return sg.Column(layout, element_justification="center")
    

    def __create_toggle_button(self, label1, label2):

        button1 = sg.Button(label1, visible=True, key=label1.replace(" ", "_"), button_color=("white", "green"))
        button2 = sg.Button(label2, visible=True, key=label2.replace(" ", "_"), button_color=("black", "white"))

        layout = [
            [button1, button2],
        ]

        return sg.Column(layout, justification="center")


    def __create_layout(self):

        apply_button = sg.Column([[sg.Button("Apply", button_color=("white", "black"))]], justification="center", pad=(0, 20))

        layout = [
            [self.__create_slider(1, 100, 1, "Number of Rays")],
            [self.__create_slider(1, 100, 1, "Max Reflections")],
            [self.__create_slider(1, 100, 1, "Decay Factor")],
            [self.__create_slider(1, 100, 1, "Field of View")],
            [self.__create_toggle_button("Reflection Mode", "Refraction Mode")],
            [self.__create_toggle_button("Specular Reflection", "Diffuse Reflection")],
            [self.__create_toggle_button("Primitive Cast", "DDA Cast")],
            [apply_button]
        ]

        return layout
    
    def __apply_settings(self, values):

        # update Values class with new settings
        Values.NUM_RAYS = int(values["number_of_rays"])
        Values.MAX_REFLECTIONS = int(values["max_reflections"])
        Values.DECAY_FACTOR_REFLECTION = float(values["decay_factor"])
        Values.FOV = float(values["field_of_view"]) * np.pi / 180

        # update from toggle states
        for button in self.selected_buttons:
            if button == "Reflection_Mode":
                Values.REFLECTION_MODE = "reflection"
            elif button == "Refraction_Mode":
                Values.REFLECTION_MODE = "refraction"
            elif button == "Specular_Reflection":
                Values.REFLECTION_TYPE = "specular"
            elif button == "Diffuse_Reflection":
                Values.REFLECTION_TYPE = "diffuse"
            elif button == "Primitive_Cast":
                Values.CAST_TYPE = "primitive"
            elif button == "DDA_Cast":
                Values.CAST_TYPE = "dda"



    def __handle_toggle_change(self, event):
        self.selected_buttons.append(event)
        self.selected_buttons.remove(self.TOGGLE_PAIRS[event])

        self.window[event].update(button_color=("white", "green"))
        self.window[self.TOGGLE_PAIRS[event]].update(button_color=("black", "white"))

    def run(self):
        while True:
            event, values = self.window.Read()
            if event is None or event == "Cancel":
                break

            if event == "Apply":
                self.__apply_settings(values)
                break

            if event in self.TOGGLE_PAIRS:
                self.__handle_toggle_change(event)

        self.window.Close()
