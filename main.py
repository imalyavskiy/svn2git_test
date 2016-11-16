# -*- coding: utf-8 -*-
import subversion_tools as svn
import git_tools as git
import settings_reader

# use this https://docs.python.org/3/howto/regex.html for regexp


def check_binaries():
    if not svn.check():
        print("Subversion client does not installed.\nOr not added to \"path\" environment variable.")
        return False
    else:
        print("[ OK ] Subversion")

    if not git.check():
        print("Git client does not installed.\nOr not added to \"path\" environment variable.")
        return False
    else:
        print("[ OK ] Git")

    return True


def main():
    settings = settings_reader.Reader()

    if not check_binaries():
        return False

    if not settings.read():
        return False

    if not settings.check():
        return False

    adapter = settings.adapter      # adapter is ready to perform the job

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
        print("[FAIL] FAILED")
        exit()
    print("[ OK ] SUCCEEDED")
    exit()
