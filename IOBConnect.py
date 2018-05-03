import re
import json
import datetime
import requests

from kivy.logger import Logger

from parsers import TokenParser, DutyParser
from WYOB_error import WYOBError
from duty import Duty
from flight import Flight


class IOBConnect:
    """ This class connects to IOB system and handle requests.
    """

    IOBURL_login_filter = 'https://fltops.omanair.com/' +\
        'mlt/filter.jsp?window=filter&loggedin=false'
    IOBURL_checkin_list = 'https://fltops.omanair.com/' +\
        'mlt/checkinlist.jsp'
    duties = []

    def __init__(self, username=None, password=None):
        """ Gets username and password and initialize attributes
        """
        self._username = username
        self._password = password
        self._session = None
        self._token_parser = TokenParser()
        self._duty_parser = DutyParser()
        self.raw_duties = []

    def run(self):
        """
        This method connects and fetch the page, parse raw duties then create
        duties and return them with the current datetime object
        :return: duties,datetime.now()
        """
        text = None
        try:
            self.connect()
            text = self.getCheckinList()
        except Exception as e:
            raise WYOBError("Connection failed!")

        if text:
            self.parseDuties(text)
            self.buildDutiesAndFlights()
            return self.duties, datetime.datetime.now()
        else:
            return None

    def connect(self):
        """ create session and log in.
        """
        # 1. Check parameters
        if self._username is None or self._password is None \
                or not isinstance(self._username, str) \
                or not isinstance(self._password, str):
            raise WYOBError(
                'Couldn\'t connect to IOB due to invalid ' +
                'username and/or password'
            )
        self._session = requests.session()
        # 2. Trying to connect to IOB website and parsing the answer
        Logger.info("WYOB: Connecting to IOB...")
        try:
            req = self._session.get(self.IOBURL_login_filter)
            self._token_parser.feed(req.text)
        except requests.RequestException:
            self._session = None
            raise WYOBError('Connection error !')

        # 3. If parsing has failed, error is raised...
        if self._token_parser.token == '' or self._token_parser.new_URL == '':
            raise WYOBError('Error parsing logging form !')

        # 4. Create logging parameters
        values = {
            'token': self._token_parser.token,
            'username': self._username,
            'password': self._password
        }

        # 5. Log in
        self._session.post(self._token_parser.new_URL, data=values)

    def getCheckinList(self):
        req = self._session.get(self.IOBURL_checkin_list)
        return req.text

    def parseDuties(self, text):
        self._duty_parser.feed(text)
        for duty in self._duty_parser.duties:
            self.raw_duties.append(dict(zip(self._duty_parser.headers, duty)))

    def buildDutiesAndFlights(self):
        """
        Parses the raw strings to extract Duty and Flight instances
        """
        full_time_pattern = re.compile(
            r'\s*(\d{2}\w{3}\d{4})\s+?(\d{2}:\d{2})\s+?\((\d{2}:\d{2})\)\s*')
        leg_pattern = re.compile(r'\d')
        duty_pattern = re.compile(r'\S')
        airport_pattern = re.compile(r'\D{3}')
        trip_pattern = re.compile(r'\s*\w+\s*')

        for raw_duty in self.raw_duties:
            # Start
            start_match = re.match(full_time_pattern, raw_duty['Start'])
            if start_match:
                start_time = self.getTimeFromMatch(start_match)
            else:
                start_time = None
            # End
            end_match = re.match(full_time_pattern, raw_duty['End'])
            if end_match:
                end_time = self.getTimeFromMatch(end_match)
            else:
                end_time = None
            # Departure
            departure_match = re.match(airport_pattern, raw_duty['From'])
            if departure_match:
                departure = departure_match.group(0)
            else:
                departure = ""
            # Arrival
            arrival_match = re.match(airport_pattern, raw_duty['To'])
            if arrival_match:
                arrival = arrival_match.group(0)
            else:
                arrival = ""

            if re.match(leg_pattern, raw_duty['Leg']):
                flight = Flight()
                flight.flight_number = raw_duty['Flight']
                flight.setStart(start_time)
                flight.setEnd(end_time)
                flight.departure = departure
                flight.arrival = arrival
                last_duty = self.duties[len(self.duties) - 1]
                last_duty.addFlight(flight)

            elif (re.match(duty_pattern, raw_duty['Duty']) or
                  re.match(trip_pattern, raw_duty['Trip'])):
                duty = Duty()
                if not duty.setNatureFromIOBCodes(raw_duty['Trip']):
                    duty.nature = 'FLIGHT'
                duty.setStart(start_time)
                duty.setEnd(end_time)
                self.duties.append(duty)

    def writeToFile(self, file='lastLoad.json'):
        """ OBSOLETE
        Gets an optional JSON file name as parameter. If there is no file name,
        data is written in "lastLoad.json"
        :param file: optional file name
        :return file: the file where fresh JSON data has been written
        """
        try:
            with open(file, 'w') as file_stream:
                duties_dict_list = [
                    duty.asDict() for duty in self.duties
                ]
                json.dump(duties_dict_list, file_stream, indent=2) # TODO: Debug
        except OSError as e:
            raise WYOBError("In IOBConnect.writeToFile:\nFile: " + file +
                            " could not be opened. Reported error: " + str(e))
        return file

    def getTimeFromMatch(self, match):
        """
        Build a timezone aware datetime object to fully determine the match string
        :param match: a returned "match object" string
        :return: a datetime object, with correct time and timezone
        """
        raw_date_format = "%d%b%Y"
        raw_time_format = "%H:%M"
        raw_start_local_date = match.group(1)
        raw_start_local_time = match.group(2)
        raw_start_utc_time = match.group(3)
        try:
            local_date = datetime.datetime.strptime(
                raw_start_local_date, raw_date_format).date()
            local_time = datetime.datetime.strptime(
                raw_start_local_time, raw_time_format).time()
            local_datetime = datetime.datetime.combine(
                local_date, local_time)
            utc_time = datetime.datetime.strptime(
                raw_start_utc_time, raw_time_format).time()
            utc_datetime = datetime.datetime.combine(
                local_date, utc_time)
            if (local_datetime - utc_datetime <
                    datetime.timedelta(hours=-12)):
                utc_datetime += datetime.timedelta(days=-1)
            if (local_datetime - utc_datetime >
                    datetime.timedelta(hours=12)):
                utc_datetime += datetime.timedelta(days=1)
            gmt_diff = local_datetime - utc_datetime
            zone = datetime.timezone(gmt_diff)
            aware_local_datetime = local_datetime.replace(tzinfo=zone)
            return aware_local_datetime
        except Exception:
            raise WYOBError('Error setting up the date from IOB.')
