import json
from datetime import datetime

from WYOB_error import WYOBError
from duty import Duty
from database import Database

datetime_format = "%Y-%m-%d %H:%M"


class Controller:

    duties = []
    database = Database()

    def update(self):
        self.database.updateFromIOB()
        self.duties = self.database.getDuties()
        # TODO: last updated feature (App state file?)
        update_data = {
            "last_updated": self.getLastUpdated() or "?",
            "next_duty": self.getNextDutyOrLegs(),
            "next_reporting": self.getNextReporting()
        }
        return update_data

    def getLastUpdated(self):
        if isinstance(self.database.update_time, datetime):
            return self.database.update_time.strftime(datetime_format)
        else:
            "?"

    def getLastToNextThreeDuties(self):
        """
        Temporary method, awaiting for RecycleView implementation
        :return: [duties] the required duties
        """
        result = []
        now = datetime.utcnow().astimezone()
        current_or_last_index = None
        # 1. Get the next duty index:
        for i in range(len(self.duties)):
            duty = self.duties[i]
            if duty.end > now:
                current_or_last_index = i
                break

        # 2. Set starting index "one step beyond!"
        if current_or_last_index and current_or_last_index > 0:
            starting_index = current_or_last_index - 1
        else:
            starting_index = 0

        # 3. Then get the next 5 duties (if it exists!)
        index = starting_index
        while index < len(self.duties) and index < starting_index + 5:
            result.append(self.duties[index])
            index += 1

        return result


    def getNextDuty(self):
        now = datetime.utcnow().astimezone()
        for duty in self.duties:
            if duty.start > now and duty.nature != 'OFF':
                return duty
        return None

    def getNextDutyOrLegs(self):
        duty = self.getNextDuty()
        if not duty:
            return "UNKNOWN"
        if duty.nature == "FLIGHT":
            result = duty.flights[0].departure
            for flight in duty.flights:
                result += " - " + flight.arrival
            return result
        else:
            return duty.nature

    def getNextReporting(self):
        duty = self.getNextDuty()
        if not duty:
            return "UNKNOWN"
        return duty.start.strftime(datetime_format)

    def loadDutiesFromJson(self, file):
        """ OBSOLETE
            Do not use!
        """
        try:
            with open(file, 'r') as file:
                try:
                    raw_duties_list = json.load(file)
                    for raw_duty in raw_duties_list:
                        duty = Duty()
                        duty.fromDict(raw_duty)
                        self.duties.append(duty)
                except json.JSONDecodeError as error:
                    raise WYOBError(
                        "Error while decoding current JSON file: " +
                        str(file) + ". Error sent from JSON: " +
                        str(error.msg))
        except OSError as error:
            raise WYOBError("Error trying to open " + str(file) +
                            ". Error from system: " + str(error))
