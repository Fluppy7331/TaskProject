class TaskAlreadyHighestPrioException(Exception):
    """
    Exception raised when a task is already at the highest priority level.
    """
    def __init__(self, message):
        super().__init__(f"{message} ({self.__class__.__name__})")
        self.message = f"{message} ({self.__class__.__name__})"