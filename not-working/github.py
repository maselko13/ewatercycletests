import os
from github import Github
# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("will not include here")

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo("maselko13/pulltesting")
f = open("pulltesting/number.txt", "r")
number = f.read()
f.close()
pulls = repo.get_pulls(state='open', sort='created')
pulls = pulls.reversed
first = False
if(pulls[0].number != number) :
 number2 = number
 for pr in pulls:
    if(pr.title.startswith("aD")):
        if(first == False):
            first = True
            number2 = pr.number
        if(int(pr.number) > int(number)):
            print(pr.number)
            print(pr.title)
        else:
            f = open("pulltesting/number.txt", "w")
            f.write(str(number2))
            f.close()
            g.close()
else:
  g.close()