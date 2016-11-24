# -*- coding: utf-8 -*-
import sys
import re_helpers

# the Parser class is intended to read command line and provide settings read from keys
class Settings:
    def __init__(self):
        self.repository_url = ""
        self.repository_rev = ""
        self.working_copy_path = ""
        self.config_path = ""
        self.blank_cfg_file = ""

class Parser(Settings):
    def __init__(self):
        super().__init__()

        self.key_url = "--url"
        self.key_rev = "--revision"
        self.key_path = "--path"
        self.key_cfg = "--config"
        self.key_cfg_crt = "--cfgcreate"

        self.re_url = re_helpers.url_subversion
        self.re_path = re_helpers.path_absolute
        self.re_number = re_helpers.number_decimal

    def read(self):
        c_arg = 1
        while c_arg < len(sys.argv):
            current = sys.argv[c_arg]
            if current == "--url":
                c_arg += self.read_url(sys.argv[c_arg + 1])
            elif current == "--revision":
                c_arg += self.read_revision(sys.argv[c_arg + 1])
            elif current == "--path":
                c_arg += self.read_path(sys.argv[c_arg + 1])
            elif current == "--config":
                c_arg += self.read_config(sys.argv[c_arg + 1])
            elif current == "--cfgcreate":
                c_arg += self.read_cfg_path(sys.argv[c_arg+1])

            c_arg += 1

        return True

    def read_url(self, string):
        if self.is_url(string):
            self.repository_url = string
            return True
        return False

    def read_revision(self, string):
        if self.is_number(string) or string == "HEAD":
            self.repository_rev = string
            return True
        return False

    def read_path(self, string):
        if self.is_path(string):
            self.working_copy_path = string
            return True
        return False

    def read_cfg_path(self, string):
        if self.is_path(string):
            self.blank_cfg_file = string
            return True
        return False

    def read_config(self, string):
        if self.is_path(string):
            self.config_path = string
            return True
        return False

    def is_url(self, string):
        m = self.re_url.match(string)
        if m is not None and m.group() == string:
            return True
        return False

    def is_number(self, string):
        m = self.re_number.match(string)
        if m is not None and m.group() == string:
            return True
        return False

    def is_path(self, string):
        m = self.re_path.match(string)
        if m is not None and m.group() == string:
            return True
        return False

    def __str__(self):
        result = ""
        if len(self.repository_url):
            result += "URL : \"" + self.repository_url + "\"\n"
        if len(self.repository_rev):
            result += "REVISION : \"" + self.repository_rev + "\"\n"
        if len(self.working_copy_path):
            result += "PATH : \"" + self.working_copy_path + "\"\n"
        if len(self.config_path):
            result += "CONFIG : \"" + self.config_path + "\"\n"
        if len(self.blank_cfg_file):
            result += "CFGCREATE : \"" + self.blank_cfg_file + "\"\n"
        return result


if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

