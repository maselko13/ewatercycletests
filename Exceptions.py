class VarDoesntExistException(Exception):
    print("the variable you're trying to get doesn't exist!")
class NotFoundException(Exception):
        def __init__(self, message):
            super().__init__(message)
class WrongFormatException(Exception):
        def __init__(self, message):
            super().__init__(message)
