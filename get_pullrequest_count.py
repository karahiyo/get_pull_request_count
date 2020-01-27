from github import Github
import configparser
from collections import Counter, defaultdict
import csv
import re


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

access_token = config['DEFAULT']['access_token']
org = config['DEFAULT']['org']
repo = config['DEFAULT']['repo']

g = Github(access_token)
repo = g.get_repo(f'{org}/{repo}')

c = Counter()
pulls = repo.get_pulls(state='closed', sort='created', base='master')
for pr in pulls:
    print({
        "created_at": pr.created_at.strftime("%Y-%m"),
        "user": pr.user.login,
        })
    c.update({f'created_at/{pr.created_at.strftime("%Y-%m")}/user/{pr.user.login}': 1})

pr_count_per_contributer = {}
key_pattern = r'created_at/(?P<created_at>[0-9-]*)/user/(?P<user>.*)'
for key, value in sorted(c.items()):
    m = re.match(key_pattern, key)
    created_at = m.group('created_at')
    user = m.group('user')
    pr_count = value
    if created_at in pr_count_per_contributer:
        if user in pr_count_per_contributer[created_at]:
            pr_count_per_contributer[created_at][user] += value
        else:
            pr_count_per_contributer[created_at][user] = value
    else:
        pr_count_per_contributer[created_at] = {user: value}

print(pr_count_per_contributer)

with open("./out/" + config['DEFAULT']['out_csv'], mode='w') as f:
    writer = csv.writer(f)
    writer.writerow(["date", "pr_count_avg"])
    for created_at, pr_count_by_user in pr_count_per_contributer.items():
        writer.writerow([created_at, sum(pr_count_by_user.values()) / len(pr_count_by_user.values())])


print("fin")
