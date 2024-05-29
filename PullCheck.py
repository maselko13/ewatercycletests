import gitlab

# this will need to be changed to not reveal the token, as we can't leak MR/PR approving capabilities
g = gitlab.Gitlab(url='https://gitlab.ewi.tudelft.nl', private_token='3NgdmMtmzpt8MuBbWEyZ')

project = (g.projects.get(13942))
mrs = project.mergerequests.list(state='opened', order_by='created_at')
for pr in mrs:
    if(pr.title.startswith("Add model:")):
            branch = project.branches.get(pr.source_branch)
            not_tested = [line.rstrip('\n') for line in open("need_to_test.txt")]
            if branch.name in not_tested:
                print("testing needed to approve branch " + branch.name)
            else:
                # merge the branch
                print("branch " + branch.name +" tested, approving MR...")


