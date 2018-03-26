from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file("gui.kv")


class GUI(BoxLayout):

    clock = StringProperty("XX:XX GMT")

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.clockSetUp()

    def clockSetUp(self):
        Clock.schedule_interval(self.clockUpdate, 0.2)

    def clockUpdate(self, dt):
        self.clock = datetime.utcnow().strftime('%H:%M:%S GMT')

    def update(self):
        print("Update!")
