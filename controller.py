import json
from datetime import datetime

from logger import logI
from WYOB_error import WYOBError
from IOBConnect import IOBConnect
from duty import Duty

datetime_format = "%Y-%m-%d %H:%M"


class Controller:

    current_file = "current.json"
    duties = []

    def update(self):
        self.updateFromIOB()
        # TODO: last updated feature (App state file?)
        update_data = {
            "last_updated": self.getLastUpdated(),
            "next_duty": self.getNextDutyOrLegs(),
            "next_reporting": self.getNextReporting()
        }
        return update_data

    def updateFromIOB(self):
        logI("Updating from IOB...")
        iobconnector = IOBConnect('93429', '93429')
        try:
            file = iobconnector.run()
            # TODO: copy file into current_file
        except WYOBError as error:
            logI("Unable to connect, continuing offline...")
        self.loadDutiesFromJson()

    def getLastUpdated(self):
        return "???"

    def getNextDuty(self):
        now = datetime.utcnow()
        for duty in self.duties:
            if duty.start > now:
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

    def loadDutiesFromJson(self):
        try:
            with open(self.current_file, 'r') as file:
                try:
                    raw_duties_list = json.load(file)
                    for raw_duty in raw_duties_list:
                        duty = Duty()
                        duty.fromDict(raw_duty)
                        self.duties.append(duty)
                except json.JSONDecodeError as error:
                    raise WYOBError(
                        "Error while decoding current JSON file: " +
                        self.current_file + ". Error sent from JSON: " +
                        str(error.msg))
        except OSError as error:
            raise WYOBError("Error trying to open " + str(self.current_file) +
                            ". Error from system: " + str(error))


if __name__ == "__main__":

    controller = Controller()
    controller.updateFromIOB()

