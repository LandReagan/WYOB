# TODO: Adapt for python 2.7

from html.parser import HTMLParser


class TokenParser(HTMLParser):
    """ This class is intended to make URL with session and token available
        It has been tested and works !
    """
    token = ""
    new_URL = ""

    def handle_starttag(self, tag, attrs):
        # print(tag + ' ' + str(attrs))
        if tag == 'form':
            for a, b in attrs:
                if a == 'action':
                    self.new_URL = 'https://fltops.omanair.com' + b  # BAD !
                    # print('New URL is: ' + self.new_URL)
        if tag == 'input':
            for a, b in attrs:
                if a == 'name' and b != 'token':
                    break
                if a == 'value':
                    self.token = b
                    # print('New token is: ' + self.token)


class DutyParser(HTMLParser):
    """ This class is intended to parse the table output of checkinlist.jsp
        It will find the <body>, then get the table headers as tuple,
        and finally populate a list with duties as tuples (same size as
        headers)
    """
    headers = []
    duties = []

    _in_table = False
    _data = ''
    _duty = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and ('class', 'list') in attrs:
            self._in_table = True

    def handle_data(self, data):
        self._data = data

    def handle_endtag(self, tag):
        if self._in_table:
            if tag == 'th':
                self.headers.append(self._data)
            if tag == 'td':
                self._duty.append(self._data)
            if tag == 'tr' and len(self._duty) == len(self.headers):
                self.duties.append(list(self._duty))
                self._duty.clear()
