"""
A module with extra exceptions that can be raised
"""
class VarDoesntExistException(Exception):
    def __init__(self):
        return
class NotFoundException(Exception):
        def __init__(self, message):
            super().__init__(message)
class WrongFormatException(Exception):
        def __init__(self, message):
            super().__init__(message)