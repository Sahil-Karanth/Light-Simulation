import FreeSimpleGUI as sg

sg.theme("SystemDefault")

class SettingsWindow:

    def __init__(self):
        self.window = sg.Window("Settings", self.__create_layout())

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
        button1 = sg.Button(label1, visible=True, key=label1)
        button2 = sg.Button(label2, visible=False, key=label2, button_color=("white", "green"))

        layout = [
            [button1, button2],
        ]

        return sg.Column(layout, justification="center")


    def __create_layout(self):

        layout = [
            [self.__create_slider(1, 100, 1, "Number of Rays")],
            [self.__create_slider(1, 100, 1, "Max Reflections")],
            [self.__create_slider(1, 100, 1, "Decay Factor")],
            [self.__create_slider(1, 100, 1, "Field of View")],
            [self.__create_toggle_button("Reflection Mode", "Refraction Mode")],
            [self.__create_toggle_button("Specular Reflection", "Diffuse Reflection")],
            [self.__create_toggle_button("Primitive Cast", "DDA Cast")],
        ]

        return layout
    
    def __apply_settings(self, values):
        print(values)

    def run(self):
        while True:
            event, values = self.window.Read()
            if event is None or event == "Cancel":
                print(values)
                self.__apply_settings(values)
                break

        self.window.Close()


window = SettingsWindow()

window.run()
