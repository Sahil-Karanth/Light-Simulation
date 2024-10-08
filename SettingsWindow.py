import FreeSimpleGUI as sg
from values import Values
import numpy as np
import sys

sg.theme("SystemDefault")

class SettingsWindow:

    TOGGLE_PAIRS = {
        "Reflection_Mode": "Refraction_Mode",
        "Refraction_Mode": "Reflection_Mode",
    }

    def __init__(self):
        self.window = sg.Window("Settings", self.__create_layout())
        self.selected_buttons = ["Reflection_Mode"]

    def __create_slider(self, min_value, max_value, step, label):

        key = label.replace(" ", "_")

        if key == "Field_Of_View":
            default_value = Values.get_value(key) * 180 / np.pi
        
        else:
            default_value = Values.get_value(key)

        slider = sg.Slider(
            key=key,
            range=(min_value, max_value),
            orientation="h",
            size=(15, 15),
            default_value=default_value,
            resolution=step,
        )

        label_text = sg.Text(label, justification="center")

        layout = [
            [label_text],
            [slider],
        ]

        return sg.Column(layout, justification="center")
    

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
            [self.__create_slider(1, 100, 1, "Number Of Rays")],
            [self.__create_slider(0, 20, 1, "Max Reflections")],
            [self.__create_slider(1, 5, 0.2, "Decay Factor")],
            [self.__create_slider(10, 360, 1, "Field Of View")],
            [self.__create_slider(1, 5, 0.2, "Refractive Index")],
            [self.__create_toggle_button("Reflection Mode", "Refraction Mode")],
            [apply_button]
        ]

        return layout
    
    def __apply_settings(self, values):

        # update from sliders
        Values.set_value("Number_Of_Rays", int(values["Number_Of_Rays"]))
        Values.set_value("Max_Reflections", int(values["Max_Reflections"]))
        Values.set_value("Decay_Factor", float(values["Decay_Factor"]))
        Values.set_value("Field_Of_View", float(values["Field_Of_View"]) * np.pi / 180)
        Values.set_value("Refractive_Index", float(values["Refractive_Index"]))

        # update from toggle states
        for button in self.selected_buttons:
            Values.set_toggle_value(button)


    def __handle_toggle_change(self, event):

        # if the button is already selected, do nothing
        if event in self.selected_buttons:
            return

        self.selected_buttons.append(event)
        self.selected_buttons.remove(self.TOGGLE_PAIRS[event])

        self.window[event].update(button_color=("white", "green"))
        self.window[self.TOGGLE_PAIRS[event]].update(button_color=("black", "white"))

    def run(self):
        while True:
            event, values = self.window.Read()
            if event is None or event == "Cancel":
                sys.exit(0)

            if event == "Apply":
                self.__apply_settings(values)
                break

            if event in self.TOGGLE_PAIRS:
                self.__handle_toggle_change(event)

        self.window.Close()
