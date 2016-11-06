# -*- coding: utf-8 -*-
import sys
import subversion_tools as svn
import git_tools as git
import re
# use regexp https://docs.python.org/3/howto/regex.html

class PropItem:
    def __init__(self):
        self.old_rev = re.compile(
            "-r\s\d+"
        )
        self.rev_num = re.compile(
            "\d+"
        )
        self.src_url = re.compile(
            "((http(s)?://)|(\^/))"     # "https://" or "^/"
            "(/?((\w|%|-)+\.?)+)+"      # server.com/folder.f/folder
        )
        self.new_rev = re.compile(
            "@\d+"                   # @122
        )
        self.dst_path = re.compile(
            "(/?((\w|-)+\.?)+)+"  # folder/folder
        )
        self.leading_space = re.compile(
            "^\s"
        )
        pass

    def split(self, string):
        src_url     = str()
        old_rev_val = str()
        new_rev_val = str()
        dst_path    = str()
        m = self.old_rev.search(string)
        if m is not None:
            old_rev = string[m.span()[0]:m.span()[1]]
            string = string[m.span()[1]: -1]
            string = self.leading_space.sub("", string)

            m = self.rev_num.search(old_rev)
            if m is not None:
                old_rev_val = old_rev[m.span()[0]: m.span()[1]]

        m = self.src_url.search(string)
        if m is not None:
            src_url = string[m.span()[0]:m.span()[1]]
            string = string[m.span()[1]: -1]
            string = self.leading_space.sub("", string)

        m = self.new_rev.search(string)
        if m is not None:
            new_rev = string[m.span()[0]:m.span()[1]]
            m = self.rev_num.search(new_rev)
            if m is not None:
                new_rev_val = new_rev[m.span()[0]: m.span()[1]]

            string = string[m.span()[1]: -1]
            string = self.leading_space.sub("", string)

        m = self.dst_path.search(string)
        if m is not None:
            dst_path = string[m.span()[0]:m.span()[1]]

        if not len(src_url) or not len(dst_path) or (len(old_rev_val) and len(new_rev_val) and old_rev_val != new_rev_val):
            return None
        elif not (len(old_rev_val) or len(new_rev_val)):
            return src_url, "HEAD", dst_path
        elif not len(old_rev_val):
            return src_url, new_rev_val, dst_path
        return src_url, old_rev_val, dst_path


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
        self.prop_item = PropItem()

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
                folders[f_name].append(self.prop_item.split(string))
            else:
                pass

        self.results[path] = folders
        return

    def __str__(self):
        result = str()
        parents = self.results.keys()
        for parent in parents:
            result += parent + "\n"
            folders = self.results[parent].keys()
            for folder in folders:
                result += "\t" + folder + "\n"
                for value in self.results[parent][folder]:
                    if value is None:
                        result += "\t\t ERROR \n"
                    else:
                        result += "\t\t" + value[0] + " | " + value[1] + " | " + value[2] + "\n"
        return result


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

    print(adapter)

    print(">>> Done.")
    return


if __name__ == "__main__":
    main()
    exit()
