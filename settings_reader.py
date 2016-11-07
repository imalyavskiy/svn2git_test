# -*- coding: utf-8 -*-
import command_prompt_parser
import svn2git_adapter as svn2git
import os

# The Reader class is intended to run command_prompt_parser.Parser class
# if the --config key is present then the Reader class must read it and provide
# settings

class Reader:
    def __init__(self):
        self.cmd = command_prompt_parser.Parser()
        self.adapter = svn2git.Adapter()

    def read(self):

        if not self.cmd.read():
            return False

        if len(self.cmd.config_path) and os.path.isfile(self.cmd.config_path):
            config = open(self.cmd.config_path)
        else:
            print("[WARN] The \"{0}\" config file does not exist".format(self.cmd.config_path))

        if config is not None:
            pass                # read config file

        if self.adapter.is_url(self.cmd.repository_url):
            print("[ OK ] Argument - Source URL.")
        else:
            print("[FAIL] Argument 1: not an URL")

        if self.adapter.is_path(self.cmd.working_copy_path):
            print("[ OK ] Argument - destination path.")
        else:
            print("[FAIL] Argument 2: is not a path")

        print(">>> URL to process: {0}".format(self.cmd.repository_url))

        return True

    def check(self):
        if not self.adapter.attach(self.cmd.repository_url):
            print("[FAIL] Cannot attach the resource.")
            return False
        return True

    def __str__(self):
        return ""

