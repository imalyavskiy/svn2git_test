# -*- coding: utf-8 -*-
import command_prompt_parser
import svn2git_adapter as svn2git
import os
# The Reader class is intended to run command_prompt_parser.Parser class
# if the --config key is present then the Reader class must read it and provide
# settings


class Reader(command_prompt_parser.Parser):
    def __init__(self):
        super().__init__()

        self.adapter = object()
        self.opt_url = "URL : \""
        self.opt_rev = "REVISION : \""
        self.opt_path = "PATH : \""

    def init(self, adapter):
        self.adapter = adapter
        # read settings
        if not super().read():
            print("[FAIL] no arguments provided. Don't know what to do.")
            return False

        if len(self.config_path) and os.path.isfile(self.config_path):
            with open(self.config_path, "rt") as config:
                lines = config.readlines()  # the config file is closed automatically at the end of the block

            for line in lines:
                line = line.replace("\n", "")
                if line.startswith(self.opt_url) and not len(self.repository_url):
                    line = line.replace(self.opt_url, "")
                    line = line.replace("\"", "")
                    if self.is_url(line):
                        self.repository_url = line
                    continue
                if line.startswith(self.opt_rev) and not len(self.repository_rev):
                    line = line.replace(self.opt_rev, "")
                    line = line.replace("\"", "")
                    if self.is_number(line) or line == "HEAD":
                        self.repository_rev = line
                    continue
                if line.startswith(self.opt_path) and not len(self.working_copy_path):
                    line = line.replace(self.opt_path, "")
                    line = line.replace("\"", "")
                    if self.is_path(line):
                        self.working_copy_path = line
                    continue

        if self.adapter.is_url(self.repository_url):
            print("[ OK ] Argument - Source URL.")
        else:
            print("[FAIL] Argument 1: not an URL")
            return False

        if self.adapter.is_path(self.working_copy_path):
            print("[ OK ] Argument - destination path.")
        else:
            print("[FAIL] Argument 2: is not a path")
            return False

        print("[INFO] URL to process: {0}".format(self.repository_url))

        # check settings
        if not self.adapter.attach(self.repository_url):
            print("[FAIL] Cannot attach the resource.")
            return False

        self.adapter.project_url = self.repository_url
        self.adapter.path_working_cpy_root = self.working_copy_path
        self.adapter.working_cpy_externals += "externals"
        self.adapter.working_cpy_placement += "working_cpy"

        return True

    def __str__(self):
        return super.__str__()

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

