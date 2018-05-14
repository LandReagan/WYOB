# duty.py
""" This file contains the Duty class
"""
from datetime import datetime, timedelta
import re

from WYOB_error import WYOBError
from flight import Flight
from utils27 import parseDateTime

datetime_format = "%Y-%m-%d %H:%M %z"
key_datetime_format = "%Y%m%d%H%M"


class Duty:

    NATURES = [
        'OFF',
        'FLIGHT',
        'STANDBY',
        'GROUND',
        'UNKNOWN',
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
        self.setStart(parseDateTime(data['start']))
        self.setEnd(parseDateTime(data['end']))
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

    @property
    def key(self):
        return (
            "{}_{}_{}_{}_{}"
            .format(self.nature,
                self.start.strftime(key_datetime_format) if self.start else "?",
                self.end.strftime(key_datetime_format) if self.end else "?",
                self.departure, self.arrival))

    # PUBLIC METHODS
    def addFlight(self, flight):
        if isinstance(flight, Flight):
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

        # 1. OFF
        if aString.count('OFF') > 0 or aString.count('ROF') > 0:
            self.nature = 'OFF'
        # 2. STANDBY
        elif (aString.count('HS-AM') > 0 or aString.count('HS-PM') > 0 or
              aString.count('HS2') > 0):  # TODO!
            self.nature = 'STANDBY'
        # 3. FLIGHT
        elif re.match(flight_pattern, aString) is not None:
            self.nature = 'FLIGHT'
        # 4. TRAINING
        elif (aString.count('SEC') > 0 or aString.count('CRM') > 0 or
                aString.count('PDC') > 0 or aString.count('SEP') > 0 or
                aString.count('TECREF') > 0):
            self.nature = 'TRAINING'
        # 5. UNKNOWN
        else:
            self.nature = 'UNKNOWN'
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
