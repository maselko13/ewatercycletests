
def containsNameTest(data):
    if data[0].startswith("name:") and len(data[0]) >= 8:
        return
    else:
        raise Exception("no name was provided in the models.txt notification!")

def includesRepositoryLinkTest(data):
      try:
            if "/" not in data[1]:
                  raise Exception("No repository name was provided")
                  return -1
      except:
            raise Exception("No repository name was provided")
            return -1
      if data[1].startswith("repository:") and len(data[1]) >= 10:
          return data[1].split()[1]
      else:
          raise Exception("The repository inclusion in the models.txt has the wrong format!")
          return -1

# extract data
file1 = open('models.txt', 'r')
data = file1.readlines()
# test data
containsNameTest(data)
# print repository link so that workflow can clone it
print(includesRepositoryLinkTest(data))