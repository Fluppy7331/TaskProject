class UnknownAttributeException(Exception):
    """
    Exception raised when an unknown filtering attribute is encountered.
    """
    def __init__(self, message):
        super().__init__(f"{message} ({self.__class__.__name__})")
        self.message = f"{message} ({self.__class__.__name__})"