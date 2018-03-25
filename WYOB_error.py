class WYOBError(Exception):
    """
    """
    def __init__(self, message=""):
        self.message = "WYOBError: " + message


if __name__ == "__main__":
    try:
        raise WYOBError("Error Test!")
    except Exception as e:
        print("PASSED WYOBError raised and caught with message: " + e.message)
