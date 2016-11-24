# -*- coding: utf-8 -*-
import svn2git_adapter as svn2git
import subversion_tools as svn
import git_tools as git
import settings_reader
import os

# use this https://docs.python.org/3/howto/regex.html for regexp


def check_binaries():
    if not svn.check():
        print("[FAIL] Subversion client does not installed.\nOr not added to \"path\" environment variable.")
        return False
    else:
        print("[ OK ] Subversion")

    if not git.check():
        print("[FAIL] Git client does not installed.\nOr not added to \"path\" environment variable.")
        return False
    else:
        print("[ OK ] Git")

    # under Linux the git-svn is a separate package and requires separate install
    if "posix" == os.name:
        if not git.svn.check():
            print("[FAIL] Git Svn client does not installed.")
            print("       You have to run \"sudo apt-get install git-svn\" in terminal")
            print("       to get it.")
            return False
        else:
            print("[ OK ] Git-Svn")

    return True


def main():
    settings = settings_reader.Reader()

    if not check_binaries():
        print("[FAIL] Required binaries check failed.")
        return False

    adapter = svn2git.Adapter()

    if not settings.init(adapter):
        print("[FAIL] Failed to initialize.")
        return False

    print("[ OK ] This is a valid svn URL.")
    print("[INFO] Starting with contents...")

    if not adapter.process_directory():
        print("[FAIL] Failed to read SVN svn:externals properties.")
        return False

    if not adapter.clone_externals():
        print("[FAIL] Failed to git clone SVN externals.")
        return False

    if not adapter.clone_working_copy():
        print("[FAIL] Failed to git clone working copy.")
        return False

    if not adapter.create_submodules():
        print("[FAIL] Failed to create symbolic links.")
        return False

    return True


if __name__ == "__main__":
    if not main():
        print("[FAIL] Finally - failed.")
    else:
        print("[ OK ] Finally - succeeded.")
    exit()
