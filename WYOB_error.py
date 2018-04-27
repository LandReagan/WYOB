from kivy.logger import Logger


class WYOBError(Exception):
    """
    """
    def __init__(self, message=""):
        self.message = "WYOBError: " + message
        Logger.error("WYOB: " + message)
