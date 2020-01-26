from github import Github
import configparser
from collections import Counter, defaultdict


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

access_token = config['DEFAULT']['access_token']
org = config['DEFAULT']['org']
repo = config['DEFAULT']['repo']

g = Github(access_token)
repo = g.get_repo(f'{org}/{repo}')

c = Counter()
pulls = repo.get_pulls(state='closed', sort='created', base='master')
for pr in pulls[0:100]:
    print({
        "created_at": pr.created_at.strftime("%Y-%m"),
        "user": pr.user.login,
        })
    c.update({f'created_at/{pr.created_at.strftime("%Y-%m")}/user/{pr.user.login}': 1})

print(c)

