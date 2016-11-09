# -*- coding: utf-8 -*-
import sys
import re_helpers

# the Parser class is intended to read command line and provide settings read from keys


class Parser:
    def __init__(self):
        self.repository_url = ""
        self.repository_rev = ""
        self.working_copy_path = ""
        self.config_path = ""
        self.cfg_create = False

        self.key_url = "--url"
        self.key_rev = "--revision"
        self.key_path = "--path"
        self.key_cfg = "--config"
        self.key_cfg_crt = "--cfgcreate"

        self.re_url = re_helpers.url_subversion
        self.re_path = re_helpers.path_absolute
        self.re_number = re_helpers.number_decimal

        pass

    def read(self):
        cArg = 1
        while cArg < len(sys.argv):
            current = sys.argv[cArg]
            if current == "--url":
                cArg += self.read_url(sys.argv[cArg + 1])
            elif current == "--revision":
                cArg += self.read_revision(sys.argv[cArg + 1])
            elif current == "--path":
                cArg += self.read_path(sys.argv[cArg + 1])
            elif current == "--config":
                cArg += self.read_config(sys.argv[cArg + 1])
            elif current == "--cfgcreate":
                self.cfg_create = True

            cArg += 1

        return True

    def read_url(self, string):
        if self.is_url(string):
            self.repository_url = string
            return True
        return False

    def read_revision(self, string):
        if self.is_number(string):
            self.repository_rev = string
            return True
        if string == "HEAD":
            return True
        return False

    def read_path(self, string):
        if self.is_path(string):
            self.working_copy_path = string
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
        result  = "URL : \"" + self.repository_url + "\"\n"
        result += "REVISION : \"" + self.repository_rev + "\"\n"
        result += "PATH : \"" + self.working_copy_path + "\"\n"
        result += "CONFIG : \"" + self.config_path + "\"\n"
        result += "CFGCREATE : \"" + self.cfg_create + "\"\n"
        return result


if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

