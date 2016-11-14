# -*- coding: utf-8 -*-

import subversion_tools as svn
import git_tools as git
import uuid
import re_helpers
import os


class PropItem:         # Stores regexps for the svn:externals certain item to be parsed
    def __init__(self):
        self.url_repository_root = str()
        self.old_rev = re_helpers.revision_old
        self.rev_num = re_helpers.number_decimal
        self.src_url = re_helpers.url_subversion
        self.new_rev = re_helpers.revision_new
        self.dst_path = re_helpers.path_relative
        self.leading_space = re_helpers.leading_space

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

        return { "URL"            : src_url             # URL to take data from
               , "REVISION"       : rev_val             # SVN REVISION of data by URL
               , "DST_PATH"       : dst_path            # Where data should be placed in relation to property container
                                                        #   will be turned to full path mode on upper levels
               , "LOCAL_REPO_NAME": git_local_repo_name # UUID name of the git local repository
               }


class Adapter:                          # Parses entire output of the "svn propget -v -R <url|path>"
                                        # and stores result for further usage
    def __init__(self):

        self.re_fs_path = re_helpers.path_absolute
        self.re_svn_ext_prop = re_helpers.subversion_external_property_item
        self.re_svn_folder_hdr = re_helpers.subversion_folder_property_report_header
        self.re_svn_property_name = re_helpers.subversion_property_name
        self.re_url = re_helpers.url_subversion

        self.results = dict()
        self.prop_item = PropItem()
        self.url_repository_root = str()
        self.path_working_cpy_root = str()
        self.working_cpy_placement = str()
        self.working_cpy_externals = str()
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
        externals_path = self.path_working_cpy_root + "/" + self.working_cpy_externals
        if not os.path.exists(externals_path):
            if not os.path.exists(self.path_working_cpy_root):
                try:
                    os.mkdir(self.path_working_cpy_root)
                except FileNotFoundError as err:
                    print("[FAIL] Cannot create the \"{0}\" directory.".format(self.path_working_cpy_root))
                    print("{0}".format(err))

                if os.path.exists(self.path_working_cpy_root):
                    print("[ OK ] Created a \"{0}\" directory".format(self.path_working_cpy_root))
            folder_sequence = (self.working_cpy_externals,)
            self.create_root_subfolder(folder_sequence)
        else:
            print("[FAIL] The \"{0}\" directory already exists.".format(externals_path))
            return False

        externals_list = open(externals_path + "/" + "list.txt", "wt")

        parents = self.results.keys()
        for parent in parents:
            pass
            arguments = self.results[parent].keys()
            for folder in arguments:
                pass
                for value in self.results[parent][folder]:
                    if value is not None:
                        arguments = self.working_cpy_externals, value["LOCAL_REPO_NAME"],
                        value["LOCAL_REPO_PATH"] = self.create_root_subfolder(arguments)
                        result = git.svn.clone(value["URL"], value["REVISION"], value["LOCAL_REPO_PATH"])
                        # TODO: write data to the file in one string of code, I read that this is possible
                        log = open(value["LOCAL_REPO_PATH"] + "/.." + "/" + value["LOCAL_REPO_NAME"] + ".log", "wt")
                        log.write(result)
                        log.close()
                        externals_list.write(value["LOCAL_REPO_NAME"] + " : -r" + value["REVISION"] + " " + value["URL"] + "\n")

        externals_list.close()
        return True

    def clone_working_copy(self):   # Executes git svn clone for the main repo
        working_copy_path = self.path_working_cpy_root + "/" + self.working_cpy_placement
        if not os.path.exists(working_copy_path):
            if not os.path.exists(self.path_working_cpy_root):
                os.mkdir(self.path_working_cpy_root)
                if os.path.exists(self.path_working_cpy_root):
                    print("[ OK ] Created a \"{0}\" directory".format(self.path_working_cpy_root))
            folder_sequence = (self.working_cpy_placement,)
            self.create_root_subfolder(folder_sequence)
        else:
            print("[FAIL] The \"{0}\" directory already exists.".format(working_copy_path))
            return False

        result = git.svn.clone(self.url_repository_root + "/" + self.url_repository_rel, "HEAD", working_copy_path)
        log = open(working_copy_path + "/.." + "/clone.log", "wt")
        log.write(result)
        log.close()

        parents = self.results.keys()
        for parent in parents:
            pass
            arguments = self.results[parent].keys()
            for folder in arguments:
                pass
                for value in self.results[parent][folder]:
                    if value is not None:
                        value["DST_PATH"] = working_copy_path + folder.replace(parent, "") + "/" + value["DST_PATH"];
                        pass

        return True

    # Creates a set of symbolic links in the same way as svn:externals should create
    # its folders
    def create_symlinks(self):
        parents = self.results.keys()
        for parent in parents:
            pass
            arguments = self.results[parent].keys()
            for folder in arguments:
                pass
                for value in self.results[parent][folder]:
                    if value is not None:
                        # TODO: should be "git submodule..." instead of "git clone..."
                        result = git.clone(value["LOCAL_REPO_PATH"], value["DST_PATH"])
                        pass
        return True

    def create_root_subfolder(self, folders):
        folder_separator  = str()
        folder_path = self.path_working_cpy_root
        if "nt" == os.name:
            folder_separator = "\\"
        if "posix" == os.name:
            folder_separator = "/"
        for item in folders:
            folder_path += folder_separator + item

        os.mkdir(folder_path)
        if os.path.exists(folder_path):
            print("[ OK ] Created a \"{0}\" directory.".format(folder_path))

        return folder_path

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")
