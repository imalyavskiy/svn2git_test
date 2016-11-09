# -*- coding: utf-8 -*-

import subversion_tools as svn
import git_tools as git
import re
import uuid


class PropItem:         # Stores regexps for the svn:externals certain item to be parsed
    def __init__(self):
        self.url_repository_root = str()
        self.old_rev = re.compile(
            "-r\s?\d+"
        )
        self.rev_num = re.compile(
            "\d+"
        )
        self.src_url = re.compile(
            "((http(s)?://)|(\^/))"  # "https://" or "^/"
            "(/?((\w|%|-|\.)+\.?)+)+"  # server.com/folder.f/folder
        )
        self.new_rev = re.compile(
            "@\d+"  # @122
        )
        self.dst_path = re.compile(
            "(/?((\w|-)+\.?)+)+"  # folder/folder
        )
        self.leading_space = re.compile(
            "^\s"
        )

    def split(self, string):
        rev_val = "HEAD"
        m = self.old_rev.search(string)
        if m is not None:
            old_rev = string[m.span()[0]:m.span()[1]]
            string = string[m.span()[1]:]
            string = self.leading_space.sub("", string)
            m = self.rev_num.search(old_rev)
            if m is not None:
                rev_val = old_rev[m.span()[0]: m.span()[1]]

        m = self.src_url.search(string)
        if m is None:
            return None

        src_url = string[m.span()[0]:m.span()[1]]
        string = string[m.span()[1]:]
        string = self.leading_space.sub("", string)

        m = self.new_rev.search(string)
        if m is not None:
            new_rev = string[m.span()[0]:m.span()[1]]
            string = string[m.span()[1]:]
            string = self.leading_space.sub("", string)
            m = self.rev_num.search(new_rev)
            if m is not None:
                if rev_val == "HEAD":
                    rev_val = new_rev[m.span()[0]: m.span()[1]]
                elif rev_val != m.group():
                    print("[WARN] old style and new style revisions are !EQ - taking the new style one.")
                    rev_val = new_rev[m.span()[0]: m.span()[1]]

        m = self.dst_path.search(string)
        if m is None:
            return None

        dst_path = string[m.span()[0]:m.span()[1]]

        if src_url.startswith("^"):
            src_url = src_url.replace("^", self.url_repository_root)

        git_local_repo_name = "{" + str(uuid.uuid4()).upper() + "}"
        return src_url, rev_val, dst_path, git_local_repo_name


class Adapter:                          # Parses entire output of the "svn propget -v -R <url|path>"
                                        # and stores result for further usage
    def __init__(self):
        self.re_fs_path = \
            re.compile(
                "([A-Za-z]:)?(((\\\\)|(/))[\w.]*)*((\\\\)|(/))?"  # "[d:]<\|/><dir name><\|/><dir name>[\|/]"
            )
        self.re_svn_ext_prop = \
            re.compile(
                "(^\s*)?"
                "(-r\s\d+\s)?"  # -r 122
                "((http(s)?://)|(\^/))"  # "https://" or "^/"
                "(/?((\w|%|-)+\.?)+)+"  # server.com/folder.f/folder
                "(@\d+)?"  # @122
                "\s"  # space
                "(/?((\w|-)+\.?)+)+"  # folder/folder
            )
        self.re_svn_folder_hdr = \
            re.compile(
                "Properties on \'"
                "((http(s)?://)|(\^/))"  # "https://" or "^/"
                "(/?((\w|%|-)+\.?)+)+"  # server.com/folder.f/folder
                "\':"
            )
        self.re_svn_property_name = \
            re.compile(
                "^\s*svn:\w*"
            )
        self.re_url = \
            re.compile(
                "((http(s)?://)|(\^/))"  # "https://" or "^/"
                "(/?((\w|%|-)+\.?)+)+"  # server.com/folder.f/folder
            )
        self.results = dict()
        self.prop_item = PropItem()
        self.url_repository_root = str()
        self.path_working_cpy_root = str()
        self.url_repository_rel = str()

    def is_url(self, path):
        m = self.re_url.match(path)
        if m.group() == path:
            return True
        return False

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

    def extract_folder_name(self, string):
        string = string.replace("Properties on \'", "")
        string = string.replace("\':", "")
        return string

    def is_prop_name(self, string):
        return self.check_match(self.re_svn_property_name, string)

    def is_prop_val(self, string):
        return self.check_match(self.re_svn_ext_prop, string)

    def attach(self, path):
        self.url_repository_root, self.url_repository_rel, self.path_working_cpy_root = svn.repository_info(path)
        if len(self.url_repository_root) and len(self.url_repository_rel) and len(self.path_working_cpy_root):
            self.prop_item.url_repository_root = self.url_repository_root
            return True
        return False

    def process_directory(self):
        svn_client = svn.Client()
        externals = svn_client.propget_recursive(self.url_repository_root + self.url_repository_rel[1:]
                                                 , "svn:externals")
        strings = externals.split(sep="\n")
        folders = dict()
        f_name = str()
        for i in range(0, len(strings)):
            string = strings[i]
            if self.is_folder_hdr(string):
                f_name = self.extract_folder_name(string)
                folders[f_name] = []
            elif self.is_prop_val(string):
                folders[f_name].append(self.prop_item.split(string))

        self.results[self.url_repository_root + self.url_repository_rel[1:]] = folders
        return True

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
                        result += "\t\t" + value[0] + "@" + value[1] + "\n"
                        result += "\t\t" + value[3] + " for " + value[2] + "\n"
        return result

    def clone_externals(self):      # Creates local git repositories to be plugged to main git repository as modules
        parents = self.results.keys()
        for parent in parents:
            pass
            folders = self.results[parent].keys()
            for folder in folders:
                pass
                for value in self.results[parent][folder]:
                    if value is None:
                        pass
                    else:
                        pass

        return False

    def clone_working_copy(self):   # Executes git svn clone for the main repo
        return False

    def create_symlinks(self):      # Creates a set of symbolic links in the same way as svn:externals should create
        return False                # its folders

