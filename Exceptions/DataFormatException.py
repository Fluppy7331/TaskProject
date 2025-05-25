class DataFormatException(Exception):
    """
    Exception raised for errors in the data format.
    """

    def __init__(self, message):
        super().__init__(f"{message} ({self.__class__.__name__})")
        self.message = f"{message} ({self.__class__.__name__})"
