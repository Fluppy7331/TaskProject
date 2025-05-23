
class TaskFormatException(Exception):
    """
    Exception raised for errors in the task format.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


