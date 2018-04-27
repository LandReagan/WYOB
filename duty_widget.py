from datetime import timezone

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file("duty_widget.kv")
date_format = "%d%b%y"
time_format = "%H:%M"


class DutyWidget(BoxLayout):
    """
    It shows a Duty instance data
    """

    date = StringProperty("DD-MM-YY")
    nature = StringProperty("NNNNNN")
    legs = StringProperty("XXX - XXX")
    departure_time_local = StringProperty("HH:MM")
    departure_time_utc = StringProperty("HH:MM")
    arrival_time_local = StringProperty("HH:MM")
    arrival_time_utc = StringProperty("HH:MM")

    def __init__(self, duty, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.date = duty.start.strftime(date_format)
        self.nature = duty.nature
        self.departure_time_local = duty.start.strftime(time_format)
        self.arrival_time_local = duty.end.strftime(time_format)
        self.buildLegs(duty)
        self.buildUtcTimes(duty)

    def buildLegs(self, duty):
        if duty.nature == 'FLIGHT':
            legs = duty.flights[0].departure
            for flight in duty.flights:
                legs += " - " + flight.arrival
            self.legs = legs
        else:
            self.legs = duty.departure + " - " + duty.arrival

    def buildUtcTimes(self, duty):
        self.departure_time_utc = (
            duty.start.astimezone(tz=timezone.utc).strftime(time_format) + 'z')
        self.arrival_time_utc = (
            duty.end.astimezone(tz=timezone.utc).strftime(time_format) + 'z')
