from datetime import datetime

datetime_format = "%Y-%m-%d %H:%M %z"


class Flight:

    def __init__(self):

        self.start = None
        self.end = None
        self.duration = None
        self.flight_number = None
        self.departure = None
        self.arrival = None

    def __str__(self):
        result = (
            "**FLIGHT**|FLIGHT NUMBER: {}|START: {}|END: {}|DURATION: {}|DEP: {}|ARR: {}|"
            .format(self.flight_number,
                    self.start.strftime(datetime_format) if self.start else "",
                    self.end.strftime(datetime_format) if self.end else "",
                    self.durationString, self.departure, self.arrival))
        return result

    def asDict(self):
        return {
            "flight_number": self.flight_number,
            "start": (self.start.strftime(datetime_format)
                      if self.start else ""),
            "end": self.end.strftime(datetime_format) if self.end else "",
            "duration": self.durationString,
            "departure": self.departure,
            "arrival": self.arrival
        }

    def fromDict(self, data):
        """
        Populate Flight attributes from a relevant JSON object
        :param data: JSON object representing a Flight
        """
        self.flight_number = data['flight_number']
        self.setStart(datetime.strptime(data['start'], datetime_format))
        self.setEnd(datetime.strptime(data['end'], datetime_format))
        self.departure = data['departure']
        self.arrival = data['arrival']

    def setStart(self, start_time):
        self.start = start_time
        if self.end:
            self.updateDuration()

    def setEnd(self, end_time):
        self.end = end_time
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
