class VarDoesntExistException(Exception):
    def __init__(self, message):
        super().__init__(message)
class NotFoundException(Exception):
        def __init__(self, message):
            super().__init__(message)
class WrongFormatException(Exception):
        def __init__(self, message):
            super().__init__(message)
