# duty.py
""" This file contains the Duty class
"""
from datetime import datetime, timedelta
import re

from WYOB_error import WYOBError
from flight import Flight

datetime_format = "%Y-%m-%d %H:%M %z"


class Duty:

    NATURES = [
        'OFF',
        'FLIGHT',
        'STANDBY',
        'GROUND',
    ]

    def __init__(self):
        self.nature = None
        self.start = None
        self.end = None
        self.duration = None
        self.departure = None
        self.arrival = None

        self.flights = []

        self.rest = None  # TODO!

    def __str__(self):
        result = (
            "***DUTY***|NATURE: {}|START: {}|END: {}|DURATION: {}|DEP: {}|ARR: {}|"
            .format(self.nature,
                    self.start.strftime(datetime_format) if self.start else "",
                    self.end.strftime(datetime_format) if self.end else "",
                    self.durationString,
                    self.departure, self.arrival))
        for flight in self.flights:
            result += '\n' + str(flight)
        return result

    def asDict(self):
        # returns a jsonable dict
        flight_list = []
        for flight in self.flights:
            flight_list.append(flight.asDict())
        return {
            "nature": self.nature,
            "start": self.start.strftime(datetime_format) if self.start else "",
            "end": self.end.strftime(datetime_format) if self.end else "",
            "duration": self.durationString,
            "departure": self.departure,
            "arrival": self.arrival,
            "flights": flight_list
        }

    def fromDict(self, data):
        """
        Takes a JSON object as parameter and populate attributes
        :param data: JSON object representing a duty
        """
        self.nature = data['nature']
        self.setStart(datetime.strptime(data['start'], datetime_format))
        self.setEnd(datetime.strptime(data['end'], datetime_format))
        self.departure = data['departure']
        self.arrival = data['arrival']
        for raw_flight in data['flights']:
            flight = Flight()
            flight.fromDict(raw_flight)
            self.addFlight(flight)

    # PROPERTIES
    @property
    def isValid(self):
        if (self.nature is None or self.nature not in self.NATURES or
                self.start is None or not isinstance(self.start, datetime) or
                self.end is None or not isinstance(self.end, datetime) or
                self.duration is None or
                not isinstance(self.duration, timedelta) or
                self.departure is None):
            return False
        return True

    # PUBLIC METHODS
    def addFlight(self, flight):
        if type(flight) == Flight:
            self.flights.append(flight)
            self.departure = self.flights[0].departure
            self.arrival = flight.arrival
        else:
            raise WYOBError(
                "Flight.addFlight called with wrong object type! Object: " +
                str(flight)
            )

    def setNatureFromIOBCodes(self, aString):
        """ This function sets the nature if possible and return True.
            If not possible, return False
        """
        flight_pattern = re.compile('\d{3}-\d{2}')
        if aString.count('OFF') > 0:
            self.nature = 'OFF'
        elif (aString.count('HS-AM') > 0 or aString.count('HS-PM') > 0 or
              aString.count('HS2') > 0):  # TODO!
            self.nature = 'STANDBY'
        elif re.match(flight_pattern, aString) is not None:
            self.nature = 'FLIGHT'
        else:
            return False
        return True

    def setStart(self, start_time):
        if isinstance(start_time, datetime):
            self.start = start_time
        else:
            raise WYOBError("Duty.setStart wrong type!")
        if self.end:
            self.updateDuration()

    def setEnd(self, end_time):
        if isinstance(end_time, datetime):
            self.end = end_time
        else:
            raise WYOBError("Duty.setEnd wrong type!")
        if self.start:
            self.updateDuration()

    # PRIVATE METHODS
    @property
    def durationString(self):
        """ returns 'HH:MM' """
        if self.duration is None:
            return "--:--"
        seconds = self.duration.total_seconds()
        hours = int(seconds // 3600)
        minutes = int(seconds // 60 - hours * 60)
        hoursString = str(hours) if hours > 9 else "0" + str(hours)
        minutesString = str(minutes) if minutes > 9 else "0" + str(minutes)
        return hoursString + ':' + minutesString

    def updateDuration(self):
        self.duration = self.end - self.start


if __name__ == '__main__':
    print("Duty class basic tests:")
    duty = Duty()
    print(duty)
    if duty.isValid:
        print("FAILED isValid returned true where it should be false!")
    else:
        print("PASSED isValid returned false with an empty Duty!")

    try:
        duty.addFlight(0)
    except WYOBError as e:
        print("PASSED addFlight with wrong argument. Message:\n\t" + str(e))

    duty.nature = "FLIGHT"
    duty.start = datetime.now()
    duty.end = duty.start + timedelta(minutes=453)
    duty.updateDuration()
    duty.departure = 'CDG'
    print(duty)
    if duty.isValid:
        print("PASSED isValid returned true for a correct duty")
    else:
        print("FAILED isValid returned false for a correct duty")
