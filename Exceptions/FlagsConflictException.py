
class FlagsConflictException(Exception):
    """
    Exception raised for redundant flags in task management operations.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


