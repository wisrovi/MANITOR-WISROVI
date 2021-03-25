from Version1.library.autoupdate import Autoupdate
import os.path as path


@Autoupdate(name="Autoupdate WISROVI", project="wisrovi/MANITOR-WISROVI", root_path=path.dirname(path.realpath(__file__)))
def main_demo_autoupdate():
    print("update library")


if __name__ == "__main__":
    main_demo_autoupdate()
