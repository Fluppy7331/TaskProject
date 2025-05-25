class NotUniqueNameException(Exception):
    """
    Exception raised when a task is already marked as done.
    """
    def __init__(self, message):
        super().__init__(f"{message} ({self.__class__.__name__})")
        self.message = f"{message} ({self.__class__.__name__})"