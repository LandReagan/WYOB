import logger


class WYOBError(Exception):
    """
    """
    def __init__(self, message=""):
        self.message = "WYOBError: " + message
        logger.logE(self.message)
