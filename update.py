PROJECT = "wisrovi/MANITOR-WISROVI"

class Version:
    centena = int()
    decena = int()
    unidad = int()
class AutoUpdate:
    import requests
    import os
    from git import Repo
    import json
    import os.path as path
    import shutil

    RAMA_TRABAJO = "main"

    def __init__(self, project):
        self.project = project

    def read_version_web(self):
        url_version = "https://raw.githubusercontent.com/" + self.project + "/main/version.txt"
        r = self.requests.get(url = url_version, params = {})
        data = r.content.decode("utf-8").replace("\n", "")
        data = [int(d) for d in data.split(".") ]
        self.web_version = Version()
        self.web_version.unidad = data[2]
        self.web_version.decena = data[1]
        self.web_version.centena = data[0]
        print("Nueva version: ", data)

    def read_version_local(self):
        with open('version.txt', 'r') as reader:
            data = reader.read().replace("\n", "")
            data = [int(d) for d in data.split(".") ]
            self.local_version = Version()
            self.local_version.unidad = data[2]
            self.local_version.decena = data[1]
            self.local_version.centena = data[0]
            print("Version actual: ", data)

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

        if there_is_new_version:
            print("Hay una nueva versión para descargar...")
            self.get_data_last_update()
            self.download_update()
        return there_is_new_version

    def get_data_last_update(self):
        url_folder = "https://github.com/" + self.project
        repo_path = self.os.getenv(url_folder)
        repo = self.Repo(repo_path)
        if not repo.bare:
            commit = list(repo.iter_commits(self.RAMA_TRABAJO))[0]

            data_repo = dict()
            data_repo['project'] = self.project
            data_repo['desc'] = repo.description

            data_repo['date'] = commit.authored_datetime.strftime("%m/%d/%Y, %H:%M:%S")
            data_repo['person'] = commit.author.name
            data_repo['email'] = commit.author.email
            data_repo['count'] = commit.count()
            data_repo['size'] = commit.size

            with open('info_version.txt', 'w') as outfile:
                self.json.dump(data_repo, outfile)
        else:
            print('Could not load repository at {} :('.format(self.project))

    def download_update(self):
        BASE_DIR = self.path.dirname(self.path.realpath(__file__))
        url_folder = "https://github.com/" + self.project + ".git"

        Folder = "temp"
        if not self.os.path.isdir(Folder):
            self.os.mkdir(Folder)
            self.Repo.clone_from(url_folder, BASE_DIR + "/" + Folder)

        contenidos = self.os.listdir(BASE_DIR)
        for elemento in contenidos:
            if self.os.path.isfile(elemento):
                if not elemento.__eq__("update.py"):
                    if not elemento.__eq__(".git"):
                        if not elemento.__eq__("version.txt"):
                            self.os.remove(elemento)

        contenidos = self.os.listdir(Folder)
        for elemento in contenidos:
            if not elemento.__eq__(".git"):
                self.shutil.copy(elemento, BASE_DIR)

        self.shutil.rmtree(Folder)
        print("update completed!")


if __name__=="__main__":
    AutoUpdate(PROJECT).check_new_version()
    print("queso")








