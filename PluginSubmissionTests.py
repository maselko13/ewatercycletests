import yaml
import Exceptions
import os

# tests whether the submission file contains the repository link
# input - data extracted from the submission.yml file
def includesRepositoryLinkTest(data):
      try:
          data.get("repository")
      except:
          raise Exceptions.NotFoundException("No repository name was provided")
          return -1
      if "/" not in data.get("repository"):
         raise Exceptions.WrongFormatException("A bad repository name was provided")
         return -1


# tests whether the submission file contains the variable list
# input - data extracted from the submission.yml file
def containsVariablesTest(data):
      try:
            data.get("variables")
      except:
            raise Exceptions.NotFoundException("No variable names were provided")
            return -1

def containsForcingParametersTest(data):
    try:
        data.get("forcing_parameters")
    except:
        raise Exceptions.NotFoundException("No forcing parameters were provided")
        return -1
# tests whether the submission file defines the vital discharge variables within its variable list
# input - data extracted from the submission.yml file
def definesCriticalVarsTest(data,variables):
        try:
            temp = data.get("variables")
            for var in variables:
              condition = False
              for temp2 in temp:
                try:
                      temp2.get(var)
                      condition = True
                      break
                except:
                      condition = False
              if not condition:
                  raise Exceptions.NotFoundException("The " + var + " variable was not provided")
                  return -1
        except:
            raise Exceptions.NotFoundException("The submission does not include any variables")

# extract data
dir_path = os.path.dirname(os.path.realpath(__file__))
data = yaml.safe_load(open(os.path.join(dir_path, 'exampleLeakyBucketSubmissionFile.yml')))
variables = ['discharge']
# test data
includesRepositoryLinkTest(data)
containsVariablesTest(data)
containsForcingParametersTest(data)
definesCriticalVarsTest(data,variables)
