import shutil
import cleaner
import os
import re


def run(github_access):
    fic = github_access.get_organization("FAIRiCUBE")
    files = 0
    for repo in fic.get_repos():
        if repo.name == 'data-requests':
            continue
        path = 'repos/' + repo.name + '/issues/'
        if not os.path.exists(path):
            os.makedirs(path)
        issues = repo.get_issues(state="all")
        # print('\n')
        # print('--------------------------------------')
        # print(repo.name)
        # print('--------------------------------------')
        for issue in issues:
            if not isinstance(issue.body, str):
                continue
            s = issue.title + '\n'
            s = s + issue.body + '\n'
            comments = issue.get_comments()
            for comment in comments:
                s = s + comment.body
                s = s + '\n'

            if s == '':
                continue
            special_chars = r'[^A-Za-z0-9]'
            title = issue.title
            title = re.sub(special_chars, '', title)
            title = title.strip().replace(' ', '')

            s = cleaner.preprocess_text(s)

            f = open(path+title+'.md', 'w', encoding="utf-8")
            f.write(s)
            f.close()
            files += 1
        # print('\n')

        if len(os.listdir(path)) == 0:
            shutil.rmtree(path)

    # To close connections after use
    # github_access.close()
    return files
