"""
A module with extra exceptions that can be raised
"""
class VarDoesntExistException(Exception):
    """
    an exception that is raised when a variable is not found
    """
    print("the variable you're trying to get doesn't exist!")
