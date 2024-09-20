import FreeSimpleGUI as sg

sg.theme("Black")

class SettingsWindow:

    def __init__(self):
        self.window = sg.Window("Settings", self.__create_layout())

    def __create_slider(self, min_value, max_value, step, label):
        slider = sg.Slider(
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

    def __create_layout(self):

        layout = [
            [self.__create_slider(1, 100, 1, "Cell Size")],
            [self.__create_slider(1, 100, 1, "Number of Rays")],
            [self.__create_slider(1, 100, 1, "Max Reflections")],
            [self.__create_slider(1, 100, 1, "Decay Factor Reflection")],
            [self.__create_slider(1, 100, 1, "Field of View")],
            [sg.Button("OK"), sg.Button("Cancel")],
        ]

        return layout

    def run(self):
        while True:
            event, values = self.window.Read()
            if event is None or event == "Cancel":
                break
            print("You entered ", values[0])
        self.window.Close()


window = SettingsWindow()

window.run()
