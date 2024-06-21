import workflows.Exceptions
import os
from workflows import Exceptions

def containsNameTest(data):
    try:
        data[0]
    except:
        raise Exceptions.NotFoundException("no name was provided in the models.txt file!")
    if data[0].startswith("name:") and len(data[0]) >= 9:
        return
    else:
        raise Exceptions.NotFoundException("no name was provided in the models.txt file!")

def includesRepositoryLinkTest(data):
      try:
           data[1]
      except:
            raise Exceptions.NotFoundException("No repository name was provided")
            return -1
      if not (data[1].startswith("repository:") and len(data[1]) >= 16):
            raise Exceptions.NotFoundException("No repository name was provided")
            return -1
      if "/" not in data[1]:
          raise Exceptions.WrongFormatException("The repository inclusion in the models.txt has the wrong format!")
          return -1
      return data[1].split()[1]

# extract data
dir_path = os.path.dirname(os.path.realpath(__file__))
file1 = open(os.path.join(dir_path, 'submissionMocks/models.txt'))
data = file1.readlines()
# test data
containsNameTest(data)
# print repository link so that workflow can clone it
print(includesRepositoryLinkTest(data))