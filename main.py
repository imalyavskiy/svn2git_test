# -*- coding: utf-8 -*-
import sys
import subversion_tools as svn
import git_tools as git
import re
# use regexp https://docs.python.org/3/howto/regex.html


def is_path(path):
    print("is_path >>> Check: \"{0}\"".format(path))
    p = re.compile("([A-Za-z]:)?(((\\\\)|(/))[\w.]*)*((\\\\)|(/))?") # "[d:]<\|/><dir name><\|/><dir name>[\|/]"
    m = p.match(path)
    if m.group() == path:
        return True
    return False


def is_external_prop(string):
    p = re.compile(
                   "(-r\s\d+\s)?"           # -r 122
                   "((http(s)?://)|(\^/))"  # "https://" or "^/"
                   "(/?((\w|%|-)+\.?)+)+"   # server.com/folder.f/folder
                   "(@\d+)?"                # @122
                   "\s"                     # space
                   "(/?((\w|-)+\.?)+)+"     # folder/folder
                   )
    m = p.match(string)
    if m is None:
        return False
    if m.group() == string:
        return True
    return False


def process_directory(path):
    path += "/"

    if not svn.is_controlled(path):
        return

    externals = svn.propget_recursive(path=path, prop="svn:externals")
    externals = externals.replace(" - ", "\r\n")
    strings = externals.split(sep="\r\n")

    strings_new = []
    for string in strings:
        if 0 == len(string):
            continue
        strings_new.append(string)

    strings = strings_new
    del strings_new

    print(strings)

    for string in strings:
        if is_path(string):
            print("[ OK ] The string:\n"
                  "       \"{0}\"\n"
                  "       is folder".format(string))
        elif is_external_prop(string):
            print("[ OK ] The string:\n"
                  "       \"{0}\"\n"
                  "       is a correct svn:externals prop".format(string))
        else:
            print("[FAIL] The string:\n"
                  "       \"{0}\"\n"
                  "       cannot be recognized.".format(string))
    return


def main():
    if not svn.check_access():
        print("Subversion client does not installed.\nOr not added to \"path\" environment variable.")
        exit()
    else:
        print("[ OK ] Subversion")

    if not git.check_access():
        print("Git client does not installed.\nOr not added to \"path\" environment variable.")
        exit()
    else:
        print("[ OK ] Git")

    if len(sys.argv) < 2:
        print("[FAIL] Not enough parameters.")
        exit()

    if is_path(sys.argv[1]):
        print("[ OK ] Argument")
    else:
        print("[FAIL] Argument: not in a windows path format")

    print(">>> Directory to process: {0}".format(sys.argv[1]))

    if not svn.is_controlled(sys.argv[1]):
        print("[FAIL] This folder is not an SVN working copy.")
        exit()

    print("[ OK ] This is a valid working copy.")
    print(">>> Starting with contents...")

    process_directory(sys.argv[1])

    print(">>> Done.")
    return

main()

exit()
