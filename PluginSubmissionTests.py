import yaml

# tests whether the submission file contains the repository link
# input - data extracted from the submission.yml file
def includesRepositoryLinkTest(data):
      try:
            if "/" not in data.get("repository"):
                  raise Exception("No repository name was provided")
                  return -1
      except:
            raise Exception("No repository name was provided")
            return -1

# tests whether the submission file contains the variable list
# input - data extracted from the submission.yml file
def containsVariablesTest(data):
      try:
            data.get("variables")
      except:
            raise Exception("No variable names were provided")
            return -1

# tests whether the submission file defines the vital discharge variables within its variable list
# input - data extracted from the submission.yml file
def definesDischargeTest(data):
            temp = data.get("variables")
            condition = True
            for temp2 in temp:
                try:
                      temp2.get('discharge')
                except:
                      raise Exception("The discharge variable was not provided")
                      return -1

# extract data
data = yaml.safe_load(open('submission.yml'))
# test data
includesRepositoryLinkTest(data)
containsVariablesTest(data)
definesDischargeTest(data)
# print repository link so that workflow can clone it
print(data.get("repository"))
