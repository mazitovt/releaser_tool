from git import Repo
import json
from logger import load_json
from git import Git
from git import IndexFile


a = {"1","2","3"}
b = {"3","4","5"}
c = a-b
print(f"diff: {', '.join(c)}")

# APP_CONF = 'app_conf.json'
#
# repo = Repo(load_json(APP_CONF)["repository"]["git_folder_path"])
#
# print(repo.active_branch)
# print(repo.description)
#
# for remote in repo.remotes:
#     print(remote)
#
# promedweb_branch = repo.heads['PROMEDWEB-37275']
#
# for branch in repo.heads:
#     print(branch)
#
# print(len(repo.heads["master"].commit.diff(repo.heads['PROMEDWEB-37275'].commit)))
# print(len(repo.index.diff(repo.heads['PROMEDWEB-37275'].commit)))
#
# for item in repo.heads["master"].commit.diff(repo.heads['PROMEDWEB-37275'].commit):
#     print()
#     print(item.a_path)
#     print(item.b_path)




#
# index = repo.index
# for k,v in index.entries.items():
#     print(k,v)