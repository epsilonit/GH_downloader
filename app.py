from github import Github
import files_manager
import issue_manager
from github import Auth
import build_folder
import os

# using an access token
token = os.environ['GH_TOKEN']
auth = Auth.Token(token)

path = 'repos/'
if not os.path.exists(path):
    os.makedirs(path)

i = False
f = False
m = True

# ISSUES
if i:
    g = Github(auth=auth)
    print('\n\n\n\n********************************************')
    print('DOWNLOADING ISSUES')
    print('********************************************')
    issues = issue_manager.run(g)
    print('Issues downloaded: ', issues)
    g.close()

if f:
    # FILES
    g = Github(auth=auth)
    print('\n\n\n\n********************************************')
    print('DOWNLOADING FILES')
    print('********************************************')
    files = files_manager.run(g)
    print('Files downloaded: ', files)
    g.close()

if m:
    print('\n\n\n\n********************************************')
    print('MOVING FILES')
    print('********************************************')
    build_folder.build()
