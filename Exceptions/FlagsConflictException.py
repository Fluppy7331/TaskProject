class FlagsConflictException(Exception):
    """
    Exception raised for redundant flags in task management operations.
    """
    def __init__(self, message):
        super().__init__(f"{message} ({self.__class__.__name__})")
        self.message = f"{message} ({self.__class__.__name__})"
