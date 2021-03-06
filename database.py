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

data_file = "data.json"


class Database:

    def __init__(self):
        pass

    def getDuties(self, start_date, end_date):
        """ getter for duties in the database """
        pass

    def getIOBFile(self):
        logI("Updating from IOB...")
        iobconnector = IOBConnect('93429', '93429')
        try:
            file = iobconnector.run()
            return file
        except WYOBError as error:
            logI("Unable to connect, continuing offline...")
            return None
