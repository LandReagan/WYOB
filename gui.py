from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder

from logger import logI
from controller import Controller
from menu import Menu

Builder.load_file("gui.kv")


class GUI(BoxLayout):

    utc_clock = StringProperty("HH:MM GMT")
    loc_clock = StringProperty("HH:MM LOC")
    last_updated = StringProperty("?")
    next_duty = StringProperty("?")
    next_reporting = StringProperty("?")

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.clockSetUp()
        self.controller = Controller()

    def clockSetUp(self):
        Clock.schedule_interval(self.clockUpdate, 0.2)

    def clockUpdate(self, dt):
        self.utc_clock = datetime.utcnow().strftime('%H:%M:%S GMT')
        self.loc_clock = datetime.now().strftime('%H:%M:%S LOC')

    def update(self):
        logI("Update!")
        update_data = self.controller.update()
        self.last_updated = update_data['last_updated']
        self.next_duty = update_data['next_duty']
        self.next_reporting = update_data['next_reporting']

    def showMenu(self):
        self.add_widget(Menu())