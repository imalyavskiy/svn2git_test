# -*- coding: utf-8 -*-
import sys
import subversion_tools as svn
import git_tools as git
import re
# use regexp https://docs.python.org/3/howto/regex.html


class Svn2GitAdapter:
    def __init__(self):
        self.re_fs_path = \
            re.compile(
                       "([A-Za-z]:)?(((\\\\)|(/))[\w.]*)*((\\\\)|(/))?" # "[d:]<\|/><dir name><\|/><dir name>[\|/]"
            )
        self.re_svn_ext_prop = \
            re.compile(
                       "(^\s*)?"
                       "(-r\s\d+\s)?"           # -r 122
                       "((http(s)?://)|(\^/))"  # "https://" or "^/"
                       "(/?((\w|%|-)+\.?)+)+"   # server.com/folder.f/folder
                       "(@\d+)?"                # @122
                       "\s"                     # space
                       "(/?((\w|-)+\.?)+)+"     # folder/folder
            )
        self.re_svn_folder_hdr = \
            re.compile(
                      "Properties on \'.*\':"
            )
        self.re_svn_property_name = \
            re.compile(
                      "^\s*svn:\w*"
            )
        self.results = dict()

    def is_path(self, path):
        m = self.re_fs_path.match(path)
        if m.group() == path:
            return True
        return False

    def check_match(self, reg_exp, string):
        m = reg_exp.match(string)
        if m is None:
            return False
        if m.group() == string:
            return True
        return False

    def is_folder_hdr(self, string):
        return self.check_match(self.re_svn_folder_hdr, string)

    def is_prop_name(self, string):
        return self.check_match(self.re_svn_property_name, string)

    def is_prop_val(self, string):
        return self.check_match(self.re_svn_ext_prop, string)

    def process_directory(self, path):
        path += "/"

        if not svn.controlled(path):
            return
        svn_client = svn.Client()
        externals = svn_client.propget_recursive(path, "svn:externals")
        strings = externals.split(sep="\n")
        folders = dict()
        f_name = str()
        for i in range(0, len(strings)):
            string = strings[i]
            if self.is_folder_hdr(string):
                f_name = string
                folders[f_name] = []
            elif self.is_prop_name(string):
                pass
            elif self.is_prop_val(string):
                folders[f_name].append(string)
            else:
                pass

        self.results[path] = folders
        return

    def print(self):
        parents = self.results.keys()
        for parent in parents:
            print("{0}".format(parent))
            folders = self.results[parent].keys()
            for folder in folders:
                print("\t{0}".format(folder))
                for value in self.results[parent][folder]:
                    print("\t\t{0}".format(value))


def main():
    adapter = Svn2GitAdapter()

    if not svn.check():
        print("Subversion client does not installed.\nOr not added to \"path\" environment variable.")
        exit()
    else:
        print("[ OK ] Subversion")

    if not git.check():
        print("Git client does not installed.\nOr not added to \"path\" environment variable.")
        exit()
    else:
        print("[ OK ] Git")

    if len(sys.argv) < 2:
        print("[FAIL] Not enough parameters.")
        exit()

    if adapter.is_path(sys.argv[1]):
        print("[ OK ] Argument")
    else:
        print("[FAIL] Argument: not in a windows path format")

    print(">>> Directory to process: {0}".format(sys.argv[1]))

    if not svn.controlled(sys.argv[1]):
        print("[FAIL] This folder is not an SVN working copy.")
        exit()

    print("[ OK ] This is a valid working copy.")
    print(">>> Starting with contents...")

    adapter.process_directory(sys.argv[1])

    adapter.print()

    print(">>> Done.")
    return


if __name__ == "__main__":
    main()
    exit()
