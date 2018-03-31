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
    departure = StringProperty("XXX")
    departure_time = StringProperty("HH:MM")
    arrival = StringProperty("XXX")
    arrival_time = StringProperty("HH:MM")


    def __init__(self, duty, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.date = duty.start.strftime(date_format)
        self.nature = duty.nature
        self.departure = duty.departure
        self.departure_time = duty.start.strftime(time_format)
        self.arrival = duty.arrival
        self.arrival_time = duty.end.strftime(time_format)


if __name__ == "__main__":
    from kivy.app import App

    duty1 = Duty()
    duty1.fromDict(
        {
            "nature": "FLIGHT",
            "start": "2018-04-05 08:35",
            "end": "2018-04-05 17:30",
            "duration": "08:55",
            "departure": "MCT",
            "arrival": "MUC",
            "flights": [
                {
                    "flight_number": "A FNum",
                    "start": "2017-04-05 10:05",
                    "end": "2017-04-05 17:00",
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
            "start": "2017-04-07 20:00",
            "end": "2017-04-08 19:59",
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
            "start": "2017-04-09 02:00",
            "end": "2017-04-09 14:00",
            "duration": "12:00",
            "departure": "MCT",
            "arrival": "MCT",
            "flights": []
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

    test.run()
