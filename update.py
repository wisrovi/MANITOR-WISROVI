PROJECT = "wisrovi/MANITOR-WISROVI"

class Version:
    centena = int()
    decena = int()
    unidad = int()
class AutoUpdate:
    import requests
    def __init__(self, project):
        self.project = project

    def read_version_web(self):
        url_version = "https://raw.githubusercontent.com/" + self.project + "/main/version.txt"
        r = self.requests.get(url = url_version, params = {})
        data = r.content.decode("utf-8")
        data = data.split(".")
        self.web_version = Version()
        self.web_version.unidad = data[2]
        self.web_version.decena = data[1]
        self.web_version.centena = data[0]

    def read_version_local(self):
        with open('version.txt', 'r') as reader:
            data = reader.read()
            data = data.split(".")
            self.local_version = Version()
            self.local_version.unidad = data[2]
            self.local_version.decena = data[1]
            self.local_version.centena = data[0]

    def check_new_version(self):
        self.read_version_local()
        self.read_version_web()

        there_is_new_version = False
        if self.web_version.centena > self.local_version.centena:
            there_is_new_version = True
        elif self.web_version.decena > self.local_version.decena:
            there_is_new_version = True
        elif self.web_version.unidad > self.local_version.unidad:
            there_is_new_version = True
        return there_is_new_version



auto_update = AutoUpdate(PROJECT)
print(auto_update.check_new_version())

url_folder = "https://github.com/" + PROJECT

COMMITS_TO_PRINT = 5

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(),
                                              commit.size)))

def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

    rama = 

import os
from git import Repo
repo_path = os.getenv(url_folder)
repo = Repo(repo_path)
if not repo.bare:
    print_repository(repo)

    # create list of commits then print some of them to stdout
    commits = list(repo.iter_commits('master'))[:COMMITS_TO_PRINT]
    for commit in commits:
        print_commit(commit)
        pass
else:
    print('Could not load repository at {} :('.format(repo_path))

