import requests
import re
import datetime

from parsers import TokenParser, DutyParser
from WYOB_error import WYOBError
from duty import Duty
from flight import Flight


class IOBConnect:
    """ This class connects to IOB system and handle requests iot fetch
        data. This include planned and completed flights.
    """
    IOBURL_login_filter = 'https://fltops.omanair.com/' +\
        'mlt/filter.jsp?window=filter&loggedin=false'
    IOBURL_checkin_list = 'https://fltops.omanair.com/' +\
        'mlt/checkinlist.jsp'
    duties_and_flights = []

    def __init__(self, username=None, password=None):
        """
        """
        self._username = username
        self._password = password
        self._session = None
        self._token_parser = TokenParser()
        self._duty_parser = DutyParser()
        self.raw_duties = []

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
        req = None
        # 2. Trying to connect to IOB website and parsing the answer
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
        req = self._session.post(self._token_parser.new_URL, data=values)

    def getCheckinList(self):
        req = self._session.get(self.IOBURL_checkin_list)
        return req.text

    def parseDuties(self, text):
        self._duty_parser.feed(text)
        for duty in self._duty_parser.duties:
            self.raw_duties.append(dict(zip(self._duty_parser.headers, duty)))

    def buildDutiesAndFlights(self):
        full_time_pattern = re.compile(
            r'\s*(\d{2}\w{3}\d{4})\s+?(\d{2}:\d{2})\s+?\((\d{2}:\d{2})\)\s*')
        leg_pattern = re.compile(r'\d')
        airp_pattern = re.compile(r'\D{3}')
        for raw_duty in self.raw_duties:
            print(raw_duty)
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

            if re.fullmatch(leg_pattern, raw_duty['Leg']):
                flight = Flight()
                # TODO: Implement Flight class first!
                self.duties_and_flights.append(flight)
            elif raw_duty['Duty']:
                duty = Duty()
                if duty.setNatureFromIOBCodes(raw_duty['Trip']):
                    duty.setStart(start_time)
                    duty.setEnd(end_time)
                    self.duties_and_flights.append(duty)
                print(duty)

    def getTimeFromMatch(self, match):
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
            # gmt_diff = datetime.timezone(local_datetime - utc_datetime)
            # print(gmt_diff)
            return utc_datetime
        except Exception:
            WYOBError('Error setting up the date from IOB.')
            raise


if __name__ == '__main__':

    iobconnect = IOBConnect(username='93429', password='93429')
    text = ''
    try:
        raise Exception()  # Clear that line to try online
        print("Trying to connect...")
        iobconnect.connect()
        text = iobconnect.getCheckinList()
    except Exception as e:
        print('Test mode with no connection...')
        with open('./testhtml/checkinlist.htm') as file:
            text = file.read()
    iobconnect.parseDuties(text)
    iobconnect.buildDutiesAndFlights()
