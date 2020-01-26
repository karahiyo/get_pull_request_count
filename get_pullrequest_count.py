from github import Github
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

access_token = config['DEFAULT']['access_token']

# or using an access token
g = Github(access_token)

for repo in g.get_user().get_repos(type='owner'):
    print(repo.name)
