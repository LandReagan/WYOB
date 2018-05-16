# database.py
""" This file contains required classes to access the JSON database
BIG TODO:
- Usage:
    => Class with methods to call - DONE
- Ensure database consistency
    => save a copy before changing
    => copy it back in case of error
    => Change only what is required - DONE
"""
from os.path import join

from kivy.storage.jsonstore import JsonStore
from kivy.logger import Logger

import config
from WYOB_error import WYOBError
from IOBConnect import IOBConnect
from duty import Duty
from utils27 import parseDateTime

datetime_format = "%Y-%m-%d %H:%M %z"


class Database:

    update_time = None
    storage = None

    def getDuties(self, start_date=None, end_date=None):
        """ Getter for duties in the database, from datetime to datetime.
            If related parameter is missing, it will take all possible duties.
            Result is sorted by ascending start time.
        """
        duties = []
        self._connectStorage()

        for key in self.storage:
            if key == 'header':
                self.update_time = parseDateTime(self.storage.get('header')['last_update'])
            else:
                duty = Duty()
                duty.fromDict(self.storage[key])
                if ((start_date is None or duty.start >= start_date) and
                        (end_date is None or duty.end <= end_date)):
                    duties.append(duty)

        self._disconnectStorage()

        duties = sorted(duties, key=lambda duty: duty.start)
        return duties

    def updateDuties(self, duties):
        """ Setter for duties in the database. Overlapping duties (in time
            period) are overwritten.
        """
        if not duties:
            return

        self._connectStorage()

        sorted(duties, key=lambda duty: duty.start)

        if duties and len(duties) > 0:
            startPeriod = duties[0].start
            endPeriod = duties[len(duties) - 1].end
        else:
            return

        # Erase updated duties:
        for key in list(self.storage):
            if key != 'header':
                duty = Duty()
                rawData = self.storage.get(key)
                if rawData:
                    duty.fromDict(rawData)
                    if duty.start >= startPeriod and duty.end <= endPeriod:
                        self.storage.delete(key)

        # Write updated duties:
        self.storage['header'] = {'last_update': self.update_time.strftime(datetime_format)}
        for duty in duties:
            self.storage[duty.key] = duty.asDict()
        Logger.info(str(len(duties)) + " new duties wrote in the storage")

        self._disconnectStorage()

    def updateFromIOB(self):
        duties = self._getIOBDuties()
        self.updateDuties(duties)
        if duties is None:
            return False
        else:
            return True

    # PRIVATE METHODS
    def _getIOBDuties(self):
        """ Use the connector to get duties from IOB system
        :return: [duties] a list of duties from IOB, or None in case of failure
        """
        iobconnector = IOBConnect('93429', '93429')
        try:
            duties, self.update_time = iobconnector.run()
            return duties
        except WYOBError:
            Logger.info("WYOB: Continuing offline!")
            return None

    def _connectStorage(self):
        try:
            self.storage = JsonStore(config.data_file_path)
        except BaseException as e:
            raise WYOBError("In Database._connectStorage, unexpected Error! " + str(e))
        Logger.info("Found " + str(self.storage.count()) + " entries in the storage " + config.data_file_path)

    def _disconnectStorage(self):
        self.storage = None
