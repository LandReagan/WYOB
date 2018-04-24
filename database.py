# database.py
""" This file contains required classes to access the JSON database
BIG TODO:
- Usage:
    => Class with methods to call
- Ensure database consistency
    => save a copy before changing
    => copy it back in case of error
    => Change only what is required
"""

from kivy.storage.jsonstore import JsonStore

from WYOB_error import WYOBError
from logger import logI
from IOBConnect import IOBConnect
from duty import Duty


class Database:

    data_file = "data.json"
    storage = None

    def __init__(self):
        pass

    def getDuties(self, start_date=None, end_date=None):
        """ ASYNCHRONOUS !
            getter for duties in the database, from datetime to datetime.
            If related parameter is missing, it will take all possible duties.
        """
        duties = []
        self._connectStorage()

        for key in self.storage:
            duty = Duty()
            duty.asDict(self.storage[key])
            if ((duty.start >= start_date or start_date is None) and
                    (duty.end <= end_date or end_date is None)):
                duties.append(duty)

        self._disconnectStorage()
        return duties

    def updateDuties(self, duties):
        """ ASYNCHRONOUS !
            Setter for duties in the database. Overlapping duties (in time
            period) are overwritten.
        """
        self._connectStorage()

        if len(duties) > 0:
            startPeriod = duties[0].start
            endPeriod = duties[len(duties) - 1].end
        else:
            return

        # Erase updated duties:
        for key in self.storage.keys:
            duty = Duty()
            duty.fromDict(self.storage.get(key))
            if duty.start >= startPeriod and duty.end <= endPeriod:
                self.storage.delete(key)

        # Write updated duties:
        for duty in duties:
            self.storage.put(duty.key, duty.asDict())

        self._disconnectStorage()


    def getIOBFile(self):
        logI("Updating from IOB...")
        iobconnector = IOBConnect('93429', '93429')
        try:
            file = iobconnector.run()
            return file
        except WYOBError:
            logI("Unable to connect, continuing offline...")
            return None

    # PRIVATE METHODS
    def _connectStorage(self):
        try:
            self.storage = JsonStore(self.data_file)
        except BaseException as e:
            raise WYOBError("In Database._getStorage, unexpected Error!")

    def _disconnectStorage(self):
        self.storage = None


if __name__ == "__main__":

    db = Database()
    db.data_file = "test_data.json"

    with open("test.txt", "r") as file:
        pass
