from datetime import timezone

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

from duty import Duty

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

if __name__ == "__main__":
    from kivy.app import App

    duty1 = Duty()
    duty1.fromDict(
        {
            "nature": "FLIGHT",
            "start": "2018-04-05 12:35 +0400",
            "end": "2018-04-05 19:30 +0200",
            "duration": "08:55",
            "departure": "MCT",
            "arrival": "MUC",
            "flights": [
                {
                    "flight_number": "A FNum",
                    "start": "2017-04-05 14:05 +0400",
                    "end": "2017-04-05 19:00 +0200",
                    "duration": "06:55",
                    "departure": "MCT",
                    "arrival": "MUC"
                }
            ]
        }
    )
    duty2 = Duty()
    duty2.fromDict(
        {
            "nature": "OFF",
            "start": "2017-04-08 00:00 +0400",
            "end": "2017-04-08 23:59 +0400",
            "duration": "23:59",
            "departure": "MCT",
            "arrival": "MCT",
            "flights": []
        }
    )
    duty3 = Duty()
    duty3.fromDict(
        {
            "nature": "STANDBY",
            "start": "2017-04-09 06:00 +0400",
            "end": "2017-04-09 18:00 +0400",
            "duration": "12:00",
            "departure": "MCT",
            "arrival": "MCT",
            "flights": []
        }
    )
    duty4 = Duty()
    duty4.fromDict(
        {
            "nature": "FLIGHT",
            "start": "2018-04-28 20:15 +0400",
            "end": "2018-04-29 08:00 +0400",
            "duration": "11:45",
            "departure": "MCT",
            "arrival": "MCT",
            "flights": [
                {
                    "flight_number": "WY671 ",
                    "start": "2018-04-28 22:15 +0400",
                    "end": "2018-04-29 01:25 +0300",
                    "duration": "03:10",
                    "departure": "MCT",
                    "arrival": "JED"
                },
                {
                    "flight_number": "WY672 ",
                    "start": "2018-04-29 04:20 +0300",
                    "end": "2018-04-29 07:30 +0400",
                    "duration": "03:10",
                    "departure": "JED",
                    "arrival": "MCT"
                }
            ]
        }
    )


    class Test(App):

        boxlayout = BoxLayout(orientation="vertical")

        def build(self):
            return self.boxlayout

    test = Test()
    test.boxlayout.add_widget(DutyWidget(duty1))
    test.boxlayout.add_widget(DutyWidget(duty2))
    test.boxlayout.add_widget(DutyWidget(duty3))
    test.boxlayout.add_widget(DutyWidget(duty4))

    test.run()
