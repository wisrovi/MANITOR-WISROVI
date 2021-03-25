class Version:
    centena = int()
    decena = int()
    unidad = int()


class AutoUpdate_project:
    import requests
    import os
    from git import Repo
    import json
    import os.path as path
    import shutil

    RAMA_TRABAJO = "main"
    NOT_ERASE_FILES = ['.git', '.gitattributes', '.gitignore', '.idea', 'info_version.txt', 'autoupdate.py', 'env',
                       '__init__.py']

    def __init__(self, project, root_path=None):
        self.local_version = Version()
        self.web_version = Version()
        self.project = project
        if root_path is not None:
            self.root_path = root_path
        else:
            self.root_path = None

    def read_version_web(self):
        url_version = "https://raw.githubusercontent.com/" + self.project + "/main/version.txt"
        r = self.requests.get(url=url_version, params={})
        data = r.content.decode("utf-8").replace("\n", "")
        data = [int(d) for d in data.split(".")]
        self.web_version.unidad = data[2]
        self.web_version.decena = data[1]
        self.web_version.centena = data[0]
        # print("Nueva version: ", data)

    def read_version_local(self):
        try:
            with open('version.txt', 'r') as reader:
                data = reader.read().replace("\n", "")
                data = [int(d) for d in data.split(".")]
                self.local_version = Version()
                self.local_version.unidad = data[2]
                self.local_version.decena = data[1]
                self.local_version.centena = data[0]
                # print("Version actual: ", data)
        except:
            pass

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
            self.get_data_last_update()
            self.download_update()
        else:
            print("OS update, not need update!")
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
        print("Downloading update...")
        if self.root_path is not None:
            BASE_DIR = self.root_path
        else:
            BASE_DIR = self.path.dirname(self.path.realpath(__file__))
        url_folder = "https://github.com/" + self.project + ".git"

        Folder = "temp"
        if not self.os.path.isdir(BASE_DIR + "/" + Folder):
            self.os.mkdir(BASE_DIR + "/" + Folder)
            self.Repo.clone_from(url_folder, BASE_DIR + "/" + Folder)

        contenidos = self.os.listdir(BASE_DIR)
        contenidos = [cont if not cont in self.NOT_ERASE_FILES else 'null' for cont in contenidos]
        contenidos = list(set(contenidos))
        contenidos.remove('null')

        for elemento in contenidos:
            if elemento != Folder:
                if self.os.path.isdir(BASE_DIR + "/" + elemento):
                    self.shutil.rmtree(elemento)
                else:
                    self.os.remove(elemento)

        contenidos = self.os.listdir(Folder)
        contenidos = [cont if not cont in self.NOT_ERASE_FILES else 'null' for cont in contenidos]
        contenidos = list(set(contenidos))
        contenidos.remove('null')

        for elemento in contenidos:
            origen = BASE_DIR + "/" + Folder + "/" + elemento
            destino = BASE_DIR + "/" + elemento
            # print(elemento, self.os.path.isfile(origen), self.os.path.isdir(origen))
            if self.os.path.isdir(origen):
                self.copytree(origen, destino)
            else:
                self.shutil.copy(origen, destino)

        self.shutil.rmtree(Folder)
        print("update completed!")

    def copytree(self, src, dst, symlinks=False, ignore=None):
        if not self.os.path.exists(dst):
            self.os.makedirs(dst)
        for item in self.os.listdir(src):
            s = self.os.path.join(src, item)
            d = self.os.path.join(dst, item)
            if self.os.path.isdir(s):
                self.shutil.copytree(s, d, symlinks, ignore)
            else:
                if not self.os.path.exists(d) or self.os.stat(s).st_mtime - self.os.stat(d).st_mtime > 1:
                    self.shutil.copy2(s, d)


class Autoupdate(object):
    def __init__(self, name, project, root_path):
        self.name = name
        self.project = project
        self.root_path = root_path

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            AutoUpdate_project(self.project, self.root_path).check_new_version()
            rta = f(*args, **kw_args)
            return rta

        return none


PROJECT = "wisrovi/MANITOR-WISROVI"

# @Autoupdate(name="Autoupdate WISROVI", project=PROJECT)
# def main_demo_autoupdate():
#     print("update library")


if __name__ == "__main__":
    # main_demo_autoupdate()
    pass
