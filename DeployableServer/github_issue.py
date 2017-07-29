import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'taylorjdawson'
PASSWORD = 'suggested9]scientists]smell]Two'

# The repository to add this issue to
REPO_OWNER = 'taylorjdawson'
REPO_NAME = 'theofficequotesdb'

def make_github_issue(title, body='', labels=None):

    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)

    # Create an authenticated session to create the issue
    session = requests.session()
    session.auth = (USERNAME, PASSWORD)

    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}

    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print('Successfully created Issue "{}"'.format(title))
    else:
        print('Could not create Issue "{}"'.format(title))
        print('Response:', json.dumps(r.json(), indent=True))

make_github_issue('Test Issue', 'This is a test issue', ["typo"])