from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file("gui.kv")


class GUI(BoxLayout):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

    def update(self):
        print("Update!")
