"""Module containing the tests of the models.txt file modifications in the submission pull request."""
import exceptions

def contains_name_test(data):
    """Test if the models.txt modification contains the name of the model.

    Args:
        data: the models.txt file.
    """
    try:
        data[0]
    except Exception as exception:
        raise exceptions.NotFoundException("no name"
                                    " was provided in the models.txt file!") \
            from exception
    if not (data[0].startswith("name:") and len(data[0]) >= 9):
        raise exceptions.NotFoundException("no name"
                                           " was provided in the models.txt file!")

def includes_repository_link_test(data):
    """Test if the models.txt modification contains the link to the model repository.

    Args:
        data: the models.txt file.
    """
    try:
        data[1]
    except Exception as exception:
        raise exceptions.NotFoundException("No repository name was provided")\
            from exception
    if not (data[1].startswith("repository:") and len(data[1]) >= 16):
        raise exceptions.NotFoundException("No repository name was provided")
    if not data[1].split()[1].startswith("https://github.com/"):
        raise exceptions.WrongFormatException("The repository"
                            " inclusion in the models.txt has the wrong format!")
    return data[1].split()[1]

# extract data
with open('models.txt', "r", encoding="utf8") as file:
    input = file.readlines()
# test data
contains_name_test(input)
# print repository link so that workflow can clone it
print(includes_repository_link_test(input))
