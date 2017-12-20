import json
import requests
import logging

# TODO: Fix the logging issue organize them http://python-guide-pt-br.readthedocs.io/en/latest/writing/logging/
logging.basicConfig(filename='githubissue.log', level=logging.DEBUG)

access_token = "d1e5ecf79a9782fb53f7af067feeb8803792fe5f"

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'taylorjdawson'
PASSWORD = 'Whether354<Information<above<<'

# The repository to add this issue to
REPO_OWNER = 'taylorjdawson'
REPO_NAME = 'theofficequotesdb'


def make_github_issue(issue_content):

    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    "https://api.github.com/repos/octocat/Hello-World/issues/1347"
    # Create an authenticated session to create the issue
    session = requests.session()
    session.headers.update({'Authorization': "token " + access_token})

    title = 'User Submitted: Quote'


    body = """
Line id: {}
Line: {}
User message: {}
""".format(issue_content['line_id'], issue_content['line'], issue_content['message'])

    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': [issue_content['type']]}

    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        status = {"message": "success"}
        print('Successfully created Issue "{}"'.format(title))
    else:
        print(url); print(access_token)
        print(r.status_code)
        print('Could not create Issue "{}"'.format(title))
        # logging.error('Could not create Issue "{}"'.format(title))
        print('Response:', json.dumps(r.json(), indent=True))
        # logging.error('Response:', json.dumps(r.json(), indent=True))
        status = {"message": r.json()}

    return status

# make_github_issue({
#     "type": "typo",
#     "message": "a Test",
#     "line_id": "these is none",
#     "line": "There is none"
#                    })