from github import Github
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

access_token = config['DEFAULT']['access_token']
org = config['DEFAULT']['org']
repo = config['DEFAULT']['repo']

# or using an access token
g = Github(access_token)
repo = g.get_repo(f'{org}/{repo}')

pulls = repo.get_pulls(state='closed', sort='created', base='master')
for pr in pulls[0:10]:
    print({
        "created_at": pr.created_at,
        "user": pr.user
        })

