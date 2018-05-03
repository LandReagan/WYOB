from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder

from controller import Controller
from menu import Menu
from duty_widget import DutyWidget

Builder.load_file("gui.kv")


class GUI(BoxLayout):

    utc_clock = StringProperty("HH:MM GMT")
    loc_clock = StringProperty("HH:MM LOC")
    last_updated = StringProperty("?")
    next_duty = StringProperty("?")
    next_reporting = StringProperty("?")

    central_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.clockSetUp()
        self.controller = Controller()
        self.update()

    def clockSetUp(self):
        Clock.schedule_interval(self.clockUpdate, 0.2)

    def clockUpdate(self, dt):
        self.utc_clock = datetime.utcnow().strftime('%H:%M:%S GMT')
        self.loc_clock = datetime.now().strftime('%H:%M:%S LOC')

    def update(self):
        update_data = self.controller.update()

        # Header data update
        self.last_updated = update_data['last_updated']
        self.next_duty = update_data['next_duty']
        self.next_reporting = update_data['next_reporting']

        # Central widget update
        self.central_widget.clear_widgets()
        duty_list = self.controller.getLastToNextThreeDuties()
        for duty in duty_list:
            duty_widget = DutyWidget(duty)
            self.central_widget.add_widget(duty_widget)

    def showMenu(self):
        self.add_widget(Menu())