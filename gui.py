from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
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

    menu_expanded = BooleanProperty(False)
    central_widget = ObjectProperty(None)
    menu_widget = ObjectProperty(None)

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



    def onMenuButton(self):
        """ Toggle menu or central widget, and menu_expanded value"""
        if self.menu_expanded:
            self.menu_widget.clear_widgets()
            self.menu_widget.size_hint_y = None
            self.menu_widget.height = 0
            self._centralWidgetUpdate()
            self.central_widget.size_hint_y = 1
        else:
            self.central_widget.clear_widgets()
            self.central_widget.size_hint_y = None
            self.central_widget.height = 0
            menu = Menu()
            self.menu_widget.add_widget(menu)
            self.menu_widget.size_hint_y = 1
        self.menu_expanded = not self.menu_expanded


    def _centralWidgetUpdate(self):
        # Central widget update
        self.central_widget.clear_widgets()
        duty_list = self.controller.getLastToNextThreeDuties()
        for duty in duty_list:
            duty_widget = DutyWidget(duty)
            self.central_widget.add_widget(duty_widget)