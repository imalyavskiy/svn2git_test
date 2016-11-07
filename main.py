# -*- coding: utf-8 -*-
import sys
import subversion_tools as svn
import git_tools as git
import svn2git_adapter as svn2git
# use regexp https://docs.python.org/3/howto/regex.html


def main():
    adapter = svn2git.Adapter()

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

    if len(sys.argv) < 3:
        print("[FAIL] Not enough parameters.")
        return False

    if adapter.is_url(sys.argv[1]):
        print("[ OK ] Argument - Source URL.")
    else:
        print("[FAIL] Argument 1: not an URL")

    if adapter.is_path(sys.argv[2]):
        print("[ OK ] Argument - destination path.")
    else:
        print("[FAIL] Argument 2: is not a path")

    print(">>> URL to process: {0}".format(sys.argv[1]))

    if not adapter.attach(sys.argv[1]):
        print("[FAIL] Cannot attach the resource.")
        return False

    print("[ OK ] This is a valid svn URL.")
    print(">>> Starting with contents...")

    if not adapter.process_directory():
        print("[FAIL] Failed to read SVN svn:externals properties.")
        return False

    if not adapter.clone_externals():
        print("[FAIL] Failed to git clone SVN externals.")
        return False

    if not adapter.clone_working_copy():
        print("[FAIL] Failed to git clone working copy.")
        return False

    if not adapter.create_symlinks():
        print("[FAIL] Failed to create symbolic links.")
        return False

    return True


if __name__ == "__main__":
    if not main():
        print(">>> FAILED <<<")
        exit()
    print(">>> SUCCEEDED <<<")
    exit()
