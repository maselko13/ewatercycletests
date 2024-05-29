import yaml

def includesRepositoryLinkTest(data):
      try:
            if "/" not in data.get("repository"):
                  raise Exception("No repository name was provided")
      except:
            raise Exception("No repository name was provided")

def containsVariablesTest(data):
      try:
            data.get("variables")
      except:
            raise Exception("No variable names were provided")

def definesDischargeTest(data):
            temp = data.get("variables")
            condition = True
            for temp2 in temp:
                try:
                      temp2.get('discharge')
                except:
                      raise Exception("The discharge variable was not provided")

data = yaml.safe_load(open('exampleSubmissionFile.yml'))
includesRepositoryLinkTest(data)
containsVariablesTest(data)
definesDischargeTest(data)