"""
This file contains python2 workarounds for datetime
"""

from datetime import datetime, timedelta, tzinfo

from WYOB_error import WYOBError


def parseDateTime(datetime_string):
    """
    This function parses the string as stored in JSON files and returns a fully
    aware datetime. Format: YYYY-MM-DD HH:MM +HHMM.
    :param datetime_string:
    :return: aware datetime object
    """
    try:
        naive_datetime = datetime.strptime(datetime_string[0:16], "%Y-%m-%d %H:%M")
    except Exception as e:
        raise WYOBError('Failed to parse the string ' + datetime_string + ' to build a datetime!')

    try:
        offset = timedelta(hours=int(datetime_string[19:21]), minutes=int(datetime_string[21:]))
    except Exception as e:
        raise WYOBError('Failed to parse the string ' + datetime_string + ' to build the offset!')

    if datetime_string[18] == '+':
        time_zone_info = TZinfo(offset=offset)
    elif datetime_string[18] == '-':
        time_zone_info = TZinfo(offset=-offset)
    else:
        time_zone_info = TZinfo(offset=0)

    aware_datetime = naive_datetime.replace(tzinfo=time_zone_info)

    return aware_datetime


class TZinfo(tzinfo):

    def __init__(self, offset, name='anonymous'):
        if isinstance(offset, timedelta):
            self._offset = offset
        elif isinstance(offset, int):
            self._offset = timedelta(minutes=offset)
        self._name = name

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return timedelta(0)


utcTZ = TZinfo(offset=0)
